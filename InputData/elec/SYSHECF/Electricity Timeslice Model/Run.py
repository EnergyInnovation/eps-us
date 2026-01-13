#!/usr/bin/env python3
"""
Representative-day and intra-day hour clustering with pinned seasonal peaks.
- Single-file input (hourly_data.csv) including capacities and capacity factors.
- Techs: solar_pv, onshore_wind, offshore_wind, distributed_pv (optional)
- Guarantees the representative days include: SUMMER peak and WINTER peak.
- Chronological hour blocks (DP) or k-means blocks.
- Full-year reconstruction error (RMSE) in MW and normalized (unitless).

Defaults allow running with zero CLI args.
"""

import os
import json
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# =============================
# User-defined run configuration (defaults)
# =============================
DEFAULT_CONFIG = {
    "infile": "./data/hourly_data.csv",
    "outdir": "./results",
    "mode": "fixed",                 # "fixed" or "budget"
    "k_days": 6,
    "k_hours": 24,
    "budget_slices": 80,            # used only if mode == "budget"
    "day_range": "12,36",            # used only if mode == "budget"
    "hour_range": "4,12",            # used only if mode == "budget"
    "error_features": "net_load_mw,vre_gen_mw",
    "hour_block_method": "average",  # or "representative"
    "chronological_blocks": "true",
    "regions_order": ["USA"],        # <---- per your request
    "export_cf_profiles": "true",
    "seed": 42,
}

# ---- Pinned seasonal peaks config ----
PIN_SEASONAL = True            # guarantee seasonal peak reps (summer & winter)
PIN_WEIGHT_POLICY = "natural"  # "natural" or "cap1"   (cap1 -> each pinned day weight = 1)
PEAK_FEATURE = "net_load_mw"   # change to "load_mw" if desired
WINTER_MONTHS = {12, 1, 2}
SUMMER_MONTHS = {6, 7, 8}

# =============================
# CLI + defaults
# =============================
def parse_args_with_defaults():
    import argparse, types
    ap = argparse.ArgumentParser(
        description="Representative-day and hour-block clustering (multi-region). "
                    "All params have sensible defaults so the script can run without CLI args."
    )
    ap.add_argument("--in", dest="infile", help="Input CSV with hourly data.")
    ap.add_argument("--outdir", help="Output directory.")
    ap.add_argument("--mode", choices=["fixed", "budget"], help="fixed uses k_days/k_hours; budget searches under a slice budget.")
    ap.add_argument("--k_days", type=int, help="Number of representative days (fixed mode).")
    ap.add_argument("--k_hours", type=int, help="Number of hour blocks (fixed mode).")
    ap.add_argument("--budget_slices", type=int, help="Max slices in budget mode (k_days*k_hours ≤ budget).")
    ap.add_argument("--day_range", help="Budget mode search range for k_days, e.g. 12,36")
    ap.add_argument("--hour_range", help="Budget mode search range for k_hours, e.g. 4,12")
    ap.add_argument("--error_features", help="Comma list of features for error metric.")
    ap.add_argument("--hour_block_method", choices=["average","representative"], help="Block representation method.")
    ap.add_argument("--chronological_blocks", choices=["true","false"], help="Enforce contiguous hour blocks.")
    ap.add_argument("--regions_order", nargs="*", help="Explicit region order for feature concatenation.")
    ap.add_argument("--export_cf_profiles", choices=["true","false"], help="Export average CFs per block × region.")
    ap.add_argument("--seed", type=int, help="Random seed.")
    cli = ap.parse_args()

    cfg = DEFAULT_CONFIG.copy()
    for k, v in vars(cli).items():
        if v is not None:
            cfg[k] = v
    return types.SimpleNamespace(**cfg)

# =============================
# Tech definitions
# =============================
TECHS = [
    ("solar_pv",      "solar_pv_cf",      "solar_pv_cap_mw",      "solar_pv_gen_mw"),
    ("onshore_wind",  "onshore_wind_cf",  "onshore_wind_cap_mw",  "onshore_wind_gen_mw"),
    ("offshore_wind", "offshore_wind_cf", "offshore_wind_cap_mw", "offshore_wind_gen_mw"),
    ("distributed_pv","distributed_pv_cf","distributed_pv_cap_mw","distributed_pv_gen_mw"),  # optional
]

