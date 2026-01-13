from pathlib import Path
import re
import numpy as np
import pandas as pd

ET_TZ = "America/New_York"

YEAR = 2024
ET_ANCHOR_START = pd.Timestamp(f"{YEAR}-01-01 00:00:00")  # naive ET anchor
HOURS_IN_YEAR = 8784 if (YEAR % 4 == 0 and (YEAR % 100 != 0 or YEAR % 400 == 0)) else 8760

# -----------------------------
# Helpers
# -----------------------------
def norm(s: str) -> str:
    s = str(s).strip().lower()
    # SAFE fix: only replace standalone typo "witho" (do NOT corrupt "without")
    s = re.sub(r"\bwitho\b", "without", s)
    s = re.sub(r"[()]", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def clean_numeric_series(s: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(s):
        return s.astype("float64", copy=False)
    ss = s.astype(str).str.strip()
    ss = ss.replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA, "-": pd.NA})
    ss = ss.str.replace(",", "", regex=False)
    return pd.to_numeric(ss, errors="coerce")

def find_first_col(df: pd.DataFrame, candidates: list[str]) -> str:
    mapping = {norm(c): c for c in df.columns}
    for cand in candidates:
        k = norm(cand)
        if k in mapping:
            return mapping[k]
    return ""

def find_cols_by_regex(df: pd.DataFrame, pattern: str) -> list[str]:
    rx = re.compile(pattern)
    return [c for c in df.columns if rx.search(norm(c))]

