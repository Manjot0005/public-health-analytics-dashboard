"""
Step 2 — Clean CDC PLACES county file → data/cleaned/cdc_places_county_clean.csv
The raw file is long-format (one row per measure). This script filters for the
5 focal conditions, takes age-adjusted prevalence, and pivots to wide format:
  one row per county × one column per condition.
"""

import pandas as pd
import os

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned")
os.makedirs(OUT, exist_ok=True)

# Five focal conditions (MeasureId → clean label)
CONDITIONS = {
    "DIABETES": "Diabetes_AdjPrev",
    "OBESITY":  "Obesity_AdjPrev",
    "BPHIGH":   "BPHIGH_AdjPrev",
    "MHLTH":    "MHLTH_AdjPrev",
    "SLEEP":    "SLEEP_AdjPrev",
}

src = os.path.join(RAW, "cdc_places_county.csv")
print(f"Reading {src} ...")
df = pd.read_csv(src, dtype={"LocationID": str})
print(f"  Raw shape: {df.shape}")

# Filter: age-adjusted only + our 5 conditions
df = df[
    (df["DataValueTypeID"] == "AgeAdjPrv") &
    (df["MeasureId"].isin(CONDITIONS))
].copy()
print(f"  After filter: {df.shape}")

# Pad FIPS to 5 digits
df["LocationID"] = df["LocationID"].str.zfill(5)

# Cast prevalence to float
df["Data_Value"] = pd.to_numeric(df["Data_Value"], errors="coerce")

# Pivot to wide: one row per county
id_vars = ["LocationID", "StateAbbr", "StateDesc", "LocationName"]
wide = df.pivot_table(
    index=id_vars,
    columns="MeasureId",
    values="Data_Value",
    aggfunc="mean",   # there should be one row per county per measure
).reset_index()

# Flatten MultiIndex columns (pivot_table creates them)
wide.columns.name = None

# Rename condition columns
wide.rename(columns={k: v for k, v in CONDITIONS.items() if k in wide.columns}, inplace=True)

# Rename FIPS for Tableau
wide.rename(columns={"LocationID": "CountyFIPS"}, inplace=True)

print(f"  Wide shape: {wide.shape}")
print(f"  Unique counties: {wide['CountyFIPS'].nunique()}")

dest = os.path.join(OUT, "cdc_places_county_clean.csv")
wide.to_csv(dest, index=False)
print(f"\nSaved → {dest}")
print("\nColumns:")
for c in wide.columns:
    print(f"  {c}")
print("\nPreview:")
print(wide.head(3).to_string(index=False))
