import pandas as pd

# === USER SETTINGS ===
input_file = "macc_raw_results.csv"
output_file = "macc_raw_results_clean.csv"

countries_to_keep = [
    "USA",
    "KOR",
    "CHN",
    "IND",
    "IDN",
    "CAN",
    "MEX",
    "AUS",
    "JPN",
    "ZAF",
    "AUT",
    "BEL",
    "BGR",
    "CYP",
    "CZE",
    "DEU",
    "DNK",
    "ESP",
    "EST",
    "FIN",
    "FRA",
    "GRC",
    "HRV",
    "HUN",
    "IRL",
    "ITA",
    "LTU",
    "LUX",
    "LVA",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "SWE",
]

# === LOAD DATA ===
df = pd.read_csv(input_file)

# ============================================================
# 1) Remove rows where year > 2080
# ============================================================
df = df[df["year"] <= 2080]

# ============================================================
# 2) Keep only specified countries (using country_code)
# ============================================================
df = df[df["country_code"].isin(countries_to_keep)]

# ============================================================
# 3) Sort by sector, source, year, country
# ============================================================
df = df.sort_values(by=["sector", "source", "year", "country"])

# ============================================================
# 4) Capture unique sector-source-tech combinations
# ============================================================
unique_techs = (
    df[["sector", "source", "tech_long"]]
    .drop_duplicates()
    .sort_values(by=["sector", "source", "tech_long"])
)

print("\nUnique sector / source / tech_long combinations:")
for _, row in unique_techs.iterrows():
    print(f"{row['sector']} | {row['source']} | {row['tech_long']}")

# ============================================================
# 5) Delete "country" column but keep "country_code"
# ============================================================
df = df.drop(columns=["country"])

# === SAVE RESULT ===
df.to_csv(output_file, index=False)

print("\nProcessing complete.")
print("Remaining rows:", len(df))
print("Unique tech combinations:", len(unique_techs))