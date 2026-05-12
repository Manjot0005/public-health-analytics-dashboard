"""
Step 4 — Quick validation before opening Tableau.
Checks row counts, FIPS format, null rates, and value ranges.
Run after 02 and 03.
"""

import pandas as pd
import os

CLEANED = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned")

def check(path, fips_col=None):
    if not os.path.exists(path):
        print(f"  MISSING: {path}")
        return
    df = pd.read_csv(path, dtype={fips_col: str} if fips_col else None)
    print(f"\n{'='*60}")
    print(f"File : {os.path.basename(path)}")
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    if fips_col and fips_col in df.columns:
        bad = df[fips_col].dropna()
        wrong_len = bad[bad.str.len() != 5]
        print(f"FIPS : {bad.nunique()} unique | {len(wrong_len)} with wrong length (expect 0)")
        if len(wrong_len):
            print(f"  Example bad FIPS: {wrong_len.head(3).tolist()}")

    num_cols = df.select_dtypes("number").columns.tolist()
    if num_cols:
        print("Numeric column ranges:")
        for c in num_cols[:8]:
            s = df[c].dropna()
            nulls = df[c].isna().sum()
            print(f"  {c:35s}  min={s.min():.1f}  max={s.max():.1f}  nulls={nulls}")

check(os.path.join(CLEANED, "cdc_places_county_clean.csv"), fips_col="CountyFIPS")
check(os.path.join(CLEANED, "heatmap_state_conditions.csv"))

print("\n\nValidation complete. If no errors above, data is ready for Tableau.")
