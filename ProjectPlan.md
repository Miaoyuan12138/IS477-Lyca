# Project Plan

## Overview
- The **goal** of this project is to explore the relationship between unemployment and mental health in the United States across different states and years. By integrating datasets on unemployment rates and mental health indicators, we aim to uncover how economic instability affects mental well-being and identify potential policy implications for workforce and healthcare planning.

---

## Research Question(s)
- How does the unemployment rate in each U.S. state correlate with mental health outcomes such as depression, anxiety, and suicide rates?
- Are there specific states or regions where unemployment has a stronger association with mental health issues?
- Do patterns change over time (e.g., pre- vs post-pandemic years)?

---

## Team
List your team members (if any) and specify clear roles and responsibilities.

| Name | Role | Responsibilities |
|------|------|------------------|
| Caroline Wen | Member | Modules 1, 3, 6, 9, 11-12, 15 in the requirements |
| Lydia Li | Member | Modules 2, 4-5, 7-8, 10, 13 in the requirements |

---

## Datasets

### Dataset 1: State Unemployment Rates (Monthly)
- **Source:** U.S. Bureau of Labor Statistics (BLS) – https://www.bls.gov/lau/

    Compiled version available through https://www.kaggle.com/datasets/justin2028/unemployment-in-america-per-us-state  

- **Format:** CSV  
- **Fields:** FIPS Code, State/Area, Year, Month, Total Civilian Non-Institutional Population in State/Area, Total Civilian Labor Force in State/Area, Percent (%) of State/Area's Population, Total Employment in State/Area, Percent (%) of Labor Force Employed in State/Area, Total Unemployment in State/Area, Percent (%) of Labor Force Unemployed in State/Area
- **License:** U.S. Government Public Domain (data produced by federal agency)
- **Purpose:** Serves as the base measure of labor market conditions across U.S. states and months. This dataset allows us to track economic stability, employment trends, and regional disparities in job markets over time.

### Dataset 2: USA Mental Health Dataset (Yearly)
- **Source:** 

    - Behavioral Risk Factor Surveillance System (BRFSS) – a national health-related telephone survey system that collects data about U.S. residents regarding their health-related risk behaviors, chronic health conditions, and use of preventive services.

    - Pregnancy Risk Assessment Monitoring System (PRAMS) – a joint project of the CDC and state health departments collecting data on maternal attitudes and experiences before, during, and shortly after pregnancy.

    - Compiled version available through https://www.kaggle.com/datasets/rifkaregmi/usa-mental-health-dataset

- **Format:** CSV  
- **Fields:** YearStart, YearEnd, LocationAbbr, LocationDesc, DataSource, Topic, Question, DataValueUnit, DataValueType, DataValue, DataValueAlt, DatavalueFootnote, LowConfidenceLimit, HighConfidenceLimit, StratificationCategory1, Stratification1, GeoLocation, LocationID, TopicID, QuestionID, DataValueTypeID, StratificationCategoryID1, StratificationID1
- **License:** CDC Open Data License (U.S. Government Public Domain)
- **Purpose:** Provides state-level indicators of population mental health, allowing examination of how social and economic variables, such as unemployment, are associated with mental health.

### Integration Strategy
- Use **State** and **Year** as the join keys.
- **Integration Goal:** Combine both datasets to evaluate correlations between unemployment rates and mental health indicators over time and across geographic regions.

---

## Timeline

| Date | Milestone | Deliverable | Responsible |
|------|------------|--------------------------------------|-------------|
| Sept 26 | Team Selection | Confirm group, create GitHub repo, relate the project to the lifecycle models, identify of all ethical, legal, or policy constraints and how they were addressed | Caroline for lifecycle models; Lydia for constraints |
| Oct 7 | Data Searching | Searching for datasets, select and describe a specific storage and organization strategy | Caroline and Lydia |
| Oct 18 | **Project Plan** | ProjectPlan.md with datasets and structure, initial exploration and profiling of datasets | Caroline and Lydia |
| Oct 25 | Data Acquisition | Start writing scripts to integrate and preprocess datasets | Caroline and Lydia |
| Nov 11 | **Interim Report** | StatusReport.md + dataset integration and preprocess scripts | Caroline and Lydia |
| Nov 20 | Workflow Automation | “Run All” pipeline | Caroline and Lydia |
| Dec 1 | Data Quality Report | Outlier handling, missing-value fixes | Caroline and Lydia |
| Dec 10 | **Final Submission** | README.md + full reproducible release | Caroline and Lydia |

---

## Constraints
- Potential year mismatches between datasets.
- Variation in definitions of mental health metrics across states.

---

## Gaps
- Need to verify overlapping years between datasets.
- Need to confirm uniformity of State naming conventions.
- May require additional regional or demographic data for deeper analysis.

---

*Version:* Draft v1.0  
*Created:* [2025-10-07]  
*Author(s):* [Caroline Wen, Lydia Li]  
