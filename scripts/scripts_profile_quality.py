#!/usr/bin/env python3
import pandas as pd, argparse, pathlib

def main(args):
    df = pd.read_csv(args.inp)
    # Missingness
    miss = (df.isna().mean() * 100).round(2).rename("missing_pct").reset_index().rename(columns={"index": "column"})
    by_year = df.groupby("Year").agg(n_states=("State","nunique"),
                                     mean_unemp=("UnemploymentRate","mean"),
                                     mean_mh=("MH_MeanUnhealthyDays","mean")).reset_index()
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    miss.to_csv(outdir / "missingness.csv", index=False)
    by_year.to_csv(outdir / "summary_by_year.csv", index=False)
    print("Wrote:", outdir / "missingness.csv")
    print("Wrote:", outdir / "summary_by_year.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", required=True)
    ap.add_argument("--outdir", default="docs/quality")
    args = ap.parse_args()
    main(args)