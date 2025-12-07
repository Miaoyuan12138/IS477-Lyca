# Snakefile for IS477 obesity / active commuting project

import os

RAW_DIR = "data/raw"
PROC_DIR = "data/processed"
QUALITY_DIR = "docs/quality"
FIG_DIR = "docs/figures"

ACS_RAW = os.path.join(RAW_DIR, "acs_active_commute_raw.csv")
BRFSS_RAW = os.path.join(RAW_DIR, "brfss_obesity_raw.csv")
POLICY_RAW = os.path.join(RAW_DIR, "policy_env_raw.csv")

INTEGRATED = os.path.join(PROC_DIR, "integrated_state_year.csv")
MISSINGNESS = os.path.join(QUALITY_DIR, "missingness.csv")
SUMMARY_BY_YEAR = os.path.join(QUALITY_DIR, "summary_by_year.csv")
SCATTER_PNG = os.path.join(FIG_DIR, "obesity_vs_active_commute.png")


rule all:
    input:
        INTEGRATED,
        MISSINGNESS,
        SUMMARY_BY_YEAR,
        SCATTER_PNG


rule acquire_data:
    """
    Download ACS, BRFSS, and Policy/Environment datasets from CDC APIs.
    """
    output:
        acs=ACS_RAW,
        brfss=BRFSS_RAW,
        policy=POLICY_RAW
    shell:
        "python scripts/scripts_acquire_data.py --outdir {RAW_DIR}"


rule integrate:
    """
    Build state-year integrated dataset from raw CDC CSVs.
    """
    input:
        acs=ACS_RAW,
        brfss=BRFSS_RAW,
        policy=POLICY_RAW
    output:
        INTEGRATED
    shell:
        "python scripts/scripts_integrate.py "
        "--acs {input.acs} --brfss {input.brfss} --policy {input.policy} "
        "--out {output}"


rule profile_quality:
    """
    Compute basic quality / coverage summaries on integrated data.
    """
    input:
        INTEGRATED
    output:
        missing=MISSINGNESS,
        summary=SUMMARY_BY_YEAR
    shell:
        "python scripts/scripts_profile_quality.py "
        "--integrated {input} "
        "--missing {output.missing} "
        "--summary {output.summary}"


rule analyze:
    """
    Generate simple exploratory figure(s) from integrated data.
    """
    input:
        INTEGRATED
    output:
        SCATTER_PNG
    shell:
        "python scripts/scripts_analyze.py "
        "--integrated {input} "
        "--out {output}"