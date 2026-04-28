import os
import sys
import re
import csv
import pandas as pd
import numpy as np

# =========================
# Paths / filenames
# =========================
BASE_DIR = r"C:\Users\RobbieOrvis\Models\US\Models\eps-us\InputData\trans\TTS"

INPUT_FILE = os.path.join(BASE_DIR, "calibration_parameters.csv")
TEMPLATE_FILE = os.path.join(BASE_DIR, "format.csv")

OUT_FLAT = os.path.join(BASE_DIR, "calibration_parameters_shareweights.csv")
OUT_TEMPLATE = os.path.join(BASE_DIR, "shareweights_formatted.csv")

# =========================
# Settings
# =========================
COST_CUTOFF = 10.0          # skip ANY option with cost_per_mile > 10 => weight=0
EPS = 1e-300
TARGET_YEARS = [2024, 2025]
RENORMALIZE_SHARES = True   # rescale shares to sum to 1 within (vehicle_type, year)


# -------------------------
# Normalization helpers
# -------------------------
def normalize_colname(c: str) -> str:
    return (
        str(c).strip().lower()
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("  ", " ")
        .replace(" ", "_")
    )

def clean_text(s: str) -> str:
    return " ".join(str(s).strip().lower().replace(",", " ").split())

def canon_vehicle_type(vt: str) -> str:
    x = clean_text(vt)
    x = x.replace("ldvs", "ldv").replace("hdvs", "hdv")

    is_passenger = "passenger" in x
    is_freight = "freight" in x
    is_ldv = "ldv" in x
    is_hdv = "hdv" in x

    if is_passenger and is_ldv:
        return "passenger ldv"
    if is_passenger and is_hdv:
        return "passenger hdv"
    if is_freight and is_ldv:
        return "freight ldv"
    if is_freight and is_hdv:
        return "freight hdv"

    return x  # fallback

def canon_tech(t: str) -> str:
    x = clean_text(t)
    x = re.sub(r"\bvehicle\b", "", x).strip()
    x = x.replace("plug-in", "plugin").replace("plug in", "plugin")

    # abbreviations
    if x in ["bev", "ev"]:
        return "battery electric"
    if x in ["phev"]:
        return "plugin hybrid"
    if x in ["ngv", "cng", "lng"]:
        return "natural gas"
    if x in ["lpg", "propane"]:
        return "lpg"
    if x in ["fcev", "fcv"]:
        return "hydrogen"
    if x in ["ice"]:
        return "gasoline"

    # text matches
    if "battery" in x and "electric" in x:
        return "battery electric"
    if "natural" in x and "gas" in x:
        return "natural gas"
    if "gasoline" in x:
        return "gasoline"
    if "diesel" in x:
        return "diesel"
    if "plugin" in x and "hybrid" in x:
        return "plugin hybrid"
    if "lpg" in x:
        return "lpg"
    if "hydrogen" in x:
        return "hydrogen"

    return x  # fallback


# -------------------------
# Load input
# -------------------------
def load_input() -> pd.DataFrame:
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)
    df.columns = [normalize_colname(c) for c in df.columns]

    required = ["year", "vehicle_type", "tech", "cost_per_mile", "share_obs", "exponent"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}\nFound: {list(df.columns)}")

    df["year"] = df["year"].astype(int)
    df["vehicle_type"] = df["vehicle_type"].astype(str)
    df["tech"] = df["tech"].astype(str)
    df["cost_per_mile"] = df["cost_per_mile"].astype(float)
    df["share_obs"] = df["share_obs"].astype(float)
    df["exponent"] = df["exponent"].astype(float)

    df["vt_key"] = df["vehicle_type"].apply(canon_vehicle_type)
    df["tech_key"] = df["tech"].apply(canon_tech)
    return df


