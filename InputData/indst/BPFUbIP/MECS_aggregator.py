# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 11:24:25 2026

@author: DanO'Brien
"""

import pandas as pd

# --- INPUT / OUTPUT ---
INFILE  = "Table5_2.xlsx"
OUTFILE = "Table5_2_long.csv"

# --- READ ---
df = pd.read_excel(INFILE, header=11)

# --- STANDARDIZE COLUMN NAMES ---
df = df.iloc[:, :10].copy()

df.columns = [
    "NAICS",
    "EndUse",
    "Total",
    "Net_electricity",
    "Residual_fuel_oil",
    "Distillate_and_diesel",
    "Natural_gas",
    "HGL",
    "Coal",
    "Other",
]

# --- FILL DOWN NAICS CODES ---
df["NAICS"] = df["NAICS"].ffill()

# --- DROP NON-DATA ROWS ---
df = df[df["EndUse"].notna()].copy()

# --- WIDE -> LONG ---
df_long = df.melt(
    id_vars=["NAICS", "EndUse"],
    value_vars=df.columns[2:],
    var_name="Fuel",
    value_name="Consumption"
)

# --- FIX TEXT ENCODING + WHITESPACE ---
def fix_mojibake(x):
    if not isinstance(x, str):
        return x
    try:
        return x.encode("cp1252").decode("utf-8")
    except Exception:
        return (x.replace("â€”", "—")
                 .replace("â€“", "–")
                 .replace("â€˜", "‘")
                 .replace("â€™", "’")
                 .replace("â€œ", "“")
                 .replace("â€�", "”"))

df_long["EndUse"] = (
    df_long["EndUse"]
        .map(fix_mojibake)
        .astype(str)
        .str.replace("\u00A0", " ", regex=False)
        .str.strip()
)

# --- CLEAN CONSUMPTION FIELD (KEEP SYMBOLS) ---
df_long["Consumption"] = df_long["Consumption"].astype(str).str.strip()

# --- EXTRACT NUMERIC NAICS CODE ---
df_long["NAICS_code"] = df_long["NAICS"].astype(str).str.extract(r"(\d{3})")

# --- DROP TRULY EMPTY ROWS ---
df_long = df_long[df_long["Consumption"] != "nan"].reset_index(drop=True)

# --- SAVE (EXCEL-SAFE UTF-8) ---
df_long.to_csv(OUTFILE, index=False, encoding="utf-8-sig")

print(f"Saved long-format data to: {OUTFILE}")
print(df_long.head(10))
