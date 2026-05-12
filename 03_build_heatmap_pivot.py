"""
Step 3 — Build pivoted heatmap dataset for View 4 (5 conditions × 50 states)
Reads cleaned CDC PLACES file (state-level aggregation) and outputs a long table.

Output columns: StateDesc | StateAbbr | Condition | Value
Run after 02_clean_cdc_places.py
"""

import pandas as pd
import os

CLEANED = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned")
src = os.path.join(CLEANED, "cdc_places_county_clean.csv")

print(f"Reading {src} ...")
df = pd.read_csv(src, dtype={"CountyFIPS": str})

# ── Five focal conditions ─────────────────────────────────────────────────────
CONDITION_MAP = {
    "Diabetes":            "Diabetes_AdjPrev",
    "Obesity":             "Obesity_AdjPrev",
    "High Blood Pressure": "BPHIGH_AdjPrev",
    "Mental Health":       "MHLTH_AdjPrev",
    "Sleep <7h":           "SLEEP_AdjPrev",
}

# Keep only columns that actually exist in the file
available = {label: col for label, col in CONDITION_MAP.items() if col in df.columns}
missing   = set(CONDITION_MAP) - set(available)
if missing:
    print(f"  WARNING — columns not found (will be skipped): {missing}")

# ── Aggregate to state level (median across counties) ────────────────────────
state_cols = [c for c in ["StateDesc", "StateAbbr"] if c in df.columns]
agg_cols   = list(available.values())

state_df = (
    df[state_cols + agg_cols]
    .groupby(state_cols, as_index=False)[agg_cols]
    .median()
)

# ── Pivot to long format ──────────────────────────────────────────────────────
long_df = state_df.melt(
    id_vars=state_cols,
    value_vars=agg_cols,
    var_name="ConditionCode",
    value_name="Value",
)

# Map internal column names back to readable labels
inv_map = {v: k for k, v in available.items()}
long_df["Condition"] = long_df["ConditionCode"].map(inv_map)
long_df.drop(columns=["ConditionCode"], inplace=True)

# Round prevalence to 2 decimal places
long_df["Value"] = long_df["Value"].round(2)

print(f"  Heatmap shape: {long_df.shape}  "
      f"({long_df['StateDesc'].nunique()} states × {long_df['Condition'].nunique()} conditions)")

dest = os.path.join(CLEANED, "heatmap_state_conditions.csv")
long_df.to_csv(dest, index=False)
print(f"\nSaved → {dest}")
print("\nPreview:")
print(long_df.head(10).to_string(index=False))
