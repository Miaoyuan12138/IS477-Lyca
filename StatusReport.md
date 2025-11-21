# StatusReport.md

## 1) Plan vs. Progress

During this milestone period, we have made substantial progress on nearly every component of our IS477 group project. Our main objective remains the same: to understand the relationship between unemployment and mental health in the United States across states and over time, using publicly available datasets from the Bureau of Labor Statistics (BLS) and the Centers for Disease Control and Prevention (CDC).

### a. Data acquisition: 

- We have successfully collected two complementary datasets from reliable public sources. 
- The first is the BLS Local Area Unemployment (LAU) dataset, which reports monthly unemployment rates from 1976 to 2022 across all U.S. states and territories. 
- The second is the CDC's Behavioral Risk Factor Surveillance System (BRFSS) dataset, which measures state-level mental health indicators, including the average number of mentally unhealthy days reported by adults. 
- All raw CSV files are stored locally for reproducibility and referenced consistently in our scripts. Standardized copies were created and placed under the data/raw/ directory.

### b. Initial integration: 

- Initial integration between these two datasets is completed. 
- We first converted the BLS unemployment data from monthly to annual averages per state to align the temporal resolution with the BRFSS mental-health data, which is reported yearly. 
- On the mental-health side, we selected an "Overall" indicator called Recent mentally unhealthy days among adults aged 18 years or older (Mean). This variable captures the average number of days in the past 30 days when individuals experienced stress, depression, or emotional problems. It is one of the most representative and continuous indicators of population mental health across states.
- After data cleaning and standardization, both datasets were merged on common fields: State and Year. This produced a unified dataset that allows direct comparison of unemployment rates and mental-health outcomes across 51 regions (the 50 states plus the District of Columbia) for roughly eleven overlapping years (2011–2021).

### c. Profiling and quality checks:

- Profiling and data-quality assessment have been conducted. 
- We verified completeness, identified missing values, and checked overlaps in time and state coverage. 
- Early profiling results indicate minimal missingness (~0.36%) in the mental-health variable and no missing values in the unemployment variable. 
- Coverage across states and years is consistent, with 561 integrated rows after merging.

### d. Automation: 

- Following the project's reproducibility requirement, we designed a reproducible workflow. 
- A Snakemake workflow skeleton and a run_all.sh script were created to automate end-to-end execution. 
- Currently, the scripts run the integration and profiling components automatically; the data-acquisition automation will be completed in the next milestone.

### e. Ethics/licensing: 

- We reviewed and documented licensing for both data sources. 
- Since both datasets were created by U.S. federal agencies, they fall under the U.S. Government Public Domain category. 
- This means they can be freely used, shared, and modified without restriction, as long as proper attribution is provided. 
- There are no personal identifiers in the data, ensuring full compliance with ethical research and privacy standards.


## 2) Current Artifacts
- `data/processed/integrated_state_year.csv` — The merged dataset combining annual unemployment rates with the mean number of mentally unhealthy days per state.
- `docs/quality/missingness.csv` — Summarizes missing values for each variable in the integrated dataset.
- `docs/quality/summary_by_year.csv` — Aggregates national coverage and yearly averages across all states.
- `scripts_acquire_data.py` - Template for data-acquisition automation to be completed next milestone.
- `scripts_integrate.py` - Fully functioning integration script that performs cleaning, aggregation, and merging.
- `scripts_profile_quality.py` - Generates quality reports and summary statistics, can be extended.
- `Snakefile` — Skeleton for an end-to-end Snakemake pipeline, recently introduced in class.
- `requirements.txt` - Lists Python dependencies (pandas, numpy, requests, etc.) for reproducibility.
- `run_all.sh` - Shell script that installs dependencies and executes the full workflow; it will be finalized in the next stage.

## 3) Coverage Summary
- Unemployment (monthly → yearly): years=47 (1976–2022), states=53.
- Mental health (Overall indicator): years≈11 (2011–2021), states≈55.
- Overlap used for integration: years=11 (2011–2021), states=51.
- Integrated rows: 561 (≈ 51 states × 11 years; D.C. included when available).

## 4) Early Data Quality Notes
- Missingness:
  - MH_MeanUnhealthyDays: ~0.36% missing after "Overall" aggregation.
  - UnemploymentRate: 0.00% missing.
  - The low missingness rates indicate good overall data quality. For future steps, we will evaluate whether the missing records cluster in particular states or years and decide whether to impute or exclude them.
- Schema and temporal alignment: We join the two datasets using state names. This works well because both datasets use standard state names. In the future, we may map them to FIPS codes to avoid ambiguity. For time alignment, we solved the issue by taking the average unemployment rate for each year. This matches the BRFSS survey data, which is also reported by year (using the YearStart field).
- Potential bias: The BRFSS data are self-reported and survey-based, meaning responses are subject to sampling error and possible under- or over-reporting biases. To account for this, we plan to incorporate the confidence intervals provided in the dataset (LowConfidenceLimit and HighConfidenceLimit) during the analysis stage to express uncertainty around estimates.

## 5) Ethical/Legal (Module 2)
- Licenses: U.S. Government Public Domain (BLS/CDC). We retain source citations/URLs.
- Privacy: State-level aggregates only — no PII.
- Policy: Respect Kaggle mirrors’ ToS; prefer primary sources (BLS/CDC) for future automated acquisition.

## 6) Updated Timeline & Next Steps
- Nov 17-18: Commit real acquisition scripts (BLS LAU and CDC/BRFSS endpoints or documented mirrors) + SHA-256 checks.
- Nov 22: Finalize Snakemake; `run_all.sh` nad `Snakefile` ready.
- Dec 1: Full quality report (missing/outliers; unit checks).
- Dec 5: Analysis & visualizations; regression/correlation + uncertainty.
- Dec 10: Final release.

## 7) Team Contributions (this milestone)
- Caroline Wen: Data integration (State x Year), initial profiling, data quality file generation, workflow structure.
- Lydia Li: Ethics/licensing write-up, storage/organization plan, documentation (DataDictionary/Ethics/Reproduce).

(Each member will add & commit their own summary in another file: Conribution.md)

## 8) Changes to Project Plan
The core research question—how unemployment correlates with mental-health outcomes—remains unchanged. However, we made several refinements based on new insights and timeline adjustments:

- Timeline adjustment: Because the interim deadline was moved one week later, we reorganized our schedule to better distribute workload across November. This ensures all milestones are achieved with sufficient time for peer review and testing.

- Indicator refinement: After exploring the mental-health dataset, we decided that "Recent mentally unhealthy days among adults aged ≥18 years" is the best main indicator. It has good yearly coverage and is easy to understand. We plan to use "Age-adjusted Mean" as a secondary measure for sensitivity analysis.

- Integration improvement: The join keys have been standardized using consistent state names, and we will later explore mapping to FIPS codes for greater reproducibility.

- Workflow evolution: Initially, we only planned manual processing; now we are transitioning to an automated workflow managed by scripts and reproducible environments. This will allow the whole workflow to be rerun with one command.

- Expanded documentation: Additional files (requirements.txt, Reproduce.md, and quality-summary outputs) were added to enhance transparency.