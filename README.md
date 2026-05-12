# public-health-analytics-dashboard
Interactive Tableau dashboard analyzing  health disparities across 3,143 US counties using  CDC PLACES 2023, SAMHSA, WHO, NCI and CDC BRFSS data.
# 🏥 Comprehensive Public Health Analytics Dashboard

> Analyzing health disparities across all 3,143 US counties using CDC, SAMHSA, WHO, and NCI data.

![Dashboard Preview](visuals/dashboard.png)

---

## 📌 Project Overview

This interactive Tableau dashboard integrates five government health datasets to reveal geographic health disparities across the United States at the county level — something impossible to see from any single data source alone.

Built as part of Data Visualization · Spring 2026 · San José State University

---

## 🔍 Key Findings

- 🔴 **2x Regional Gap** — Appalachian counties average 17.8% diabetes vs Pacific NW 8.7%
- 📈 **R² = 0.74** — Obesity explains 74% of county-level diabetes variation
- ⚠️ **Repeat Offenders** — AL, MS, WV, KY rank bottom 10 across 4 of 5 conditions
- 📊 **80/20 Rule** — 20% of counties account for 80% of US diabetes burden

---

## 📊 Dashboard Views

| Visual | Description |
|--------|-------------|
| County Choropleth Map | Color-coded map of all 3,143 counties across 5 conditions |
| Top Counties Bar Chart | Ranked worst 20 counties, cross-filtered by state |
| Obesity × Diabetes Scatter | R²=0.74 correlation with trend line |
| State Heatmap | 50 states × 5 conditions severity matrix |
| Health Burden Index | Unified score averaging all 5 conditions per county |
| Outlier Detection Quadrant | 4-quadrant crisis/anomaly/resilient/benchmark analysis |
| Pareto Chart | 80/20 rule — counties driving 80% of diabetes burden |

---

## 🗂️ Data Sources

| Dataset | Agency | Level | Link |
|---------|--------|-------|------|
| PLACES 2023 | CDC | County | [data.cdc.gov](https://data.cdc.gov) |
| NSDUH | SAMHSA | State | [datafiles.samhsa.gov](https://datafiles.samhsa.gov) |
| Global Health Observatory | WHO | National | [who.int/data/gho](https://who.int/data/gho) |
| SEER Program | NCI | Regional | [seer.cancer.gov](https://seer.cancer.gov) |
| BRFSS | CDC | State | [cdc.gov/brfss](https://cdc.gov/brfss) |

---

## 🛠️ How to Reproduce

1. Download all 5 datasets from links above
2. Format `CountyFIPS` column as **text** (not number) to preserve leading zeros
3. Open Tableau Desktop
4. Connect to `data/cleaned/cdc_places_county_clean.csv` as primary source
5. Follow methodology in `docs/methodology.md`
6. Open `ComprehensivePublicHealth.twbx` to view the complete workbook

---

## 🤖 Agentic AI Layer

A Claude AI chat interface is proposed alongside the dashboard allowing users to ask plain English questions about the health data and receive instant data-backed answers — no Tableau expertise required.

---

## 📄 License

MIT License — free to use, share, and build upon with attribution.
