rule all:
    input:
        "data/processed/integrated_state_year.csv",
        "docs/quality/summary_by_year.csv",
        "docs/quality/missingness.csv"

rule acquire:
    output:
        unemp="data/raw/Unemployment in America Per US State.csv",
        mh="data/raw/mental_health_data.csv"
    shell:
        """
        # Placeholder: user places files or implement API pulls
        # cp /path/to/local/unemployment.csv {output.unemp}
        # cp /path/to/local/mental_health.csv {output.mh}
        touch {output.unemp}
        touch {output.mh}
        """

rule integrate:
    input:
        unemp="data/raw/Unemployment in America Per US State.csv",
        mh="data/raw/mental_health_data.csv"
    output:
        out="data/processed/integrated_state_year.csv"
    shell:
        "python scripts/integrate.py --unemp {input.unemp} --mh {input.mh} --out {output.out}"

rule profile:
    input:
        "data/processed/integrated_state_year.csv"
    output:
        by_year="docs/quality/summary_by_year.csv",
        miss="docs/quality/missingness.csv"
    shell:
        "python scripts/profile_quality.py --inp {input} --outdir docs/quality"