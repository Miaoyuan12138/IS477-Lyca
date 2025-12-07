# Project Plan

## Overview
The goal of this project is to explore how **adult obesity prevalence** relates to
(1) **everyday active transportation** (walking or biking to work) and
(2) **state-level policy and environmental supports** for nutrition and physical activity
across U.S. states and years.

We focus on three public, government-maintained datasets from the CDC’s Nutrition, Physical Activity, and Obesity (NPAO) “Data, Trends, and Maps” program:

1. **Nutrition, Physical Activity, and Obesity – Behavioral Risk Factor Surveillance System (BRFSS)**  
   – adult obesity prevalence and related behavioral risk factors. :contentReference[oaicite:0]{index=0}  

2. **Nutrition, Physical Activity, and Obesity – American Community Survey (ACS)**  
   – percent of adults who bike or walk to work. :contentReference[oaicite:1]{index=1}  

3. **Nutrition, Physical Activity, and Obesity – Policy and Environmental Data**  
   – state-level policies and environmental supports (e.g., complete streets, PE requirements, healthy food access). :contentReference[oaicite:2]{index=2}  

By integrating these three sources at the **state–year** level, we will examine whether states with stronger policy environments and higher active commuting show lower obesity prevalence over time.

---

## Research Question(s)

**Primary Questions**

1. How is active commuting (walking or biking to work) associated with adult obesity prevalence across U.S. states from 2011–2021?  
2. Do supporting policy environments—measured by BFHI participation—align with differences in obesity trends at the state level?  
3. To what extent does tracking physical-activity infrastructure (commuting) improve interpretation of obesity outcomes relative to policy-only models?

**Secondary Questions**

- Are there systematic differences across geographic regions?
- Are there time trends that apply nationwide or only in certain states?
- How does data quality vary across sources and years?

---

## Team
List your team members (if any) and specify clear roles and responsibilities.

| Name | Role | Responsibilities |
|------|------|------------------|
| Caroline Wen | Member | Modules 1, 3, 6, 9, 11-12, 15 in the requirements |
| Lydia Li | Member | Modules 2, 4-5, 7-8, 10, 13 in the requirements |

---

## Datasets

### Dataset 1: Nutrition, Physical Activity, and Obesity – Behavioral Risk Factor Surveillance System (BRFSS)

- **Publisher:** CDC, Division of Nutrition, Physical Activity, and Obesity (DNPAO) :contentReference[oaicite:3]{index=3}  
- **Access:** Public data with Open Database License (ODbL) as indicated on Data.gov.  
- **URL:** `https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system`
- **URL (CSV API):** `https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD`  
- **Format:** CSV (wide survey-derived table).  
- **Key fields (expected):**
  - `YearStart`, `YearEnd`
  - `LocationAbbr`, `LocationDesc`
  - `Class`, `Topic`, `Question`
  - `Data_Value` (obesity %)
  - Confidence interval fields and stratification variables
- **Use in project:**  
  We will extract a **state–year adult obesity prevalence** indicator (e.g., “Percent of adults aged 18 years and older who have obesity”) and aggregate to overall state–year values (no demographic stratification) to form our primary outcome variable.

---

### Dataset 2: Nutrition, Physical Activity, and Obesity – American Community Survey (ACS)

- **Publisher:** CDC / DNPAO (derived from U.S. Census ACS). :contentReference[oaicite:4]{index=4}  
- **Access:** Public, ODbL.  
- **URL:** `https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-american-community-survey`
- **URL (CSV API):** `https://data.cdc.gov/api/views/8mrp-rmkw/rows.csv?accessType=DOWNLOAD`  
- **Format:** CSV.  
- **Key fields (expected):**
  - `YearStart`, `LocationAbbr`, `LocationDesc`
  - Indicator describing percent of adults who **bike or walk to work**
  - `Data_Value` (percentage)
- **Use in project:**  
  We will derive a **state–year metric of active commuting** from this dataset to use as a key predictor (exposure) when modeling obesity.

---

### Dataset 3: Nutrition, Physical Activity, and Obesity – Policy and Environmental Data

- **Publisher:** CDC / DNPAO. :contentReference[oaicite:5]{index=5}  
- **Access:** Public, ODbL.  
- **URL:** `https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-policy-and-environmental-data` 
- **URL (CSV API):** `https://data.cdc.gov/api/views/k8w5-7ju6/rows.csv?accessType=DOWNLOAD` 
- **Format:** CSV.  
- **Key fields (expected):**
  - `Year`, `LocationDesc`, `LocationAbbr`
  - `Category`, `Indicator` (e.g., walkability, nutrition environments, PE policies)
  - `Data_Value` and metadata
- **Use in project:**  
  We will select a small set of **policy/environment indicators** that plausibly support physical activity and healthy weight (e.g., presence of Complete Streets policies, walkability supports) and aggregate them into **state–year policy scores**.

### Integration Strategy

- **Join keys:**  
  - BRFSS: (`LocationDesc` → state; `YearStart` → year)  
  - ACS: (`LocationDesc` → state; `YearStart` → year)  
  - Policy: (`LocationDesc` → state; `Year` → year)
- **Target integrated table:**  
  - One row per `state`–`year` with:
    - `obesity_pct` (BRFSS)
    - `active_commute_pct` (ACS)
    - Several `policy_*` indicators or a combined `policy_support_score`.

We will construct this as `data/processed/integrated_state_year.csv`.

---

## Timeline

| Date | Milestone | Deliverable | Responsible |
|------|------------|--------------------------------------|-------------|
| Sept 26 | Team Selection | Confirm group, create GitHub repo, relate the project to the lifecycle models, identify of all ethical, legal, or policy constraints and how they were addressed | Caroline for lifecycle models; Lydia for constraints |
| Oct 7 | Data Searching | Searching for datasets, select and describe a specific storage and organization strategy | Caroline and Lydia |
| Oct 18 | **Project Plan** | ProjectPlan.md with datasets and structure, initial exploration and profiling of datasets | Caroline and Lydia |
| Oct 25 | Data Acquisition | Start writing scripts to integrate and preprocess datasets | Caroline and Lydia |
| Nov 17 | **Interim Report** | StatusReport.md + dataset integration and preprocess scripts | Caroline and Lydia |
| Nov 23 | Workflow Automation | “Run All” pipeline | Caroline and Lydia |
| Dec 1 | Data Quality Report | Outlier handling, missing-value fixes | Caroline and Lydia |
| Dec 10 | **Final Submission** | README.md + full reproducible release | Caroline and Lydia |

---

## Constraints

- **Schema drift:** CDC may update column names or add indicators over time; our scripts will include robust filtering but may need small manual adjustments.
- **Indicator choice:** Each dataset contains many indicators; careful selection is needed to avoid over-complication.
- **Survey uncertainty:** BRFSS is survey-based with confidence intervals and possible data suppression in some states/years.

---

## Gaps

- Need to finalize the exact BRFSS obesity indicator string and ACS active-commute indicator string based on the latest schema.
- Need to select 1–3 policy/environment indicators that are informative but manageable for this course project.
- Need to decide how to combine policy indicators into a single score (e.g., standardized sum) or keep them as separate predictors.

*Version:* Updated v3.0 (CDC obesity & ACS project)  
*Created:* 2025-10-07, *Updated:* 2025-12-07  
*Authors:* Caroline Wen, Lydia Li
