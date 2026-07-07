import pandas as pd
import numpy as np

# === USER SETTINGS ===
input_file = "macc_raw_results_clean.csv"
bucket_defs_file = "MarginalCostDefinitions.csv"
output_file = "macc_raw_results_bucketed.csv"

chunksize = 2_000_000  # tune for your RAM
key_cols = ["sector", "source", "year", "country_code", "tech_long"]

# Bucket file column names
lower_col = "Lower Bound"
upper_col = "Upper Bound"
rep_col   = "$/ton abated"   # representative p value per bucket

# ============================================================
# LOAD + PREP BUCKET DEFINITIONS
# ============================================================
bdefs = pd.read_csv(bucket_defs_file)

required = [lower_col, upper_col, rep_col]
missing = [c for c in required if c not in bdefs.columns]
if missing:
    raise ValueError(f"Bucket file missing columns: {missing}. Found: {list(bdefs.columns)}")

bdefs["Lower"] = pd.to_numeric(bdefs[lower_col], errors="coerce").fillna(-np.inf)
bdefs["Upper"] = pd.to_numeric(bdefs[upper_col], errors="coerce").fillna(np.inf)
bdefs["p_bucket_value"] = pd.to_numeric(bdefs[rep_col], errors="coerce")

# Sort and assign stable bucket_id
bdefs = bdefs.sort_values(["Lower", "Upper"]).reset_index(drop=True)
bdefs["bucket_id"] = np.arange(len(bdefs), dtype=np.int32)

# ------------------------------------------------------------
# Pick which bucket should receive p == 0 ("middle bucket")
# Priority:
#   1) explicit [0,0] bucket if present
#   2) any bucket that spans 0 (Lower < 0 < Upper)  -> choose narrowest
#   3) bucket that starts at 0 and goes positive (Lower == 0 < Upper) -> choose narrowest
#   4) bucket that ends at 0 from negative side (Lower < 0 == Upper)  -> choose narrowest
# ------------------------------------------------------------
zero_candidates = bdefs[(bdefs["Lower"] == 0) & (bdefs["Upper"] == 0)]
if len(zero_candidates) == 1:
    zero_bucket_id = int(zero_candidates["bucket_id"].iloc[0])
elif len(zero_candidates) > 1:
    raise ValueError("Multiple [0,0] buckets found in bucket definitions. Please make it unique.")
else:
    spans_zero = bdefs[(bdefs["Lower"] < 0) & (bdefs["Upper"] > 0)]
    if not spans_zero.empty:
        spans_zero = spans_zero.assign(width=spans_zero["Upper"] - spans_zero["Lower"])
        zero_bucket_id = int(spans_zero.sort_values("width").iloc[0]["bucket_id"])
    else:
        starts_at_zero = bdefs[(bdefs["Lower"] == 0) & (bdefs["Upper"] > 0)]
        if not starts_at_zero.empty:
            starts_at_zero = starts_at_zero.assign(width=starts_at_zero["Upper"] - starts_at_zero["Lower"])
            zero_bucket_id = int(starts_at_zero.sort_values("width").iloc[0]["bucket_id"])
        else:
            ends_at_zero = bdefs[(bdefs["Lower"] < 0) & (bdefs["Upper"] == 0)]
            if not ends_at_zero.empty:
                ends_at_zero = ends_at_zero.assign(width=ends_at_zero["Upper"] - ends_at_zero["Lower"])
                zero_bucket_id = int(ends_at_zero.sort_values("width").iloc[0]["bucket_id"])
            else:
                raise ValueError(
                    "Could not identify a 'middle bucket' for p==0 from your bucket definitions.\n"
                    "Expected one of: [0,0], a bucket spanning 0, a bucket starting at 0, or a bucket ending at 0."
                )

# ------------------------------------------------------------
# Build IntervalIndex for NON-ZERO-WIDTH buckets only
# We'll bucket nonzero p values using [Lower, Upper) (closed left),
# then override p==0 -> zero_bucket_id.
# ------------------------------------------------------------
nonzero_width = bdefs[bdefs["Lower"] < bdefs["Upper"]].copy()

intervals = pd.IntervalIndex.from_arrays(
    nonzero_width["Lower"].to_numpy(),
    nonzero_width["Upper"].to_numpy(),
    closed="left"   # [Lower, Upper)
)

# If your definitions truly overlap (not just touch), that's ambiguous
if intervals.is_overlapping:
    raise ValueError(
        "Bucket intervals overlap (beyond touching). Fix MarginalCostDefinitions.csv to be non-overlapping."
    )

# Map IntervalIndex position -> bucket_id in the original bdefs table
pos_to_bucket_id = nonzero_width["bucket_id"].to_numpy(dtype=np.int32)

print("Zero values will be forced into bucket_id:", zero_bucket_id)

# ============================================================
# STREAM + AGGREGATE
# ============================================================
acc = {}  # (keys..., bucket_id) -> q_sum
use_cols = key_cols + ["p", "q"]

for chunk in pd.read_csv(input_file, usecols=use_cols, chunksize=chunksize):
    chunk["p"] = pd.to_numeric(chunk["p"], errors="coerce")
    chunk["q"] = pd.to_numeric(chunk["q"], errors="coerce")
    chunk = chunk.dropna(subset=["p", "q"])

    pvals = chunk["p"].to_numpy()
    qvals = chunk["q"].to_numpy()

    # Bucket nonzero values via IntervalIndex
    idx = intervals.get_indexer(pvals)  # positions in IntervalIndex, or -1
    bucket_id = np.full_like(idx, fill_value=-1, dtype=np.int32)

    # Nonzero -> normal bucketing
    ok = idx != -1
    bucket_id[ok] = pos_to_bucket_id[idx[ok]]

    # Force exact zeros into the chosen middle bucket
    bucket_id[pvals == 0] = zero_bucket_id

    # Drop rows that still didn't match any bucket (if bucket file doesn't cover full range)
    keep = bucket_id != -1
    if not np.all(keep):
        chunk = chunk.iloc[np.where(keep)[0]].copy()
        bucket_id = bucket_id[keep]
        qvals = qvals[keep]

    chunk["bucket_id"] = bucket_id

    # Aggregate within chunk
    gcols = key_cols + ["bucket_id"]
    chunk_agg = chunk.groupby(gcols, sort=False, observed=True)["q"].sum().reset_index()

    # Accumulate
    for row in chunk_agg.itertuples(index=False):
        k = tuple(row[:-1])  # keys + bucket_id
        acc[k] = acc.get(k, 0.0) + float(row[-1])

# ============================================================
# BUILD OUTPUT
# ============================================================
out = pd.DataFrame(
    [(k[0], k[1], k[2], k[3], k[4], int(k[5]), float(v)) for k, v in acc.items()],
    columns=key_cols + ["bucket_id", "q_sum"]
)

# Attach only representative p value
bucket_meta = bdefs[["bucket_id", "p_bucket_value"]].copy()
out = out.merge(bucket_meta, on="bucket_id", how="left")

# Rename columns
out = out.rename(columns={
    "p_bucket_value": "p",
    "q_sum": "q"
})

# Keep only desired columns
out = out[key_cols + ["p", "q"]]

# Sort nicely
out = out.sort_values(key_cols + ["p"]).reset_index(drop=True)

# Save
out.to_csv(output_file, index=False)

print("Done.")
print("Rows written:", len(out))
print("Output:", output_file)