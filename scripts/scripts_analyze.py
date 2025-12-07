#!/usr/bin/env python
"""
Exploratory analysis for integrated obesity / active commuting dataset.

This script:
- Loads the integrated_state_year.csv file.
- Normalizes column names so that we always have:
    - year
    - state
    - active_commute_pct
    - obesity_pct
- Produces a scatterplot:
    x = active_commute_pct
    y = obesity_pct
    color = year
    marker style / alpha reasonable for readability.

Saved as a PNG for inclusion in the report.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def detect_year_col(df: pd.DataFrame) -> str:
    candidates = ["year", "Year", "YearStart", "YearEnd"]
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(
        f"No year-like column found. Available columns: {list(df.columns)}"
    )


def detect_state_col(df: pd.DataFrame) -> str:
    candidates = ["state", "State", "LocationAbbr", "locationabbr"]
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(
        f"No state-like column found. Available columns: {list(df.columns)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate exploratory figure for obesity vs active commuting."
    )
    parser.add_argument(
        "--integrated",
        type=Path,
        required=True,
        help="Path to integrated_state_year.csv",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output PNG path for scatter plot",
    )
    args = parser.parse_args()

    print(f"[analyze] Loading integrated data from {args.integrated}")
    df = pd.read_csv(args.integrated)

    # Detect/normalize key columns
    year_col = detect_year_col(df)
    state_col = detect_state_col(df)

    if "year" not in df.columns:
        df["year"] = df[year_col]
    if "state" not in df.columns:
        df["state"] = df[state_col]

    # Try to normalize indicator column names from integration script
    # We expect something like:
    #   active_commute_pct (ACS)
    #   obesity_pct        (BRFSS)
    #   baby_friendly_pct  (policy)
    col_map = {}

    # Active commute
    for c in df.columns:
        cl = c.lower()
        if "active" in cl and "commut" in cl:
            col_map["active_commute_pct"] = c
            break

    # Obesity
    for c in df.columns:
        cl = c.lower()
        if "obes" in cl and "pct" in cl or "percent" in cl:
            col_map["obesity_pct"] = c
            break

    if "active_commute_pct" not in col_map or "obesity_pct" not in col_map:
        raise KeyError(
            "Could not identify active commute / obesity columns. "
            f"Columns: {list(df.columns)}"
        )

    # Drop rows missing either indicator
    df_plot = df.dropna(
        subset=[col_map["active_commute_pct"], col_map["obesity_pct"], "year"]
    ).copy()

    print(f"[analyze] Plotting {len(df_plot)} state-year observations.")

    # Make sure output directory exists
    args.out.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(
        df_plot[col_map["active_commute_pct"]],
        df_plot[col_map["obesity_pct"]],
        c=df_plot["year"],
        alpha=0.7,
        edgecolors="none",
    )
    cbar = plt.colorbar(sc)
    cbar.set_label("Year")

    plt.xlabel("Percent of workers who commute by walking or biking (ACS)")
    plt.ylabel("Percent of adults with obesity (BRFSS)")
    plt.title("Obesity vs Active Commuting by State-Year")

    plt.tight_layout()
    plt.savefig(args.out, dpi=300)
    plt.close()
    print(f"[analyze] Wrote scatter plot to {args.out}")


if __name__ == "__main__":
    main()