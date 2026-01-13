from pathlib import Path
import re
import numpy as np
import pandas as pd

YEAR = 2024
AS_OF_DATE = pd.Timestamp(f"{YEAR}-12-31")  # "operable as of end of 2024"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "out_930_with_860"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- Inputs (edit these if your filenames differ) ----
HOURLY_930_FILE = DATA_DIR / f"us_hourly_demand_and_generation_et_anchored_utc_stepped_2024.csv"
EIA860_FILE = DATA_DIR / "3_1_Generator_Y2024.xlsx"


# Prefer summer capacity if present; otherwise fallback to nameplate
PREFERRED_CAPACITY_FIELD = "summer"  # "summer" or "nameplate"

# Treat unit operable only if Status == OP by default
OPERABLE_STATUSES = {"OP"}

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def norm(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def pick_col(df: pd.DataFrame, candidates: list[str]) -> str:
    """Pick the first existing column matching candidates after normalization."""
    nmap = {norm(c): c for c in df.columns}
    for cand in candidates:
        key = norm(cand)
        if key in nmap:
            return nmap[key]
    return ""

def ym_to_timestamp(year, month) -> pd.Timestamp:
    """Convert year+month to first day of that month; returns NaT if missing."""
    try:
        y = int(year)
        m = int(month)
        if y <= 0 or m <= 0 or m > 12:
            return pd.NaT
        return pd.Timestamp(year=y, month=m, day=1)
    except Exception:
        return pd.NaT

def parse_float_series(s: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float)
    return pd.to_numeric(
        s.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce",
    )

# -------------------------------------------------------------------
# Resource mapping: EIA860 Energy Source 1 -> our categories
# Edit/extend if you want a different mapping.
# -------------------------------------------------------------------
FUEL_MAP = {
    # Coal-ish
    "BIT": "coal", "SUB": "coal", "LIG": "coal", "WC": "coal", "RC": "coal", "ANT": "coal",
    # Natural gas
    "NG": "natural_gas", "BFG": "natural_gas",  # BFG can be special; map to gas by default
    # Nuclear
    "NUC": "nuclear",
    # Hydro
    "WAT": "hydro", "HYC": "hydro",
    # Wind / solar / geo
    "WND": "wind",
    "SUN": "solar",
    "GEO": "geothermal",
    # Petroleum
    "DFO": "oil", "RFO": "oil", "JF": "oil", "KER": "oil", "PC": "oil", "WO": "oil",
    # Storage (Form 860 often uses "MWH" for batteries; some use "OTH" + storage prime mover)
    "MWH": "battery_storage",
}

# Prime mover codes that indicate storage if Energy Source isn’t explicit
STORAGE_PRIME_MOVERS = {"BA", "BS"}  # BA = Battery Storage, BS seen in some vintages

def categorize_resource(energy_source_1: str, prime_mover: str) -> str:
    es = str(energy_source_1).strip().upper()
    pm = str(prime_mover).strip().upper()

    if pm in STORAGE_PRIME_MOVERS:
        return "battery_storage"

    return FUEL_MAP.get(es, "other_or_unknown")

# -------------------------------------------------------------------
# Load EIA 860 Generator data
# -------------------------------------------------------------------
def load_eia860_generator(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing EIA860 file: {path}")

    if path.suffix.lower() in [".xlsx", ".xls"]:
        # Try common sheet names first; fall back to first sheet
        xls = pd.ExcelFile(path)
        sheet = None
        for s in xls.sheet_names:
            if "generator" in norm(s):
                sheet = s
                break
        if sheet is None:
            sheet = xls.sheet_names[0]
        df = pd.read_excel(path, sheet_name=sheet)
    else:
        df = pd.read_csv(path, low_memory=False)

    # Column picks (robust across vintage variations)
    col_status = pick_col(df, ["Status", "Operating Status"])
    col_es1 = pick_col(df, ["Energy Source 1", "Energy Source Code 1", "Energy Source Code"])
    col_pm = pick_col(df, ["Prime Mover", "Prime Mover Code"])

    col_op_year = pick_col(df, ["Operating Year", "Operating Year (YYYY)", "Year of Commercial Operation"])
    col_op_month = pick_col(df, ["Operating Month", "Operating Month (MM)"])

    col_ret_year = pick_col(df, ["Retirement Year", "Planned Retirement Year", "Retirement Year (YYYY)"])
    col_ret_month = pick_col(df, ["Retirement Month", "Planned Retirement Month", "Retirement Month (MM)"])

    col_summer = pick_col(df, ["Summer Capacity (MW)", "Nameplate Capacity (MW) Summer", "Summer Capacity MW"])
    col_nameplate = pick_col(df, ["Nameplate Capacity (MW)", "Nameplate Capacity MW"])

    needed = {
        "status": col_status,
        "es1": col_es1,
        "pm": col_pm,
        "op_year": col_op_year,
        "op_month": col_op_month,
        "ret_year": col_ret_year,
        "ret_month": col_ret_month,
        "summer": col_summer,
        "nameplate": col_nameplate,
    }

    # Basic validation: we need at least status + op year + a capacity field
    if not needed["status"] or not needed["op_year"] or (not needed["summer"] and not needed["nameplate"]):
        raise ValueError(
            "Could not locate required columns in the EIA860 generator file.\n"
            f"Detected columns:\n{needed}"
        )

    out = df.copy()

    # Dates
    out["in_service_date"] = [
        ym_to_timestamp(y, m)
        for y, m in zip(out[needed["op_year"]], out[needed["op_month"]] if needed["op_month"] else [1]*len(out))
    ]

    if needed["ret_year"]:
        out["retire_date"] = [
            ym_to_timestamp(y, m)
            for y, m in zip(out[needed["ret_year"]], out[needed["ret_month"]] if needed["ret_month"] else [1]*len(out))
        ]
    else:
        out["retire_date"] = pd.NaT

    # Status
    out["status"] = out[needed["status"]].astype(str).str.strip().str.upper()

    # Capacity
    if PREFERRED_CAPACITY_FIELD == "summer" and needed["summer"]:
        out["capacity_mw"] = parse_float_series(out[needed["summer"]])
    elif needed["nameplate"]:
        out["capacity_mw"] = parse_float_series(out[needed["nameplate"]])
    else:
        # fallback
        out["capacity_mw"] = parse_float_series(out[needed["summer"]])

    # Resource
    es1 = out[needed["es1"]] if needed["es1"] else ""
    pm = out[needed["pm"]] if needed["pm"] else ""
    out["resource"] = [categorize_resource(e, p) for e, p in zip(es1, pm)]

    return out[["status", "in_service_date", "retire_date", "capacity_mw", "resource"]].copy()

def filter_operable_as_of(df860: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    """
    Operable as-of rules:
      - status in OPERABLE_STATUSES (default OP)
      - in_service_date <= as_of
      - not retired before/as_of:
            retire_date is NaT OR retire_date > as_of (strict >, since retire_date is first day of month)
    """
    df = df860.copy()

    df = df[df["status"].isin(OPERABLE_STATUSES)].copy()

    df = df[df["in_service_date"].notna() & (df["in_service_date"] <= as_of)].copy()

    # retirement: treat retire_date as first-of-month; if retire_date <= as_of month start, it's out
    df = df[df["retire_date"].isna() | (df["retire_date"] > as_of)].copy()

    df = df[df["capacity_mw"].notna() & (df["capacity_mw"] > 0)].copy()

    return df

def build_capacity_table(df860_operable: pd.DataFrame) -> pd.DataFrame:
    cap = df860_operable.groupby("resource", as_index=False)["capacity_mw"].sum()
    cap = cap.sort_values("capacity_mw", ascending=False)
    return cap

# -------------------------------------------------------------------
# Compute CFs from hourly generation
# -------------------------------------------------------------------
GEN_COL_TO_RESOURCE = {
    "gen_coal_mw": "coal",
    "gen_natural_gas_mw": "natural_gas",
    "gen_nuclear_mw": "nuclear",
    "gen_oil_mw": "oil",
    "gen_hydro_mw": "hydro",
    "gen_wind_mw": "wind",
    "gen_solar_mw": "solar",
    "gen_geothermal_mw": "geothermal",
    "gen_battery_storage_mw": "battery_storage",
}

def compute_capacity_factors(hourly: pd.DataFrame, cap_table: pd.DataFrame) -> pd.DataFrame:
    cap_map = cap_table.set_index("resource")["capacity_mw"].to_dict()

    out = hourly.copy()
    for gcol, resource in GEN_COL_TO_RESOURCE.items():
        if gcol not in out.columns:
            continue
        cap = cap_map.get(resource)
        if cap is None or cap <= 0:
            continue
        cf_col = f"cf_{resource}"
        out[cf_col] = out[gcol] / cap

        # Keep CF interpretable; allow modest >1 for data quirks
        out[cf_col] = out[cf_col].clip(lower=0, upper=1.5)

    return out

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    if not HOURLY_930_FILE.exists():
        raise FileNotFoundError(f"Missing hourly EIA-930 file: {HOURLY_930_FILE}")

    hourly = pd.read_csv(HOURLY_930_FILE, low_memory=False)

    # Ensure datetime columns parse cleanly
    for c in ["ts_utc_excel", "ts_et_excel"]:
        if c in hourly.columns:
            hourly[c] = pd.to_datetime(hourly[c], errors="coerce")

    df860 = load_eia860_generator(EIA860_FILE)
    df860_op = filter_operable_as_of(df860, AS_OF_DATE)
    cap = build_capacity_table(df860_op)

    # Save capacity table
    cap_out = OUT_DIR / f"us_capacity_by_resource_operable_asof_{YEAR}-12-31_form860.csv"
    cap.to_csv(cap_out, index=False)

    # Compute CFs
    out = compute_capacity_factors(hourly, cap)

    # Write combined output
    out_file = OUT_DIR / f"us_hourly_generation_capacity_factors_et_anchor_utc_step_{YEAR}_form860.csv"
    out.to_csv(out_file, index=False)

    # Quick console summary
    print("Form 860 generator rows (raw):", len(df860))
    print("Form 860 operable as-of:", AS_OF_DATE.date(), "rows:", len(df860_op))
    print("\nTop capacity (MW):")
    print(cap.head(12).to_string(index=False))
    print("\nWrote:")
    print(" ", cap_out.resolve())
    print(" ", out_file.resolve())

if __name__ == "__main__":
    main()
