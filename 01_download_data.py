"""
Step 1 — Download all 5 raw datasets into data/raw/
Run: python scripts/01_download_data.py
"""

import urllib.request
import os

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW, exist_ok=True)

SOURCES = {
    # CDC PLACES 2024 release (county-level, ~3143 rows)
    "cdc_places_county.csv": (
        "https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD"
    ),
    # CDC BRFSS Sleep module (state-level)
    "cdc_brfss_sleep.csv": (
        "https://data.cdc.gov/api/views/eqbn-8mpz/rows.csv?accessType=DOWNLOAD"
    ),
}

for filename, url in SOURCES.items():
    dest = os.path.join(RAW, filename)
    if os.path.exists(dest):
        print(f"  SKIP (already exists): {filename}")
        continue
    print(f"  Downloading {filename} ...")
    try:
        urllib.request.urlretrieve(url, dest)
        size = os.path.getsize(dest) // 1024
        print(f"  OK — {size} KB saved to data/raw/{filename}")
    except Exception as e:
        print(f"  FAILED: {e}")
        print(f"  → Download manually and save to: data/raw/{filename}")

print("\nManual downloads required (APIs need registration):")
print("  SAMHSA NSDUH  → https://www.samhsa.gov/data/nsduh/reports-detailed-tables")
print("    Save as: data/raw/samhsa_mental_health.csv")
print("  NCI SEER      → https://seer.cancer.gov/statistics-network/explorer/")
print("    Save as: data/raw/nci_cancer_screening.csv")
print("  WHO GHO       → https://www.who.int/data/gho/data/themes/cardiovascular-diseases")
print("    Save as: data/raw/who_cardiovascular.csv")
