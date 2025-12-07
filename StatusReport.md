# StatusReport.md
**IS477 – Milestone 3 Status Report** 

## 1) Plan vs. Progress

Following feedback from the teaching staff, our team shifted from Kaggle-based inputs to an **independently integrated dataset built entirely from CDC open data sources**. Our revised project now combines:

1. **ACS Active Commuting Data**  
   *Source:* CDC DNPAO → “Percent of adults who walk or bike to work”  
   *Dataset ID:* 8mrp-rmkw

2. **BRFSS Obesity Prevalence**  
   *Source:* CDC BRFSS  
   *Dataset ID:* hn4x-zwk7  
   *Metric:* Percent of adults aged ≥18 who have obesity

3. **Policy & Environmental Indicators**  
   *Source:* CDC Nutrition, Physical Activity, and Obesity – Policy and Environmental Data  
   *Dataset ID:* k8w5-7ju6  
   *Metric:* Baby Friendly Hospital Initiative adoption rate (% of births at BFHI-certified facilities)

Compared to the updated project plan (CDC obesity + ACS active commuting + policy data), our current status is:

### **1. Data Acquisition — Completed**

Script: `scripts/scripts_acquire_data.py`  
The script downloads the datasets using API URLs and saves:

- `data/raw/acs_active_commute_raw.csv`
- `data/raw/brfss_obesity_raw.csv`
- `data/raw/policy_env_raw.csv`

Each file includes:
- Logged API URL  
- SHA-256 digest  
- Local save path  

This ensures reproducibility and provenance.

---

### **2. Data Integration — Completed**

Script: `scripts/scripts_integrate.py`  
Processes:
- Clean and standardize column names  
- Extract state/year  
- Aggregate where necessary  
- Left-join into unified **state-year table**  

Output:  
`data/processed/integrated_state_year.csv` (550 rows)

---

### **3. Data Quality Profiling — Completed**

Script: `scripts/scripts_profile_quality.py`

Outputs:
- `docs/quality/missingness.csv`
- `docs/quality/summary_by_year.csv`

Findings:
- ACS and BRFSS nearly complete across years  
- Policy indicators sparse before 2011  
- No critical gaps affecting analysis  
- Minor categorical inconsistencies normalized

---

### **4. Visualization & Analysis — Completed**

Script: `scripts/scripts_analyze.py`  
Output figure:  
`docs/figures/obesity_vs_active_commute.png`

**Interpretation:**
- Clear **negative association** between active commuting and obesity prevalence  
- Relationship stable across 2011–2021  
- High state-level variability suggests influence of infrastructure, policies, and built environment

Visualization successfully reproduces known public-health patterns.

---

### **Automation**

A **Snakemake workflow** in `Snakefile` orchestrates:

1. `acquire_data` → fetch raw CSVs.
2. `integrate` → build `integrated_state_year.csv`.
3. `profile_quality` → generate quality reports.
4. `analyze` → (placeholder) generate figures/analysis outputs.

`run_all.sh` provides a single entry point to run the full workflow from a clean environment.

---

### **Ethics/licensing**
- Verified that all three datasets are public and licensed under ODbL or equivalent open-data terms on Data.gov/Healthdata.gov.
- Documented licensing and attribution in `README.md` (to be finalized) and comments in `scripts_acquire_data.py`.

---


## 2) Current Artifacts

### **Data Files**

- `data/raw/acs_active_commute_raw.csv`
- `data/raw/brfss_obesity_raw.csv`
- `data/raw/policy_env_raw.csv`
- `data/processed/integrated_state_year.csv`

### **Quality Reports**

- `docs/quality/missingness.csv`
- `docs/quality/summary_by_year.csv`

### **Visualization**

- `docs/figures/obesity_vs_active_commute.png`

### **Scripts**

- `scripts_acquire_data.py`
- `scripts_integrate.py`
- `scripts_profile_quality.py`
- `scripts_analyze.py`
- `Snakefile`
- `requirements.txt`
- `run_all.sh`

---

## 3) Coverage Summary

Based on `summary_by_year.csv` and inspection of `integrated_state_year.csv`:

- **Temporal coverage**
  - The integrated dataset currently includes **2011–2019 and 2021** (there is no 2020 row in `summary_by_year.csv`).
  - For each of these 10 years, we have state-level observations for essentially all U.S. states plus D.C. and selected territories.

- **ACS active commuting (`active_commute_pct`)**
  - Years covered in the integrated data: **2011–2019, 2021**.
  - Average active commuting across states is around **3–4%**, with a slight downward trend over time (e.g., ~3.75% in 2011 vs. ~2.86% in 2021).

- **BRFSS obesity (`obesity_pct`)**
  - Years covered: **2011–2019, 2021**.
  - State-level averages show a clear upward trend over time (e.g., ~27.6% in 2011 up to ~33.5% in 2021).

- **Policy indicator (`baby_friendly_pct`)**
  - Years covered: **2011–2019, 2021**.
  - This variable captures the percentage of live births in “baby-friendly” facilities for each state-year.
  - The average across states rises sharply over time (from ~4.4% in 2011 to ~28.3% in 2021), indicating substantial policy/environmental change.