# =============================
# Utilities
# =============================
def compute_generation(df: pd.DataFrame) -> pd.DataFrame:
    """Compute tech generation (MW) as CF × CAP if available; else pass through gen column or zeros."""
    df = df.copy()
    for _, cf_col, cap_col, gen_col in TECHS:
        if gen_col not in df.columns:
            df[gen_col] = 0.0
        has_cf  = cf_col  in df.columns
        has_cap = cap_col in df.columns
        if has_cf and has_cap:
            cf  = pd.to_numeric(df[cf_col],  errors="coerce").fillna(0.0)
            cap = pd.to_numeric(df[cap_col], errors="coerce").fillna(0.0)
            df[gen_col] = cf * cap
        else:
            df[gen_col] = pd.to_numeric(df.get(gen_col, 0.0), errors="coerce").fillna(0.0)
    return df

def compute_net_load(df: pd.DataFrame) -> pd.DataFrame:
    """Compute net_load_mw if missing: net_load = load - sum(VRE gen)."""
    df = df.copy()
    if "net_load_mw" not in df.columns:
        gen_cols = [gen for _, _, _, gen in TECHS if gen in df.columns]
        total_vre = df[gen_cols].sum(axis=1) if gen_cols else 0.0
        df["net_load_mw"] = pd.to_numeric(df["load_mw"], errors="coerce") - total_vre
    df["net_load_mw"] = pd.to_numeric(df["net_load_mw"], errors="coerce").fillna(0.0)
    return df

def daily_feature_block(hourly: pd.DataFrame, regions: List[str]) -> Tuple[pd.DataFrame, List[str]]:
    """Concatenate daily features across regions."""
    feats_per_region = []
    for r in regions:
        sub = hourly[hourly["region"] == r].copy()
        g = sub.groupby("date")

        def max_abs_ramp(x: pd.Series) -> float:
            arr = x.values
            if len(arr) < 2:
                return 0.0
            diffs = np.diff(arr)
            return float(np.nanmax(np.abs(diffs))) if len(diffs) > 0 else 0.0

        agg = pd.DataFrame({
            (r, "load_mean"): g["load_mw"].mean(),
            (r, "load_max"): g["load_mw"].max(),
            (r, "load_min"): g["load_mw"].min(),
            (r, "net_mean"): g["net_load_mw"].mean(),
            (r, "net_min"): g["net_load_mw"].min(),
            (r, "net_p95"): g["net_load_mw"].quantile(0.95),
            (r, "load_ramp_max"): g["load_mw"].apply(max_abs_ramp),
            (r, "net_ramp_max"): g["net_load_mw"].apply(max_abs_ramp),
        })

        # correlation load vs VRE sum
        gen_cols = [gen for _, _, _, gen in TECHS if gen in sub.columns]
        sub["vre_sum_mw"] = sub[gen_cols].sum(axis=1) if gen_cols else 0.0

        def corr_load_vre(x: pd.DataFrame) -> float:
            if x["load_mw"].std(ddof=0) == 0 or x["vre_sum_mw"].std(ddof=0) == 0:
                return 0.0
            return float(x["load_mw"].corr(x["vre_sum_mw"]))

        agg[(r, "corr_load_vre")] = g.apply(corr_load_vre, include_groups=False)

        agg.columns = ["__".join(map(str, c)) for c in agg.columns]
        feats_per_region.append(agg)

    joined = pd.concat(feats_per_region, axis=1, join="inner").sort_index()
    return joined, list(joined.columns)

