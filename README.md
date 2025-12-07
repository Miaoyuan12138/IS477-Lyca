# Active Commuting, Obesity, and Baby-Friendly Policy: An Integrated State-Year Profile

## Contributors

- Caroline Wen 
- Lydia Li

---

## Summary

This project builds an end-to-end, reproducible workflow to study how **active commuting to work** and **baby-friendly hospital policies** relate to **adult obesity** at the U.S. state level. Using three publicly available datasets from the U.S. Centers for Disease Control and Prevention (CDC) and the Department of Health & Human Services (HHS), we construct an integrated **state–year** dataset covering **2011–2019 and 2021**.

The motivating questions are:

1. How have **active commuting rates** and **adult obesity prevalence** changed over time across U.S. states?
2. Is there a detectable **association** between the share of adults who walk/bike to work and state-level obesity percentages?
3. How does the **expansion of baby-friendly hospital designations** co-evolve with these behavioral and health indicators?

To answer these questions, the project:

- Programmatically acquires three datasets via **CDC APIs** using a Python script (`scripts_acquire_data.py`).
- Cleans and integrates them into a unified table (`integrated_state_year.csv`) using `scripts_integrate.py`.
- Profiles data quality and missingness (`scripts_profile_quality.py`), and generates summary tables (`missingness.csv`, `summary_by_year.csv`).
- Automates the entire pipeline via a **Snakemake** workflow (`Snakefile`) orchestrated by `run_all.sh`.
- Produces a simple exploratory visualization (`obesity_vs_active_commute.png`) showing the relationship between active commuting and obesity, colored by year.

The resulting workflow is designed to be **reproducible and transparent**:

- All transformations are captured in version-controlled scripts.
- Dependencies are specified in `requirements.txt`.
- A single command (`bash run_all.sh`) re-runs the full pipeline from data acquisition through analysis.

---

## Data Profile

### Overview of Datasets

The project uses **three** distinct datasets, all from CDC/HHS:

1. **ACS Active Commuting (Nutrition, Physical Activity, and Obesity – American Community Survey)**  
   - Source: CDC / HHS, `data.cdc.gov` (API ID: `8mrp-rmkw`).  
   - Content: State-level percent of adults who **walk or bike to work**, derived from the American Community Survey (ACS).  
   - Key fields after cleaning:
     - `state` – two-letter state (or territory) abbreviation.
     - `year` – integer year (derived from ACS year fields).
     - `active_commute_pct` – percentage of adults who report walking or biking to work.

2. **BRFSS Obesity (Behavioral Risk Factor Surveillance System)**  
   - Source: CDC, `data.cdc.gov` (API ID: `hn4x-zwk7`).  
   - Content: State-level **obesity prevalence** for adults aged 18+ based on BMI ≥ 30, from BRFSS survey data.  
   - Key fields after filtering:
     - Restriction to **state-level “Overall” rows** (all sexes, all races/ethnicities, and “Total” stratification).
     - `state` – two-letter state abbreviation.
     - `year` – integer `YearStart`.
     - `obesity_pct` – percentage of adults with obesity.
     - Additional interval fields (low/high confidence limits) are preserved in intermediate artifacts but not all are carried into the final integrated table.

3. **Baby-Friendly Policy Indicator (Breastfeeding – Environmental or Policy Supports)**  
   - Source: CDC, `data.cdc.gov` (API ID: `k8w5-7ju6`).  
   - Content: Percent of live births occurring at facilities designated as “baby-friendly” under the Baby Friendly Hospital Initiative (BFHI), at the state level.  
   - Key fields:
     - `state` – two-letter state abbreviation.
     - `year` – `YearStart` for the indicator.
     - `baby_friendly_pct` – percentage of live births occurring in BFHI-designated facilities.

### Access Methods and Formats

- All three datasets are accessed via **HTTP CSV endpoints** exposed by `data.cdc.gov`.  
- The project uses a dedicated acquisition script:

  - `scripts_acquire_data.py`  
    - Downloads the CSVs from the CDC endpoints.
    - Writes them to `data/raw/` with fixed filenames:
      - `acs_active_commute_raw.csv`
      - `brfss_obesity_raw.csv`
      - `policy_env_raw.csv`