# -------------------------
# Compute weights safely (no overflow)
# -------------------------
def compute_shareweights(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assumed probability form:
      P_j ∝ w_j * exp(exponent * cost)

    Solve (up to scaling constant):
      w_j ∝ share_obs_j * exp(-exponent * cost)

    Implementation:
      - if cost > COST_CUTOFF => shareweight=0
      - otherwise compute in LOG SPACE and normalize within group so max weight = 1
    """
    out_blocks = []

    for (vt_key, year), g in df.groupby(["vt_key", "year"], dropna=False):
        g = g.copy()
        exponent = float(g["exponent"].dropna().iloc[0])

        # Optional: rescale shares to sum to 1
        if RENORMALIZE_SHARES:
            ssum = g["share_obs"].sum()
            if ssum > 0:
                g["share_obs"] = g["share_obs"] / ssum

        cost = g["cost_per_mile"].values
        share = g["share_obs"].values

        # Skip high-cost techs entirely
        skip = cost > COST_CUTOFF
        g["shareweight"] = 0.0

        idx = np.where(~skip)[0]
        if len(idx) == 0:
            g["alpha"] = -np.inf
            out_blocks.append(g)
            continue

        # log(w_raw) = log(share) - exponent * cost
        share_safe = np.clip(share[idx], EPS, 1.0)
        logw = np.log(share_safe) - exponent * cost[idx]

        # Normalize in log-space so max(logw)=0 -> max weight = 1
        max_logw = np.max(logw)
        w = np.exp(logw - max_logw)

        g.loc[g.index[idx], "shareweight"] = w
        g["alpha"] = np.where(g["shareweight"] > 0, np.log(g["shareweight"]), -np.inf)
        out_blocks.append(g)

    return pd.concat(out_blocks, ignore_index=True)


# -------------------------
# Write flat output
# -------------------------
def write_flat(weights: pd.DataFrame) -> None:
    cols = [
        "year", "vehicle_type", "tech",
        "cost_per_mile", "share_obs", "exponent",
        "shareweight", "alpha"
    ]
    # keep extra cols if present
    extra = [c for c in weights.columns if c not in cols]
    weights[cols + extra].to_csv(OUT_FLAT, index=False)
    print(f"\nOK: Wrote shareweights to:\n{OUT_FLAT}")


# -------------------------
# Fill template output
# -------------------------
def fill_template(weights: pd.DataFrame) -> None:
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Template file not found: {TEMPLATE_FILE}")

    w = weights[weights["year"].isin(TARGET_YEARS)].copy()

    lookup = {(r["vt_key"], int(r["year"]), r["tech_key"]): float(r["shareweight"])
              for _, r in w.iterrows()}

    tech_key_set = set(w["tech_key"].unique().tolist())

    def is_vehicle_header(text: str) -> bool:
        t = clean_text(text)
        return (("passenger" in t) or ("freight" in t)) and (("ldv" in t) or ("ldvs" in t) or ("hdv" in t) or ("hdvs" in t))

    output_rows = []
    current_vt_key = None

    filled_nonzero = 0
    with open(TEMPLATE_FILE, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            row = (row + ["", "", ""])[:3]
            raw0 = row[0]
            c0 = raw0.strip()

            if c0 and is_vehicle_header(c0):
                current_vt_key = canon_vehicle_type(c0)
                output_rows.append([row[0], row[1], row[2]])
                continue

            if current_vt_key and c0:
                tkey = canon_tech(c0)
                if tkey in tech_key_set:
                    v24 = lookup.get((current_vt_key, 2024, tkey), 0.0)
                    v25 = lookup.get((current_vt_key, 2025, tkey), 0.0)

                    if v24 != 0.0:
                        filled_nonzero += 1
                    if v25 != 0.0:
                        filled_nonzero += 1

                    def fmt(x):
                        if abs(x) < 1e-15:
                            return "0"
                        return f"{x:.12g}"

                    output_rows.append([row[0], fmt(v24), fmt(v25)])
                    continue

            output_rows.append([row[0], row[1], row[2]])

    with open(OUT_TEMPLATE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)

    print(f"\nOK: Wrote formatted output to:\n{OUT_TEMPLATE}")
    print(f"OK: Filled {filled_nonzero} nonzero year-cells (zeros written as 0).")


# -------------------------
# Main
# -------------------------
def main():
    df = load_input()

    # Report share sums (important)
    sums = df.groupby(["vehicle_type", "year"])["share_obs"].sum().reset_index(name="share_sum")
    bad = sums[(sums["share_sum"] < 0.98) | (sums["share_sum"] > 1.02)]
    if len(bad) > 0:
        print("Warning: share_obs not ~1 in some groups:\n" + bad.to_string(index=False), file=sys.stderr)
        if RENORMALIZE_SHARES:
            print("RENORMALIZE_SHARES=True, so shares will be rescaled within each (vehicle_type, year).", file=sys.stderr)

    weights = compute_shareweights(df)

    # Always write both outputs
    write_flat(weights)
    fill_template(weights)


if __name__ == "__main__":
    main()