#!/usr/bin/env python
"""
scripts_integrate.py

Integrate three CDC datasets (all state x year):

1) ACS (8mrp-rmkw): walking / biking to work
2) BRFSS (hn4x-zwk7): adult obesity prevalence
3) Policy / Environment (k8w5-7ju6): baby-friendly births (example policy indicator)

Outputs:
- data/processed/integrated_state_year.csv
    columns: Year, State, active_commute_pct, obesity_pct, baby_friendly_pct
"""

import argparse
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _detect_year_col(df: pd.DataFrame) -> str:
    """Try to find a year-like column."""
    for cand in ["YearStart", "Year", "YearStart_YearEnd", "DataYear"]:
        if cand in df.columns:
            return cand

    for col in df.columns:
        if "year" in col.lower():
            return col

    raise ValueError("No year column found in dataset.")


def _detect_state_col(df: pd.DataFrame) -> str:
    """Try to find a state code column (two-letter abbreviation)."""
    for cand in ["LocationAbbr", "StateAbbr", "State", "StateAbbreviation"]:
        if cand in df.columns:
            return cand

    # fallback: pick a column that looks like it has 2-letter codes
    for col in df.columns:
        if df[col].astype(str).str.fullmatch(r"[A-Z]{2}").any():
            return col

    raise ValueError("No state / LocationAbbr column found in dataset.")


# ---------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------

def load_acs(path: Path) -> pd.DataFrame:
    """
    Load ACS (walk/bike to work) from 8mrp-rmkw CSV.

    Returns DataFrame with columns: Year, State, active_commute_pct
    """
    print(f"[integrate] Loading ACS from {path}")
    df = pd.read_csv(path, dtype=str)
    print(f"[integrate] ACS raw rows: {len(df)}")

    year_col = _detect_year_col(df)
    state_col = _detect_state_col(df)

    # Filter to the walking/biking question.
    # Be robust: just require walk OR bike + "to work".
    q_col = "Question"
    if q_col not in df.columns:
        raise ValueError("ACS dataset does not contain a 'Question' column.")

    mask_q = df[q_col].str.contains("walk", case=False, na=False) | \
             df[q_col].str.contains("bike", case=False, na=False)
    mask_q &= df[q_col].str.contains("work", case=False, na=False)

    # Common column name for the value
    if "Data_Value" not in df.columns:
        raise ValueError("ACS dataset does not contain 'Data_Value' column.")

    # Restrict to 'Value' / percentage rows
    if "Data_Value_Type" in df.columns:
        mask_type = df["Data_Value_Type"].str.contains("Value", case=False, na=False)
    else:
        mask_type = True

    acs = df[mask_q & mask_type].copy()
    print(f"[integrate] ACS rows after question filter: {len(acs)}")

    # Convert to numeric
    acs["Data_Value"] = pd.to_numeric(acs["Data_Value"], errors="coerce")

    # State-year mean percent walking/biking to work
    grouped = (
        acs.groupby([year_col, state_col], as_index=False)["Data_Value"]
        .mean()
        .rename(columns={
            year_col: "Year",
            state_col: "State",
            "Data_Value": "active_commute_pct"
        })
    )

    # Clean types
    grouped["Year"] = pd.to_numeric(grouped["Year"], errors="coerce").astype("Int64")
    grouped = grouped.dropna(subset=["Year", "State"])
    grouped["State"] = grouped["State"].astype(str)

    print(f"[integrate] ACS aggregated rows: {len(grouped)}")
    return grouped


def load_brfss(path: Path) -> pd.DataFrame:
    """
    Load BRFSS obesity prevalence from hn4x-zwk7 CSV.

    We keep: Percent of adults aged 18+ who have obesity, overall (Total/Overall).

    Returns DataFrame with columns: Year, State, obesity_pct
    """
    print(f"[integrate] Loading BRFSS from {path}")
    df = pd.read_csv(path, dtype=str)
    print(f"[integrate] BRFSS raw rows: {len(df)}")

    if len(df) == 0:
        # Guard against empty file (just in case)
        raise ValueError("BRFSS dataset is empty. Check download and path.")

    year_col = _detect_year_col(df)
    state_col = _detect_state_col(df)

    # Required columns
    for col in ["Class", "Topic", "Question", "Data_Value"]:
        if col not in df.columns:
            raise ValueError(f"BRFSS dataset missing expected column '{col}'.")

    # Filter to obesity question
    mask_class = df["Class"].str.contains("Obesity", case=False, na=False)
    mask_topic = df["Topic"].str.contains("Obesity", case=False, na=False)
    mask_q = df["Question"].str.contains("Percent of adults", case=False, na=False) & \
             df["Question"].str.contains("obes", case=False, na=False)

    # Data_Value_Type ~ "Value" / "Crude prevalence" / "Age-adjusted prevalence"
    if "Data_Value_Type" in df.columns:
        mask_dvt = df["Data_Value_Type"].isin(
            ["Value", "Crude prevalence", "Age-adjusted prevalence"]
        )
    else:
        mask_dvt = True

    # Overall rows: StratificationCategory1 / Stratification1 contains Total/Overall
    if "StratificationCategory1" in df.columns:
        c1 = df["StratificationCategory1"].str.contains(
            "Total|Overall", case=False, na=False
        )
    else:
        c1 = False

    if "Stratification1" in df.columns:
        s1 = df["Stratification1"].str.contains(
            "Total|Overall", case=False, na=False
        )
    else:
        s1 = False

    mask_overall = c1 | s1

    brfss = df[mask_class & mask_topic & mask_q & mask_dvt & mask_overall].copy()
    print(f"[integrate] BRFSS rows after filters: {len(brfss)}")

    if len(brfss) == 0:
        raise ValueError("No BRFSS rows matched obesity filters; check filters / dataset.")

    # Convert to numeric
    brfss["Data_Value"] = pd.to_numeric(brfss["Data_Value"], errors="coerce")

    grouped = (
        brfss.groupby([year_col, state_col], as_index=False)["Data_Value"]
        .mean()
        .rename(columns={
            year_col: "Year",
            state_col: "State",
            "Data_Value": "obesity_pct"
        })
    )

    grouped["Year"] = pd.to_numeric(grouped["Year"], errors="coerce").astype("Int64")
    grouped = grouped.dropna(subset=["Year", "State"])
    grouped["State"] = grouped["State"].astype(str)

    print(f"[integrate] BRFSS aggregated rows: {len(grouped)}")
    return grouped