- The datasets are stored as **tabular CSV files** and kept under `data/raw/` (input) and `data/processed/` (output).

### Ethical / Legal Considerations

- All datasets are **public U.S. Government data** and are effectively in the public domain (open-data license / ODC-ODbL-equivalent).
- The project:
  - Uses only **aggregated state-level data**; no personally identifiable information (PII) is present.
  - Clearly cites the original API endpoints and dataset titles in the References section.
  - Avoids redistributing proprietary data; all inputs can be re-downloaded from official sources.

---

## Data Quality

### Integrated Schema

The final integrated file, `data/processed/integrated_state_year.csv`, has one row per **state-year** and includes the following key fields:

- `state` – two-letter state (or territory) abbreviation.
- `year` – integer year.
- `active_commute_pct` – ACS-derived percent walking/biking to work.
- `obesity_pct` – BRFSS-derived adult obesity percent.
- `baby_friendly_pct` – percent of live births in BFHI-designated facilities.
- Additional helper columns (e.g., `Year`, `State`) that preserve original labels.

### Temporal and Spatial Coverage

From `docs/quality/summary_by_year.csv`:

- Years represented: **2011–2019 and 2021** (no 2020 row appears in the current integrated output).
- For each year in this range:
  - We typically have ~55 jurisdictions per year (50 states, D.C., and selected territories), leading to **550 total integrated rows**.

Average values across states by year (illustrative):

- **Active commuting (`active_commute_pct`)**
  - ~3.75% in 2011 → ~2.86% in 2021 (gradual decline).
- **Obesity (`obesity_pct`)**
  - ~27.6% in 2011 → ~33.5% in 2021 (steady increase).
- **Baby-friendly births (`baby_friendly_pct`)**
  - ~4.4% in 2011 → ~28.3% in 2021 (sharp growth in BFHI coverage).

### Missingness

From `docs/quality/missingness.csv`:

- `Year`, `State`, `year`, `state`: **0.0% missing**.
- `active_commute_pct`: **3.64% missing**.
- `obesity_pct`: **2.73% missing**.
- `baby_friendly_pct`: **3.45% missing**.

Interpretation:

- All key identifiers (state and year) are complete, ensuring a well-defined state-year key.
- The three main quantitative indicators have **low single-digit missingness**, which is acceptable for exploratory analysis and simple models.
- Future work can investigate whether missingness is concentrated in specific states or years and choose either:
  - Dropping those rows, or
  - Imputing plausible values (e.g., interpolation across neighboring years or states).

### Cleaning and Integration Steps

Key transformations in `scripts_integrate.py` include:

1. **Filtering to relevant rows**  
   - BRFSS: restrict to adult obesity, state-level, “Total” or “Overall” categories.
   - Policy data: restrict to BFHI-related indicator (“Percent of live births occurring at facilities designated as baby-friendly”).

2. **Harmonizing keys**
   - Convert state fields to a common `state` abbreviation (e.g., `AL`, `CA`).
   - Extract or compute `year` consistently from `YearStart`/ACS year fields.

3. **Aggregation**
   - For policy rows with multiple records per state-year, aggregate (`mean`) so that each state-year appears only once.
   - For ACS and BRFSS, aggregate or select state-level rows so that the final integrated table has **one record per state-year**.

4. **Merging**
   - Merge the three cleaned tables on `(state, year)` to produce `data/processed/integrated_state_year.csv`.

These steps are fully scripted and therefore reproducible.

---

## Findings

This project focuses on **descriptive** rather than causal analysis. The main findings are:

1. **Obesity rates are rising over time.**  
   - The average state-level obesity percentage increases from around **27–28% in 2011** to over **33% by 2021**.
   - This pattern is visible both in `docs/quality/summary_by_year.csv` and in `docs/figures/obesity_vs_active_commute.png`, where later years cluster at higher obesity levels.

2. **Active commuting is relatively rare and slowly declining.**  
   - ACS data show that only about **3–4%** of adults walk or bike to work on average across states.
   - Over time, this percentage drifts downward, especially by 2021.

