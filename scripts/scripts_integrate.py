#!/usr/bin/env python3
"""
Integrate unemployment (monthly→annual) with mental-health indicator (Overall).
"""
import pandas as pd, numpy as np, argparse, pathlib

def main(args):
    unemp = pd.read_csv(args.unemp)
    mh = pd.read_csv(args.mh)

    rate_col = [c for c in unemp.columns if "Percent" in c and "Unemployed" in c][0]
    state_col = "State/Area"
    year_col = "Year"

    # Clean & aggregate unemployment (annual mean)
    u = unemp.copy()
    u_rate = u[rate_col].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False)
    u[rate_col] = pd.to_numeric(u_rate, errors="coerce")
    u_yearly = u.groupby([year_col, state_col], dropna=False)[rate_col].mean().reset_index()
    u_yearly = u_yearly.rename(columns={year_col: "Year", state_col: "State", rate_col: "UnemploymentRate"})

    # Mental health selection (Overall; 'Recent mentally unhealthy days among adults >= 18 years', any Mean)
    question = "Question"
    dtype = "DataValueType"
    value = "DataValue"
    yearstart = "YearStart"
    locdesc = "LocationDesc"
    strat_cat = "StratificationCategory1"
    strat = "Stratification1"

    mh_sel = mh[(mh[question].str.contains("Recent mentally unhealthy days among adults", case=False, na=False)) &
                (mh[dtype].str.contains("Mean", case=False, na=False))].copy()
    mh_overall = mh_sel[(mh_sel[strat_cat].str.contains("OVERALL", case=False, na=False)) |
                        (mh_sel[strat].str.contains("OVR|Overall", case=False, na=False))].copy()
    mh_overall[value] = pd.to_numeric(mh_overall[value], errors="coerce")
    mh_keep2 = mh_overall[[yearstart, locdesc, value]].rename(columns={yearstart: "Year", locdesc: "State", value: "MH_MeanUnhealthyDays"})

    # Aggregate duplicates (mean of means by State-Year)
    mh_agg = mh_keep2.groupby(["State", "Year"], as_index=False)["MH_MeanUnhealthyDays"].mean()

    integrated = pd.merge(mh_agg, u_yearly, on=["State", "Year"], how="inner")
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    integrated.to_csv(args.out, index=False)
    print("Wrote:", args.out, "rows:", len(integrated))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--unemp", required=True)
    ap.add_argument("--mh", required=True)
    ap.add_argument("--out", default="data/processed/integrated_state_year.csv")
    args = ap.parse_args()
    main(args)