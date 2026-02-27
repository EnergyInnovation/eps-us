import pandas as pd

# === USER SETTINGS ===
input_file = "macc_raw_results_bucketed.csv"      # your bucketed output
output_file = "macc_bucketed_with_EUR.csv"            # combined output

eu_iso3 = [
    "AUT","BEL","BGR","HRV","CYP","CZE","DNK","EST","FIN","FRA",
    "DEU","GRC","HUN","IRL","ITA","LVA","LTU","LUX","MLT","NLD",
    "POL","PRT","ROU","SVK","SVN","ESP","SWE"
]

# Columns in the bucketed file (adjust if yours differs)
key_cols = ["sector", "source", "year", "country_code", "tech_long", "p"]
q_col = "q"

# === LOAD ===
df = pd.read_csv(input_file)

# Ensure numeric q
df[q_col] = pd.to_numeric(df[q_col], errors="coerce")
df = df.dropna(subset=[q_col])

# Tag EU rows as EUR
df.loc[df["country_code"].isin(eu_iso3), "country_code"] = "EUR"

# Re-aggregate (because many EU countries now share the same key)
out = (
    df.groupby(key_cols, as_index=False)[q_col]
      .sum()
      .sort_values(key_cols)
)

# Save
out.to_csv(output_file, index=False)

print("Done.")
print("Rows written:", len(out))
print("Output:", output_file)