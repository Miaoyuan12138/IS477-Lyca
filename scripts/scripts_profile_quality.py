#!/usr/bin/env python
"""
Profile data quality for the integrated obesity / active commute dataset.

This script:
- Loads the integrated_state_year.csv file.
- Normalizes column names so that we always have:
    - year   (int)
    - state  (string)
- Computes:
    1) Column-level missingness.
    2) Year-level summary statistics for the key indicators.
"""

import argparse
import pandas as pd
from pathlib import Path


def detect_year_col(df: pd.DataFrame) -> str:
    """Return the name of the column that contains year information."""
    candidates = ["year", "Year", "YearStart", "YearEnd"]
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(
        f"No year-like column found. Available columns: {list(df.columns)}"
    )


def detect_state_col(df: pd.DataFrame) -> str:
    """Return the name of the column that contains state information."""
    candidates = ["state", "State", "LocationAbbr", "locationabbr"]
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(
        f"No state-like column found. Available columns: {list(df.columns)}"
    )


def compute_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Compute simple column-level missingness percentages."""
    missing = df.isna().mean().reset_index()
    missing.columns = ["column", "missing_fraction"]
    missing["missing_percent"] = (missing["missing_fraction"] * 100).round(2)
    return missing


def compute_summary_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute year-level summary statistics for key numeric indicators.

    Expects columns:
      - year
      - active_commute_pct  (from ACS)
      - obesity_pct         (from BRFSS)
      - baby_friendly_pct   (from policy/env data)
    If some of these are missing, we just summarize whatever exists.
    """
    # Only keep numeric columns plus year
    numeric_cols = []
    for col in df.columns:
        if col == "year":
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)

    if not numeric_cols:
        # Nothing to summarize numerically
        return pd.DataFrame()

    # Group by year and compute mean of numeric columns
    grouped = (
        df.groupby("year", dropna=True)[numeric_cols]
        .mean(numeric_only=True)
        .reset_index()
        .sort_values("year")
    )
    return grouped


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile quality of integrated obesity / active commute data."
    )
    parser.add_argument(
        "--integrated",
        type=Path,
        required=True,
        help="Path to integrated_state_year.csv",
    )
    parser.add_argument(
        "--missing",
        type=Path,
        required=True,
        help="Output CSV for column-level missingness",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        required=True,
        help="Output CSV for year-level summary statistics",
    )
    args = parser.parse_args()

    print(f"[quality] Loading integrated data from {args.integrated}")
    df = pd.read_csv(args.integrated)

    # Detect and normalize year/state columns so downstream code is stable
    year_col = detect_year_col(df)
    state_col = detect_state_col(df)

    if "year" not in df.columns:
        df["year"] = df[year_col]
    if "state" not in df.columns:
        df["state"] = df[state_col]

    # Column-level missingness
    print("[quality] Computing missingness by column…")
    missing_df = compute_missingness(df)
    args.missing.parent.mkdir(parents=True, exist_ok=True)
    missing_df.to_csv(args.missing, index=False)
    print(f"[quality] Wrote missingness to {args.missing}")

    # Year-level summary
    print("[quality] Computing summary by year…")
    summary_df = compute_summary_by_year(df)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(args.summary, index=False)
    print(f"[quality] Wrote summary-by-year to {args.summary}")

    print("[quality] Done.")


if __name__ == "__main__":
    main()