3. **Baby-friendly hospital policies have expanded sharply.**  
   - The average percentage of live births in BFHI-designated facilities rises from ~4–5% (2011) to nearly **30%** (2021).
   - This indicates substantial growth in policy adoption and hospital accreditation over the decade.

4. **Cross-sectional association between active commuting and obesity.**  
   - In `obesity_vs_active_commute.png`, each point is a state-year. Roughly:
     - States with **higher active commuting** tend to appear at **slightly lower obesity percentages**.
     - However, there is considerable spread, and the association is modest.

Because this project’s primary goal is to demonstrate **data integration, workflow automation, and reproducibility**, we do not fit formal statistical models (e.g., regressions) here. The scatterplot and summary statistics are sufficient to show how an integrated state-year dataset can support more advanced analysis in future work.

---

## Future Work

Several extensions could deepen both the methodological and substantive contributions:

1. **Richer modeling**
   - Fit multi-level or panel regression models to quantify the relationship between active commuting, baby-friendly policies, and obesity while controlling for:
     - Socioeconomic indicators.
     - Urbanization or population density.
     - Demographic composition.

2. **Expanding the data profile**
   - Add additional CDC or Census variables:
     - Physical activity guidelines adherence.
     - Dietary indicators (e.g., fruit/vegetable intake).
     - Income or education distributions.

3. **Uncertainty-aware analysis**
   - Incorporate BRFSS confidence intervals (low/high bounds) and ACS margins of error.
   - Use simulation or Bayesian models to propagate survey uncertainty into downstream estimates.

4. **Handling the 2020 gap**
   - Investigate why 2020 is missing in the current integrated output.
   - If 2020 data are available from the underlying APIs, extend the acquisition and integration scripts to include that year.

5. **Improved visualization and dashboards**
   - Build interactive dashboards (e.g., with Altair, Plotly, or a simple web app) that:
     - Allow filtering by state and year.
     - Show time-series for active commuting, obesity, and baby-friendly coverage.
     - Provide simple download options for researchers and policymakers.

6. **Reproducible packaging**
   - Containerize the project (e.g., with a `Dockerfile`) so that it can run identically on any machine.
   - Publish an archival snapshot (e.g., via Zenodo) with a DOI, as suggested by the course rubric.

---

## Reproducing This Project

### Prerequisites

- Python 3.11 (or compatible).
- Git.
- (Optional) Bash shell environment (Linux/macOS or WSL on Windows).