def load_policy(path: Path) -> pd.DataFrame:
    """
    Load one policy/environmental indicator from k8w5-7ju6 CSV.

    Here we use: Percent of live births occurring at "baby friendly" facilities (BFHI).

    Returns DataFrame with columns: Year, State, baby_friendly_pct
    """
    print(f"[integrate] Loading Policy data from {path}")
    df = pd.read_csv(path, dtype=str)
    print(f"[integrate] Policy raw rows: {len(df)}")

    year_col = _detect_year_col(df)
    state_col = _detect_state_col(df)

    # Required cols
    for col in ["Question", "Data_Value"]:
        if col not in df.columns:
            raise ValueError(f"Policy dataset missing expected column '{col}'.")

    # Filter to BFHI baby-friendly births question
    mask_q = df["Question"].str.contains(
        "baby friendly", case=False, na=False
    )

    # Data_Value_Type ~ "Value" / "Percent"
    if "Data_Value_Type" in df.columns:
        mask_dvt = df["Data_Value_Type"].str.contains(
            "Value|Percent", case=False, na=False
        )
    else:
        mask_dvt = True

    # Overall rows
    if "StratificationCategory1" in df.columns:
        c1 = df["StratificationCategory1"].str.contains(
            "Total|Overall", case=False, na=False
        )
    else:
        c1 = False

    if "Stratification1" in df.columns:
        s1 = df["Stratification1"].str.contains(
            "Total|Overall", case=False, na=False
        )
    else:
        s1 = False

    mask_overall = c1 | s1

    pol = df[mask_q & mask_dvt & (mask_overall | ~mask_overall)].copy()
    # (mask_overall | ~mask_overall) == keep all baby-friendly rows
    # but we still computed mask_overall in case you want to tighten later

    print(f"[integrate] Policy rows after question filter: {len(pol)}")

    # Convert Data_Value to numeric before averaging
    pol["Data_Value"] = pd.to_numeric(pol["Data_Value"], errors="coerce")

    grouped = (
        pol.groupby([year_col, state_col], as_index=False)["Data_Value"]
        .mean()
        .rename(columns={
            year_col: "Year",
            state_col: "State",
            "Data_Value": "baby_friendly_pct"
        })
    )

    grouped["Year"] = pd.to_numeric(grouped["Year"], errors="coerce").astype("Int64")
    grouped = grouped.dropna(subset=["Year", "State"])
    grouped["State"] = grouped["State"].astype(str)

    print(f"[integrate] Policy aggregated rows: {len(grouped)}")
    return grouped


# ---------------------------------------------------------------------
# Main integration
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Integrate ACS, BRFSS, and Policy datasets into state-year panel."
    )
    parser.add_argument("--acs", required=True, help="Path to ACS CSV (8mrp-rmkw).")
    parser.add_argument("--brfss", required=True, help="Path to BRFSS CSV (hn4x-zwk7).")
    parser.add_argument("--policy", required=True, help="Path to Policy CSV (k8w5-7ju6).")
    parser.add_argument("--out", required=True, help="Output CSV path.")
    args = parser.parse_args()

    acs_path = Path(args.acs)
    brfss_path = Path(args.brfss)
    policy_path = Path(args.policy)
    out_path = Path(args.out)

    acs = load_acs(acs_path)
    brfss = load_brfss(brfss_path)
    pol = load_policy(policy_path)

    # Inner joins so we only keep rows where we have all three signals
    merged = (
        acs.merge(brfss, on=["Year", "State"], how="inner")
           .merge(pol, on=["Year", "State"], how="inner")
    )

    merged = merged.sort_values(["State", "Year"]).reset_index(drop=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_path, index=False)
    print(f"[integrate] Wrote integrated dataset to {out_path} ({len(merged)} rows)")


if __name__ == "__main__":
    main()