- **Integrated dataset**
  - Integrated rows: **550**, which is consistent with ~55 jurisdictions (states, D.C., and a few territories when available) × 10 years.
  - Each row represents a **single state-year** with aligned values for active commuting, obesity, and the baby-friendly policy indicator.

---

## 4) Early Data Quality Notes

- **Missingness (from `missingness.csv`)**
  - `active_commute_pct`: **3.64%** missing.
  - `obesity_pct`: **2.73%** missing.
  - `baby_friendly_pct`: **3.45%** missing.
  - `Year`, `State`, `year`, and `state` have **0% missing**, so every row has a well-defined state-year key.
  - Overall, missingness is **low and in the low single-digit range**, which is acceptable for exploratory analysis. In later work, we can:
    - Check whether missing values cluster in particular states or years.
    - Decide whether to impute, drop affected rows, or model missingness explicitly.

- **Schema and temporal alignment**
  - Each source uses its own naming scheme (`LocationAbbr`, `LocationDesc`, `YearStart`, etc.). The integration script harmonizes these into:
    - `state` – two-letter state (or territory) abbreviation.
    - `year` – integer year (from `YearStart` or equivalent).
  - Policy rows with multiple records per state-year were aggregated (mean) so that the final integrated table has **one row per state-year**.
  - The absence of a 2020 row in `summary_by_year.csv` means we currently analyze **2011–2019 and 2021** as a continuous-but-gapped time series; we explicitly note that gap in the report.

- **Potential bias and uncertainty**
  - BRFSS obesity measures are **self-reported** survey data and thus subject to:
    - Sampling error.
    - Under-/over-reporting of weight and height.
  - ACS active commuting estimates are also survey-based and can have higher variance in small states or territories.
  - The baby-friendly indicator reflects **policy adoption and hospital designation**, which may differ from actual practice “on the ground”.
  - Confidence intervals and metadata fields (where available) are preserved in the intermediate data and can be used in future extensions to quantify uncertainty around state-year estimates.

---

## 5) Ethical / Legal (Module 2)

- **Licenses and terms of use**
  - All three datasets (ACS active commuting, BRFSS obesity, and baby-friendly policy indicators) are sourced from **U.S. federal agencies** (CDC / HHS) via `data.cdc.gov`.
  - These data are released under **U.S. Government open data** terms (public domain / ODC-ODbL-style), and we:
    - Cite the original API endpoints and dataset titles in the report.
    - Do not impose any additional restrictive license on the integrated outputs.

- **Privacy and confidentiality**
  - All data are **aggregated at the state-year level**.
  - There is **no individual-level information or direct identifiers**, so the risk of re-identification is minimal.
  - We do not attempt to link these aggregates to any microdata or external personally identifiable datasets.

- **Policy and responsible use**
  - We prioritize **primary sources** (CDC/HHS) over third-party mirrors.
  - Any future reuse of this project should:
    - Respect updated terms of use and citation guidelines for each dataset.
    - Avoid over-interpreting the results as causal; they are observational aggregates.
  - Our documentation clearly describes the sources, transformations, and limitations so that downstream users can evaluate fitness-for-use in their own contexts.

---

## 6) Updated Timeline & Next Steps
- Nov 17-18: Commit real acquisition scripts (BLS LAU and CDC/BRFSS endpoints or documented mirrors) + SHA-256 checks.
- Nov 22: Finalize Snakemake; `run_all.sh` nad `Snakefile` ready.
- Dec 1: Full quality report (missing/outliers; unit checks).
- Dec 5: Analysis & visualizations; regression/correlation + uncertainty.
- Dec 10: Final release.

---

## 7) Team Contributions (this milestone)
- Caroline Wen: Data integration (State x Year), initial profiling, data quality file generation, workflow structure.
- Lydia Li: Ethics/licensing write-up, storage/organization plan, documentation (DataDictionary/Ethics/Reproduce).

(Each member will add & commit their own summary in another file: Conribution.md)

---

## 8) Changes to Project Plan
The core research question—how unemployment correlates with mental-health outcomes—remains unchanged. However, we made several refinements based on new insights and timeline adjustments:

- Timeline adjustment: Because the interim deadline was moved one week later, we reorganized our schedule to better distribute workload across November. This ensures all milestones are achieved with sufficient time for peer review and testing.

- Indicator refinement: After exploring the mental-health dataset, we decided that "Recent mentally unhealthy days among adults aged ≥18 years" is the best main indicator. It has good yearly coverage and is easy to understand. We plan to use "Age-adjusted Mean" as a secondary measure for sensitivity analysis.

- Integration improvement: The join keys have been standardized using consistent state names, and we will later explore mapping to FIPS codes for greater reproducibility.

- Workflow evolution: Initially, we only planned manual processing; now we are transitioning to an automated workflow managed by scripts and reproducible environments. This will allow the whole workflow to be rerun with one command.

- Expanded documentation: Additional files (requirements.txt, Reproduce.md, and quality-summary outputs) were added to enhance transparency.

- ACS dataset replaced with the validated CDC-hosted version due to corrupted HHS CSV.

- Policy dataset filtered to indicators with numeric values relevant to health-supportive environments.

- Improved workflow using Snakemake to ensure reproducibility.