### Step-by-Step Instructions

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>.git
   cd <your-repo-name>
   ```

2. **(Recommended) Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the full pipeline**

   ```bash
   bash run_all.sh
   ```

This will:
    - Install any remaining dependencies (idempotent).
    - Download raw datasets into `data/raw/`.
    - Clean and integrate them into `data/processed/integrated_state_year.csv`.
    - Profile data quality and generate summary tables in `docs/quality/`.
    - Produce the exploratory scatterplot `obesity_vs_active_commute.png` in `docs/figures/`.
5. **Check outputs**
    - Integrated data: `data/processed/integrated_state_year.csv`
    - Data quality reports: `docs/quality/missingness.csv`, `docs/quality/summary_by_year.csv`
    - Visualization: `docs/figures/obesity_vs_active_commute.png`

---

## Project Lifecycle and Workflow Mapping

This project explicitly follows a data lifecycle similar to the models discussed in class:

1. **Plan / Design** – We defined the research questions (commuting, obesity, and baby-friendly policy) and selected U.S. state-level CDC/HHS datasets that could be integrated on a common state–year key.
2. **Collect / Acquire** – `scripts_acquire_data.py` programmatically downloads the three source datasets from `data.cdc.gov` into `data/raw/` with SHA-stable filenames.
3. **Organize / Store** – We use a filesystem-based organization:
   - `data/raw/` for original CSVs,
   - `data/processed/` for integrated outputs, and
   - `docs/` for quality reports and figures.
   This aligns with the course’s emphasis on clear folder structures and naming conventions.
4. **Integrate / Enrich / Clean** – `scripts_integrate.py` and `scripts_profile_quality.py` handle schema harmonization, aggregation, integration, and quality profiling to produce `integrated_state_year.csv`, `missingness.csv`, and `summary_by_year.csv`.
5. **Analyze / Visualize** – `scripts_analyze.py` creates `docs/figures/obesity_vs_active_commute.png` to support exploratory analysis of the relationship between active commuting and obesity.
6. **Automate / Preserve / Share** – The `Snakefile` and `run_all.sh` script automate the end-to-end workflow, while this `README.md` plus a data dictionary (see below) document how others can reproduce and reuse the work.

By making each lifecycle stage explicit and script-driven, we support both **reproducibility** and **transparency**, as required by the course.

---

## Metadata and Data Documentation

To support reuse and understandability, we provide lightweight but explicit metadata:

- **Data dictionary** – A separate file `docs/data_dictionary.md` lists:
  - Each column in `integrated_state_year.csv`,
  - Its description, type (numeric/categorical),
  - Source dataset and any transformation applied (e.g., aggregation, renaming).
- **Provenance metadata** – The combination of:
  - `scripts_acquire_data.py`,
  - `scripts_integrate.py`,
  - `scripts_profile_quality.py`,
  - `Snakefile`,
  - and this `README.md`
  captures the provenance chain from original CDC/HHS APIs to final integrated outputs.
- **Licensing metadata** – We treat all derived data and code as open for educational and research use. Dataset licenses and terms of use are inherited from the original CDC/HHS sources, which are U.S. Government open data.

If this project were to be published beyond the class, we would package these metadata in a standard format such as **DataCite** or **Schema.org/Dataset** and register the archive with a DOI-issuing repository (e.g., Zenodo).

---

## Data Archival, FAIRness, and Box Folder

Per course requirements, we provide an archival copy of our key outputs via Box:

- **Box folder (output data only)**: `<INSERT BOX LINK HERE>`
- Contents:
  - `integrated_state_year.csv`
  - `docs/quality/missingness.csv`
  - `docs/quality/summary_by_year.csv`
  - `docs/figures/obesity_vs_active_commute.png`
- After downloading, these files should be placed into the corresponding folders under the project root (e.g., `data/processed/`, `docs/quality/`, `docs/figures/`). Paths are documented in this README and in the Box folder description.
- The Box paths are added to `.gitignore` so large data files are **not** pushed to GitHub, consistent with good repository hygiene.

In terms of **FAIR** principles:

- **Findable** – The GitHub repository and Box folder provide stable URLs and descriptive metadata.
- **Accessible** – All source data are retrievable via public CDC/HHS APIs; processed outputs are available from Box.
- **Interoperable** – Data are stored as CSV with clear, documented column names and types.
- **Reusable** – Licensing (U.S. Government public data) and transformation steps are documented so others can reuse or extend the integrated dataset.

If we were turning this into a research output, the next step would be to upload a frozen version of the repository plus key data artifacts to an archival repository such as Zenodo and obtain a DOI.

---

## References
1. Centers for Disease Control and Prevention. (2016). Nutrition, Physical Activity, and Obesity – American Community Survey (ACS) [Data set]. Centers for Disease Control and Prevention. https://data.cdc.gov/Nutrition-Physical-Activity-and-Obesity/Nutrition-Physical-Activity-and-Obesity-American-C/8mrp-rmkw
2. Centers for Disease Control and Prevention. (2016). Nutrition, Physical Activity, and Obesity – Behavioral Risk Factor Surveillance System (BRFSS) [Data set]. Centers for Disease Control and Prevention. https://data.cdc.gov/Nutrition-Physical-Activity-and-Obesity/Nutrition-Physical-Activity-and-Obesity-Behavioral/hn4x-zwk7
3. Centers for Disease Control and Prevention. (2016). Nutrition, Physical Activity, and Obesity – Policy and Environmental Data [Data set]. Centers for Disease Control and Prevention. https://data.cdc.gov/Nutrition-Physical-Activity-and-Obesity/Nutrition-Physical-Activity-and-Obesity-Policy-and/k8w5-7ju6