def coalesce_cols(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    """Row-wise first non-null across alternative columns (NOT additive)."""
    if not cols:
        return pd.Series(np.nan, index=df.index, dtype="float64")
    cleaned = [clean_numeric_series(df[c]) for c in cols]
    tmp = pd.concat(cleaned, axis=1)
    return tmp.bfill(axis=1).iloc[:, 0]

def sum_components(series_list: list[pd.Series]) -> pd.Series:
    """Row-wise sum for true components (e.g., solar with IBS + without IBS)."""
    if not series_list:
        return pd.Series(np.nan)
    return pd.concat(series_list, axis=1).sum(axis=1, min_count=1)

def tiered_value_from_cols(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    """
    Row-wise priority: Imputed -> Adjusted -> Raw
    Within tier, treat columns as alternatives -> COALESCE (not sum).
    """
    imp = [c for c in cols if "imputed" in norm(c)]
    adj = [c for c in cols if ("imputed" not in norm(c)) and ("adjusted" in norm(c))]
    raw = [c for c in cols if ("imputed" not in norm(c)) and ("adjusted" not in norm(c))]

    s_imp = coalesce_cols(df, imp)
    s_adj = coalesce_cols(df, adj)
    s_raw = coalesce_cols(df, raw)

    return s_imp.combine_first(s_adj).combine_first(s_raw)

def tiered_value(df: pd.DataFrame, base_regex: str) -> pd.Series:
    return tiered_value_from_cols(df, find_cols_by_regex(df, base_regex))

def tiered_value_excluding(df: pd.DataFrame, base_regex: str, exclude_tokens: list[str]) -> pd.Series:
    rx = re.compile(base_regex)
    cols = []
    for c in df.columns:
        h = norm(c)
        if rx.search(h) and not any(tok in h for tok in exclude_tokens):
            cols.append(c)
    return tiered_value_from_cols(df, cols)

# -----------------------------
# Build ET-anchored, UTC-stepped hourly index
# -----------------------------
def build_et_anchored_utc_hour_index() -> pd.DataFrame:
    """
    Create exactly HOURS_IN_YEAR rows, starting at YEAR-01-01 00:00 ET,
    advancing +1 hour in UTC each row.

    Returns dataframe with:
      hour_index, ts_utc_excel, timestamp_utc, ts_et_excel, timestamp_et
    """
    start_utc = ET_ANCHOR_START.tz_localize(ET_TZ).tz_convert("UTC").tz_localize(None)
    utc_index = pd.date_range(start=start_utc, periods=HOURS_IN_YEAR, freq="H")

    # Convert each UTC hour to ET label (DST-safe)
    et = utc_index.tz_localize("UTC").tz_convert(ET_TZ)

    out = pd.DataFrame({
        "hour_index": np.arange(HOURS_IN_YEAR, dtype=int),
        "ts_utc_excel": utc_index,  # naive UTC
        "timestamp_utc": utc_index.strftime("%Y-%m-%d %H:%M"),
        "ts_et_excel": et.tz_localize(None),
        "timestamp_et": et.strftime("%Y-%m-%d %H:%M"),
    })

    return out

# -----------------------------
# Per-file standardization
# -----------------------------
TIME_COL_CANDS = ["UTC Time at End of Hour", "UTC Time", "UTC Datetime"]
BA_COL_CANDS   = ["Balancing Authority", "BA"]

def standardize_one_file(path: Path, utc_start: pd.Timestamp, utc_end: pd.Timestamp) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)

    time_col = find_first_col(df, TIME_COL_CANDS)
    ba_col   = find_first_col(df, BA_COL_CANDS)
    if not time_col or not ba_col:
        raise ValueError(f"[{path.name}] Missing required columns: time or balancing authority")

    # Parse UTC timestamp (end of hour)
    ts_utc = pd.to_datetime(df[time_col], utc=True, errors="raise")
    df["ts_utc_excel"] = ts_utc.dt.tz_convert("UTC").dt.tz_localize(None)

    # Filter to the UTC window needed for the ET-anchored year
    df = df[(df["ts_utc_excel"] >= utc_start) & (df["ts_utc_excel"] < utc_end)].copy()

    # Demand (exclude forecast)
    df["us_demand_mw"] = tiered_value_excluding(
        df,
        base_regex=r"^(demand|load) mw(\s|$)",
        exclude_tokens=["forecast"],
    )

    # Fuels
    df["gen_coal_mw"] = tiered_value(df, r"^net generation.*mw.*from coal")
    df["gen_natural_gas_mw"] = tiered_value(df, r"^net generation.*mw.*from natural gas")
    df["gen_nuclear_mw"] = tiered_value(df, r"^net generation.*mw.*from nuclear")
    df["gen_oil_mw"] = tiered_value(df, r"^net generation.*mw.*from all petroleum products")
    df["gen_geothermal_mw"] = tiered_value(df, r"^net generation.*mw.*from geothermal")
    df["gen_other_fuel_mw"] = tiered_value(df, r"^net generation.*mw.*from other fuel sources")
    df["gen_unknown_fuel_mw"] = tiered_value(df, r"^net generation.*mw.*from unknown fuel sources")

    # Solar (components)
    solar_wo = tiered_value(df, r"^net generation.*mw.*from solar.*\bwithout\b integrated battery storage")
    solar_w  = tiered_value(df, r"^net generation.*mw.*from solar.*\bwith\b integrated battery storage")
    solar_new_total = sum_components([solar_wo, solar_w])
    solar_old = tiered_value(df, r"^net generation.*mw.*from solar(?!.*integrated battery storage)")
    df["gen_solar_mw"] = solar_new_total.combine_first(solar_old)

    # Wind (components)
    wind_wo = tiered_value(df, r"^net generation.*mw.*from wind.*\bwithout\b integrated battery storage")
    wind_w  = tiered_value(df, r"^net generation.*mw.*from wind.*\bwith\b integrated battery storage")
    wind_new_total = sum_components([wind_wo, wind_w])
    wind_old = tiered_value(df, r"^net generation.*mw.*from wind(?!.*integrated battery storage)")
    df["gen_wind_mw"] = wind_new_total.combine_first(wind_old)

    # Hydro (components)
    hydro_old_total = tiered_value(df, r"^net generation.*mw.*from hydropower and pumped storage")
    hydro_excl = tiered_value(df, r"^net generation.*mw.*from hydropower excluding pumped storage")
    pumped     = tiered_value(df, r"^net generation.*mw.*from pumped storage")
    hydro_new_total = sum_components([hydro_excl, pumped])
    df["gen_hydro_mw"] = hydro_new_total.combine_first(hydro_old_total)

    # Storage
    df["gen_battery_storage_mw"] = tiered_value(df, r"^net generation.*mw.*from battery storage")
    df["gen_other_storage_mw"] = tiered_value(df, r"^net generation.*mw.*from other energy storage")
    df["gen_unknown_storage_mw"] = tiered_value(df, r"^net generation.*mw.*from unknown energy storage")

    keep = ["ts_utc_excel",
            "us_demand_mw",
            "gen_coal_mw", "gen_natural_gas_mw", "gen_nuclear_mw", "gen_oil_mw",
            "gen_hydro_mw", "gen_solar_mw", "gen_wind_mw",
            "gen_battery_storage_mw", "gen_other_storage_mw", "gen_unknown_storage_mw",
            "gen_geothermal_mw", "gen_other_fuel_mw", "gen_unknown_fuel_mw"]
    out = df[keep].copy()
    out["__source_file"] = path.name
    return out

# -----------------------------
# Main
# -----------------------------
def main(input_files: list[Path], outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)

    # Build the desired ET-anchored, UTC-stepped index
    idx = build_et_anchored_utc_hour_index()
    utc_start = idx["ts_utc_excel"].min()
    utc_end = idx["ts_utc_excel"].max() + pd.Timedelta(hours=1)

    # Read + standardize files within the needed UTC range
    standardized = [standardize_one_file(p, utc_start, utc_end) for p in input_files if p.exists()]
    if not standardized:
        raise FileNotFoundError("No input files found (check ./data/).")

    df = pd.concat(standardized, ignore_index=True)

    gen_cols = [c for c in df.columns if c.startswith("gen_") and c.endswith("_mw")]

    # US totals by UTC hour (the stable join key)
    us_utc = (
        df.groupby("ts_utc_excel", as_index=False)[["us_demand_mw"] + gen_cols]
          .sum(min_count=1)
          .sort_values("ts_utc_excel")
    )

    # Join onto our canonical index (guarantees 8760/8784 rows)
    out = idx.merge(us_utc, on="ts_utc_excel", how="left")

    # Add helpful columns for Excel/modeling
    out["date_et"] = out["ts_et_excel"].dt.strftime("%Y-%m-%d")
    out["hour_et"] = out["ts_et_excel"].dt.hour
    out["date_utc"] = out["ts_utc_excel"].dt.strftime("%Y-%m-%d")
    out["hour_utc"] = out["ts_utc_excel"].dt.hour

    core_total_cols = [
        "gen_coal_mw", "gen_natural_gas_mw", "gen_nuclear_mw", "gen_oil_mw",
        "gen_hydro_mw", "gen_solar_mw", "gen_wind_mw",
        "gen_geothermal_mw", "gen_other_fuel_mw", "gen_unknown_fuel_mw",
        "gen_battery_storage_mw", "gen_other_storage_mw", "gen_unknown_storage_mw",
    ]
    core_total_cols = [c for c in core_total_cols if c in out.columns]
    out["total_generation_core_mw"] = out[core_total_cols].sum(axis=1, min_count=1)

    # Diagnostics: are we missing values because we lack the 2025 file?
    missing = out["us_demand_mw"].isna().sum()
    print(f"Target rows: {HOURS_IN_YEAR} (year={YEAR})")
    print(f"Rows in output: {len(out)}")
    print(f"Hours with missing demand values after join: {missing}")
    if missing > 0:
        # show the first few missing rows (often near the end if you don't have 2025 Jan-Jun)
        print("\nFirst missing rows (if any):")
        print(out.loc[out["us_demand_mw"].isna(), ["hour_index", "timestamp_et", "timestamp_utc"]].head(10).to_string(index=False))
        print("\nIf the missing UTC timestamps are on 2025-01-01 00:00–04:00 UTC, you need EIA930_BALANCE_2025_Jan_Jun.csv.")

    # Write outputs
    out_all = outdir / f"us_hourly_demand_and_generation_et_anchored_utc_stepped_{YEAR}.csv"
    out.to_csv(out_all, index=False)
    print("\nWrote:", out_all.resolve())

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    OUT_DIR = BASE_DIR / "out_930_et_anchor_utc_step"

    input_files = [
        DATA_DIR / "EIA930_BALANCE_2023_Jul_Dec.csv",
        DATA_DIR / "EIA930_BALANCE_2024_Jan_Jun.csv",
        DATA_DIR / "EIA930_BALANCE_2024_Jul_Dec.csv",
        # Optional but often needed to cover the last ET hours of the year (which are early Jan UTC):
        DATA_DIR / "EIA930_BALANCE_2025_Jan_Jun.csv",
    ]

    main(input_files=input_files, outdir=OUT_DIR)