def pick_representative_days(X_daily: pd.DataFrame, k_days: int, seed: int) -> Tuple[pd.Series, pd.DataFrame]:
    """KMeans daily clustering; pick medoids as rep days, weights by cluster size."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_daily.values)
    km = KMeans(n_clusters=k_days, random_state=seed, n_init="auto")
    labels = km.fit_predict(X_scaled)
    centers = km.cluster_centers_
    dists = ((X_scaled - centers[labels]) ** 2).sum(axis=1)
    df_idx = pd.DataFrame({"date": X_daily.index, "cluster": labels, "dist": dists}).set_index("date")

    rep_rows = []
    for c in range(k_days):
        in_c = df_idx[df_idx["cluster"] == c]
        if in_c.empty:
            continue
        rep_date = in_c["dist"].idxmin()
        weight = int(in_c.shape[0])
        rep_rows.append({"cluster": c, "rep_date": str(pd.Timestamp(rep_date).date()), "weight_days": weight,
                         "is_pinned": False, "pin_tags": ""})

    reps_df = pd.DataFrame(rep_rows).sort_values("cluster").reset_index(drop=True)
    return pd.Series(labels, index=pd.Index(pd.to_datetime(X_daily.index).normalize(), name="date"), name="cluster"), reps_df

def _summer_winter_peak_dates(df, peak_feature="net_load_mw",
                              winter_months=WINTER_MONTHS, summer_months=SUMMER_MONTHS):
    """Return dict {iso_date: set('winter'/'summer')} for winter and summer daily peaks."""
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.normalize()
    d["month"] = d["date"].dt.month
    pins = {}

    # Winter peak
    winter = d[d["month"].isin(winter_months)]
    if not winter.empty:
        w_daily = winter.groupby("date")[peak_feature].max()
        if not w_daily.empty:
            w_peak = w_daily.idxmax()
            pins.setdefault(w_peak.date().isoformat(), set()).add("winter")

    # Summer peak
    summer = d[d["month"].isin(summer_months)]
    if not summer.empty:
        s_daily = summer.groupby("date")[peak_feature].max()
        if not s_daily.empty:
            s_peak = s_daily.idxmax()
            pins.setdefault(s_peak.date().isoformat(), set()).add("summer")

    return pins  # e.g., {"2024-01-17": {"winter"}, "2024-08-24": {"summer"}}

def pick_representative_days_with_pins(
    X_daily: pd.DataFrame,
    k_days: int,
    seed: int,
    pinned_dates_iso=None,
    pin_tags_map=None,
    pin_weight_policy: str = "natural"
) -> Tuple[pd.Series, pd.DataFrame]:
    """
    KMeans daily clustering that guarantees pinned dates are reps.
    Pinned reps are included as centers; remaining days clustered into (k_days - n_pin).
    pin_weight_policy: "natural" or "cap1".
    """
    pinned_dates_iso = pinned_dates_iso or []
    pin_tags_map = pin_tags_map or {}

    dates_all = pd.to_datetime(X_daily.index).normalize()
    X = X_daily.values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    present_dates = set(dates_all.date)
    pins_clean = [p for p in pinned_dates_iso if pd.Timestamp(p).date() in present_dates]
    pins_clean = sorted(list(dict.fromkeys(pins_clean)))
    pin_mask = dates_all.isin(pd.to_datetime(pins_clean))
    n_pin = int(pin_mask.sum())

    if n_pin == 0:
        return pick_representative_days(X_daily, k_days, seed)
    if n_pin > k_days:
        raise ValueError(f"Pinned days ({n_pin}) exceed k_days ({k_days}). Increase k_days or reduce pins.")

    X_rest = X_scaled[~pin_mask]
    dates_rest = dates_all[~pin_mask]
    X_pins = X_scaled[pin_mask]
    dates_pins = dates_all[pin_mask]

    centers = []
    cluster_offset = 0
    k_rest = max(0, k_days - n_pin)
    if k_rest > 0:
        km = KMeans(n_clusters=k_rest, random_state=seed, n_init="auto").fit(X_rest)
        centers.append(km.cluster_centers_)
        cluster_offset = k_rest

    if n_pin > 0:
        centers.append(X_pins)

    C = np.vstack(centers) if centers else np.empty((0, X_scaled.shape[1]))

    # Assign all days to nearest center
    dists_all = ((X_scaled[:, None, :] - C[None, :, :])**2).sum(axis=2)
    labels = dists_all.argmin(axis=1)  # 0..k_days-1

    rep_rows = []
    pinned_cluster_indices = list(range(cluster_offset, cluster_offset + n_pin))
    pinned_idx_to_date = {cluster_offset + i: dates_pins[i].date().isoformat() for i in range(n_pin)}

    for ci in range(k_days):
        members = np.where(labels == ci)[0]
        if len(members) == 0:
            continue
        if ci in pinned_cluster_indices:
            rep_iso = pinned_idx_to_date[ci]
            weight = 1 if pin_weight_policy == "cap1" else int(len(members))
            rep_rows.append({
                "cluster": ci,
                "rep_date": rep_iso,
                "weight_days": weight,
                "is_pinned": True,
                "pin_tags": ",".join(sorted(pin_tags_map.get(rep_iso, set())))
            })
        else:
            center = C[ci]
            m_idx = members[np.argmin(((X_scaled[members] - center)**2).sum(axis=1))]
            rep_date = dates_all[m_idx]
            weight = int(len(members))
            rep_rows.append({
                "cluster": ci,
                "rep_date": rep_date.date().isoformat(),
                "weight_days": weight,
                "is_pinned": False,
                "pin_tags": ""
            })

    labels_series = pd.Series(labels, index=pd.Index(dates_all, name="date"), name="cluster")
    reps_df = pd.DataFrame(rep_rows).sort_values("cluster").reset_index(drop=True)
    return labels_series, reps_df

def hourly_feature_block(hourly: pd.DataFrame, regions: List[str], rep_dates: List[pd.Timestamp]) -> pd.DataFrame:
    """Concatenate hourly features for (rep_date, hour) across regions."""
    rows, index = [], []
    for d in rep_dates:
        sub_day = hourly[hourly["date"] == d]
        region_feats_hourly = []
        for r in regions:
            sub_r = sub_day[sub_day["region"] == r].copy()
            if "hour" not in sub_r.columns:
                sub_r["hour"] = sub_r["timestamp"].dt.hour
            sub_r = sub_r.set_index("hour").sort_index()

            feats = pd.DataFrame(index=sub_r.index)
            feats[f"{r}__net_load_mw"] = sub_r["net_load_mw"]
            feats[f"{r}__load_mw"]     = sub_r["load_mw"]
            gen_cols_r = [gen for _, _, _, gen in TECHS if gen in sub_r.columns]
            feats[f"{r}__vre_gen_mw"]  = sub_r[gen_cols_r].sum(axis=1) if gen_cols_r else 0.0
            region_feats_hourly.append(feats)

        H = pd.concat(region_feats_hourly, axis=1, join="inner").sort_index()
        for h in H.index:
            rows.append(H.loc[h].values)
            index.append((pd.Timestamp(d), int(h)))

    return pd.DataFrame(
        rows,
        index=pd.MultiIndex.from_tuples(index, names=["rep_date", "hour"]),
        columns=pd.concat(region_feats_hourly, axis=1).columns
    )

def relabel_blocks_by_time(labels: np.ndarray, hours: np.ndarray, k: int) -> np.ndarray:
    means = {c: (hours[labels == c].mean() if np.any(labels == c) else np.inf) for c in range(k)}
    order = sorted(means, key=lambda c: means[c])
    remap = {old: i+1 for i, old in enumerate(order)}
    return np.array([remap[l] for l in labels], dtype=int)

# =============================
# Full-year reconstruction error (correct)
# =============================
def _reconstruction_error_full_year(df_full, labels_series, reps_df, hb, regions, features):
    """
    Compute RMSE by reconstructing the FULL 8760-hour year using final day labels.
    Critical: compute block means per (rep_date, block_id, region) to preserve rep-day specificity.
    Returns dict with per-feature and mean MW / normalized RMSE.
    """
    import numpy as np
    import pandas as pd

    df = df_full.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    if "timestamp" in df.columns:
        df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour

    reps = reps_df.copy()
    reps["rep_date"] = pd.to_datetime(reps["rep_date"]).dt.normalize()
    hb2 = hb.copy()
    hb2["rep_date"] = pd.to_datetime(hb2["rep_date"]).dt.normalize()

    lab = labels_series.to_frame(name="cluster").copy()
    lab.index = pd.to_datetime(lab.index).normalize()
    date2cluster = lab["cluster"]
    clus2rep = reps.set_index("cluster")["rep_date"]
    date2rep = date2cluster.map(clus2rep)

    df = df.merge(date2rep.rename("rep_date"), left_on="date", right_index=True, how="left")
    df = df.merge(hb2[["rep_date","hour","block_id"]], on=["rep_date","hour"], how="left")

    feats = [f for f in features if f in df.columns]
    if not feats:
        raise ValueError("No error features found in dataframe.")

    block_means = (
        df.groupby(["rep_date","block_id","region"], dropna=False)[feats]
          .mean(numeric_only=True)
          .reset_index()
    )

    df_pred = df.merge(block_means, on=["rep_date","block_id","region"], suffixes=("", "_hat"), how="left")

    res = {"per_feature": {}}
    for f in feats:
        if f not in df_pred.columns or f + "_hat" not in df_pred.columns:
            continue
        diff = df_pred[f] - df_pred[f + "_hat"]
        rmse_mw = float(np.sqrt(np.nanmean(diff**2)))
        var = float(df_pred[f].var(ddof=0))
        rmse_norm = float(rmse_mw / np.sqrt(var)) if var > 0 else float("nan")
        res["per_feature"][f] = {"rmse_mw": rmse_mw, "rmse_norm": rmse_norm}

    vals_mw = [v["rmse_mw"] for v in res["per_feature"].values()]
    vals_nm = [v["rmse_norm"] for v in res["per_feature"].values()]
    res["mean_rmse_mw"] = float(np.nanmean(vals_mw)) if vals_mw else float("nan")
    res["mean_rmse_norm"] = float(np.nanmean(vals_nm)) if vals_nm else float("nan")
    return res

def compute_cluster_scalars(df_full, labels_series, reps_df, hour_block_method="representative"):
    """
    Returns a DataFrame with columns:
      cluster, region, weight_days, E_cluster_MWh, E_rep_day_MWh, scalar

    - E_cluster_MWh: sum over all real days assigned to cluster (per region)
    - E_rep_day_MWh: sum over the 24h of the cluster's representative date (per region)
    - scalar: 1.0 if hour_block_method == "average"; otherwise energy-preserving factor
    """
    import numpy as np
    import pandas as pd

    # --- Normalize inputs ---
    df = df_full.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    if "region" not in df.columns or "load_mw" not in df.columns:
        raise ValueError("df_full must include columns 'region' and 'load_mw'.")

    # labels_series: index=date, value=cluster
    ls = labels_series.copy()
    ls.index = pd.to_datetime(ls.index).normalize()
    day_assign = ls.rename("cluster").reset_index()  # cols: ['date','cluster']

    # Merge cluster labels onto ALL hourly rows
    df_lab = df.merge(day_assign, on="date", how="left")

    # If any rows are missing cluster, warn (they’ll be dropped)
    if df_lab["cluster"].isna().any():
        missing = int(df_lab["cluster"].isna().sum())
        print(f"⚠️  {missing} hourly rows had no cluster assignment and will be ignored in scalar calculation.")
        df_lab = df_lab[df_lab["cluster"].notna()].copy()

    df_lab["cluster"] = df_lab["cluster"].astype(int)

    # --- Cluster totals across full year (per region) ---
    clust_totals = (df_lab
        .groupby(["cluster", "region"], dropna=False)["load_mw"]
        .sum()
        .rename("E_cluster_MWh")
        .reset_index())

    # --- Representative-day totals (per region) ---
    reps = reps_df.copy()
    reps["rep_date"] = pd.to_datetime(reps["rep_date"]).dt.normalize()
    reps = reps[["cluster", "rep_date", "weight_days"]].copy()
    reps["cluster"] = reps["cluster"].astype(int)

    # Pull ONLY the representative dates, attach their cluster ids, sum 24h load by (cluster, region)
    rep_rows = (df_lab.merge(reps[["cluster", "rep_date"]],
                             left_on=["cluster", "date"],
                             right_on=["cluster", "rep_date"],
                             how="inner"))
    rep_day_totals = (rep_rows
        .groupby(["cluster", "region"], dropna=False)["load_mw"]
        .sum()
        .rename("E_rep_day_MWh")
        .reset_index())

    # --- Join and compute scalar ---
    out = (clust_totals
        .merge(rep_day_totals, on=["cluster", "region"], how="left")
        .merge(reps[["cluster", "weight_days"]].drop_duplicates(), on="cluster", how="left"))

    # Default scalar
    if str(hour_block_method).lower() == "average":
        out["scalar"] = 1.0
    else:
        denom = out["weight_days"].clip(lower=1).astype(float) * out["E_rep_day_MWh"].replace(0, np.nan)
        out["scalar"] = (out["E_cluster_MWh"] / denom).replace([np.inf, -np.inf], np.nan).fillna(1.0)

    # Final ordering
    return out[["cluster", "region", "weight_days", "E_cluster_MWh", "E_rep_day_MWh", "scalar"]].sort_values(["cluster", "region"]).reset_index(drop=True)


# =============================
# Main
# =============================
def main():
    args = parse_args_with_defaults()

    os.makedirs(args.outdir, exist_ok=True)
    if not os.path.exists(args.infile):
        print(f"⚠️  Input file not found at '{args.infile}'. "
              f"Update DEFAULT_CONFIG['infile'] or pass --in /path/to/hourly_data.csv")
        return

    # Load
    df = pd.read_csv(args.infile)
    required = ["timestamp", "region", "load_mw"]
    if any(c not in df.columns for c in required):
        raise ValueError("Input must include columns: timestamp, region, load_mw")

    # Time parsing
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError("Some timestamps could not be parsed. Ensure ISO-8601 hourly stamps.")
    df["date"] = pd.to_datetime(df["timestamp"]).dt.normalize()
    df["hour"] = df["timestamp"].dt.hour
    df["region"] = df["region"].astype(str)

    # Generation + net load
    df = compute_generation(df)
    df = compute_net_load(df)

    # Region order
    regions = list(args.regions_order) if args.regions_order else sorted(df["region"].unique().tolist())

    # ===== Daily clustering (with seasonal pins) =====
    X_daily, feat_names = daily_feature_block(df, regions)

    pinned_dates = []
    pinned_tags = {}
    if PIN_SEASONAL:
        auto_pins = _summer_winter_peak_dates(df, peak_feature=PEAK_FEATURE)
        # De-duplicate; keep only dates present in X_daily
        present = set(pd.to_datetime(X_daily.index).normalize().date)
        pinned_dates = sorted({d for d in auto_pins.keys() if pd.Timestamp(d).date() in present})
        pinned_tags = {d: auto_pins[d] for d in pinned_dates}

    if pinned_dates:
        print(f"Pinned representative dates (seasonal peaks): {pinned_dates}")
        if len(pinned_dates) >= args.k_days:
            raise ValueError(f"Too many pinned dates ({len(pinned_dates)}) for k_days={args.k_days}. Increase k_days or reduce pins.")
        labels_series, reps_df = pick_representative_days_with_pins(
            X_daily, args.k_days, args.seed,
            pinned_dates_iso=pinned_dates,
            pin_tags_map=pinned_tags,
            pin_weight_policy=PIN_WEIGHT_POLICY
        )
    else:
        labels_series, reps_df = pick_representative_days(X_daily, args.k_days, args.seed)

    # Save daily outputs
    day_assign = labels_series.reset_index()
    day_assign.columns = ["date", "cluster"]
    day_assign.to_csv(os.path.join(args.outdir, "day_assignments.csv"), index=False)

    # Write reps (ensure pin columns present)
    reps_out = reps_df.copy()
    for c in ["is_pinned", "pin_tags"]:
        if c not in reps_out.columns:
            reps_out[c] = False if c == "is_pinned" else ""
    reps_out.to_csv(os.path.join(args.outdir, "representative_days.csv"), index=False)

    # ----- Cluster scalars (energy-preserving factors) -----
    cluster_scalars = compute_cluster_scalars(
        df_full=df,
        labels_series=labels_series,
        reps_df=reps_df,
        hour_block_method=args.hour_block_method
    )
    cluster_scalars.to_csv(os.path.join(args.outdir, "cluster_scalars.csv"), index=False)
    print("Wrote cluster_scalars.csv (energy-preserving factors).")
    # Representative dates for hourly feature build
    rep_dates = pd.to_datetime(reps_df.sort_values("cluster")["rep_date"]).dt.normalize().tolist()

    # ===== Hour blocks =====
    XH = hourly_feature_block(df, regions, rep_dates)
    chronological_flag = (str(args.chronological_blocks).lower() == "true")

    if chronological_flag:
        tmp = XH.reset_index().copy()
        tmp["rep_date"] = pd.to_datetime(tmp["rep_date"]).dt.normalize()
        wmap = (reps_df.assign(rep_date=pd.to_datetime(reps_df["rep_date"]).dt.normalize())
                        .set_index("rep_date")["weight_days"].to_dict())
        tmp["w"] = tmp["rep_date"].map(wmap).astype(float)

        feat_cols = XH.columns.tolist()
        grp = tmp.groupby("hour")
        sumw = grp["w"].sum()
        sumwx = grp[feat_cols].apply(lambda g: (g.mul(tmp.loc[g.index, "w"], axis=0)).sum())
        mean_by_hour = sumwx.div(sumw, axis=0).reindex(range(0, 24)).ffill().bfill()
        W = sumw.reindex(range(0, 24)).ffill().bfill().values.astype(float)
        V = mean_by_hour.values

        S1 = np.zeros(25); Sxx = np.zeros(25); Sx = np.zeros((25, V.shape[1]))
        for h in range(24):
            w = W[h]; x = V[h]
            S1[h + 1] = S1[h] + w
            Sx[h + 1] = Sx[h] + w * x
            Sxx[h + 1] = Sxx[h] + w * (x @ x)

        def seg_cost(i, j):
            sw = S1[j + 1] - S1[i]
            sx = Sx[j + 1] - Sx[i]
            sxx = Sxx[j + 1] - Sxx[i]
            if sw <= 0: return 0.0
            return float(sxx - (sx @ sx) / sw)

        K = int(args.k_hours)
        DP = np.full((K + 1, 25), np.inf)
        BP = np.full((K + 1, 25), -1, dtype=int)
        DP[0, 0] = 0.0
        for m in range(1, K + 1):
            for t in range(m, 24 + 1):
                best_cost = np.inf; best_s = -1
                for s in range(m - 1, t):
                    c = DP[m - 1, s] + seg_cost(s, t - 1)
                    if c < best_cost: best_cost = c; best_s = s
                DP[m, t] = best_cost; BP[m, t] = best_s

        hour_to_block = {}
        m, t = K, 24; boundaries = []
        while m > 0:
            s = BP[m, t]
            boundaries.append((s, t - 1)); t = s; m -= 1
        boundaries = list(reversed(boundaries))
        for bid, (i, j) in enumerate(boundaries, start=1):
            for h in range(i, j + 1):
                hour_to_block[h] = bid

        hb = pd.DataFrame({
            "rep_date": [pd.Timestamp(idx[0]).normalize() for idx in XH.index],
            "hour": XH.index.get_level_values("hour").astype(int)
        })
        hb["block_id"] = hb["hour"].map(hour_to_block).astype(int)

    else:
        scaler_h = StandardScaler()
        XH_scaled = scaler_h.fit_transform(XH.values)
        km_h = KMeans(n_clusters=args.k_hours, random_state=args.seed, n_init="auto")
        h_labels = km_h.fit_predict(XH_scaled)
        hours = XH.index.get_level_values("hour").values.astype(int)
        block_labels = relabel_blocks_by_time(h_labels, hours, args.k_hours)
        hb = pd.DataFrame({
            "rep_date": [pd.Timestamp(idx[0]).normalize() for idx in XH.index],
            "hour": hours,
            "block_id": block_labels
        })

    hb["rep_date"] = pd.to_datetime(hb["rep_date"]).dt.normalize()
    wmap_final = (reps_df.assign(rep_date=pd.to_datetime(reps_df["rep_date"]).dt.normalize())
                         .set_index("rep_date")["weight_days"].to_dict())
    hb = hb.sort_values(["rep_date", "hour"]).reset_index(drop=True)
    hb["weight_hours"] = hb["rep_date"].map(wmap_final).astype(float)
    hb.to_csv(os.path.join(args.outdir, "hour_blocks.csv"), index=False)

    block_weights = hb.groupby("block_id")["weight_hours"].sum().reset_index() \
                      .rename(columns={"weight_hours": "total_hour_weight"})
    block_weights.to_csv(os.path.join(args.outdir, "hour_block_weights.csv"), index=False)

    # ===== Block profiles (average or representative hour) =====
    rep_dates_set = set(pd.to_datetime(reps_df["rep_date"]).dt.normalize().tolist())
    base_cols = ["date", "hour", "region", "load_mw", "net_load_mw"]
    tech_gen_cols = [gen for _, _, _, gen in TECHS]
    tech_cf_cols  = [cf  for _, cf, _, _ in TECHS]
    cols_keep = [c for c in (base_cols + tech_gen_cols + tech_cf_cols) if c in df.columns]

    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df_rep = df[df["date"].isin(rep_dates_set)][cols_keep].copy()
    df_rep = df_rep.rename(columns={"date": "rep_date"})
    df_rep["rep_date"] = pd.to_datetime(df_rep["rep_date"]).dt.normalize()
    hb["rep_date"] = pd.to_datetime(hb["rep_date"]).dt.normalize()

    df_rep = df_rep.merge(hb[["rep_date", "hour", "block_id", "weight_hours"]],
                          on=["rep_date", "hour"], how="left")

    if df_rep["block_id"].isna().all():
        raise ValueError("No (rep_date, hour) rows matched hour blocks. Check timestamps/timezone consistency.")

    present_gen_cols = [c for c in tech_gen_cols if c in df_rep.columns]
    df_rep["vre_gen_mw"] = df_rep[present_gen_cols].sum(axis=1) if present_gen_cols else 0.0

    if str(args.hour_block_method).lower() == "average":
        def wavg(g: pd.DataFrame, col: str) -> float:
            w = pd.to_numeric(g["weight_hours"], errors="coerce").values
            x = pd.to_numeric(g[col], errors="coerce").values
            return float(np.average(x, weights=w)) if np.sum(w) > 0 else float(np.nan)

        rows = []
        for (b, r), g in df_rep.groupby(["block_id", "region"]):
            row = {"block_id": int(b), "region": r}
            row["load_mw"]     = wavg(g, "load_mw")
            row["net_load_mw"] = wavg(g, "net_load_mw")
            for _, _, _, gen in TECHS:
                if gen in g.columns:
                    row[gen] = wavg(g, gen)
            row["vre_gen_mw"]  = wavg(g, "vre_gen_mw")
            rows.append(row)

        avg_profiles = pd.DataFrame(rows).sort_values(["region","block_id"]).reset_index(drop=True)
        avg_profiles.to_csv(os.path.join(args.outdir, "avg_block_profiles.csv"), index=False)

        if str(args.export_cf_profiles).lower() == "true":
            cf_present = [c for c in tech_cf_cols if c in df_rep.columns]
            if cf_present:
                rows_cf = []
                for (b, r), g in df_rep.groupby(["block_id", "region"]):
                    row = {"block_id": int(b), "region": r}
                    for c in cf_present:
                        row[c] = wavg(g, c)
                    rows_cf.append(row)
                avg_cf = pd.DataFrame(rows_cf).sort_values(["region","block_id"]).reset_index(drop=True)
                avg_cf.to_csv(os.path.join(args.outdir, "avg_block_cf.csv"), index=False)

    else:
        # Representative hour per block: medoid across rep days
        rows = []
        for b, g in df_rep.groupby("block_id"):
            featset = [c for c in ["load_mw", "net_load_mw", "vre_gen_mw"] if c in g.columns]
            if not featset:
                continue
            gh = g.groupby(["rep_date","hour"])[featset].sum().reset_index()
            X = gh[featset].values
            dmat = np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2)
            best_i = int(np.argmin(dmat.sum(axis=1)))
            rep_date_sel = pd.to_datetime(gh.loc[best_i, "rep_date"]).normalize()
            hour_sel = int(gh.loc[best_i, "hour"])
            gsel = g[(pd.to_datetime(g["rep_date"]).dt.normalize() == rep_date_sel) & (g["hour"] == hour_sel)]
            for r, gr in gsel.groupby("region"):
                row = {"block_id": int(b), "region": r, "rep_date": str(rep_date_sel.date()), "hour": hour_sel}
                row["load_mw"]     = float(gr["load_mw"].iloc[0])
                row["net_load_mw"] = float(gr["net_load_mw"].iloc[0])
                for _, _, _, gen in TECHS:
                    if gen in gr.columns:
                        row[gen] = float(gr[gen].iloc[0])
                row["vre_gen_mw"]  = float(gr["vre_gen_mw"].iloc[0])
                rows.append(row)
        rep_profiles = pd.DataFrame(rows).sort_values(["region","block_id"]).reset_index(drop=True)
        rep_profiles.to_csv(os.path.join(args.outdir, "rep_block_profiles.csv"), index=False)

    # ===== Timeslices + metadata =====
    timeslices = block_weights.rename(columns={"total_hour_weight": "duration_hours"})
    timeslices.to_csv(os.path.join(args.outdir, "timeslices.csv"), index=False)

    meta = {
        "mode": args.mode,
        "k_days": args.k_days,
        "k_hours": args.k_hours,
        "regions": regions,
        "features_daily": feat_names,
        "hour_block_method": args.hour_block_method,
        "chronological_blocks": args.chronological_blocks,
        "export_cf_profiles": args.export_cf_profiles,
        "random_seed": args.seed,
        "techs": [t[0] for t in TECHS],
        "pinned_dates": pinned_dates,
        "pin_weight_policy": PIN_WEIGHT_POLICY,
    }
    with open(os.path.join(args.outdir, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)

    # ===== Full-year reconstruction RMSE =====
    print("\nComputing full-year reconstruction error...")
    err_features = [f.strip() for f in args.error_features.split(",") if f.strip()]
    use_feats = [f for f in err_features if f in df.columns] or ["net_load_mw", "vre_gen_mw"]

    err = _reconstruction_error_full_year(
        df.assign(date=pd.to_datetime(df["date"]).dt.normalize()),
        labels_series, reps_df, hb, regions, use_feats
    )
    print(f"Mean normalized RMSE: {err['mean_rmse_norm']:.3f}")
    print(f"Mean raw RMSE (MW): {err['mean_rmse_mw']:.1f}")
    for f, vals in err["per_feature"].items():
        print(f"  {f}: {vals['rmse_mw']:.1f} MW  ({vals['rmse_norm']:.3f} normalized)")

    # ===== Soft validation =====
    total_days = int(reps_df["weight_days"].sum())
    total_hour_weights = int(block_weights["total_hour_weight"].sum())
    expected_hours = 24 * total_days

    print("\nValidation summary:")
    ok_days = total_days in (365, 366)
    print(f"  Sum of representative-day weights: {total_days} " + ("✅" if ok_days else "⚠️"))

    ok_hours = (total_hour_weights == expected_hours)
    print(f"  Sum of total hour weights: {total_hour_weights} (expected {expected_hours}) "
          + ("✅" if ok_hours else "⚠️"))

    if not ok_days:
        print("  ⚠️ Warning: day weights do not sum to 365/366. Check input coverage and date parsing.")
    if not ok_hours:
        print("  ⚠️ Warning: total hour weights ≠ 24 × total_days. Check hour-block construction.")

if __name__ == "__main__":
    main()
