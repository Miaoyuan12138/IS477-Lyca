#!/usr/bin/env python3
import hashlib, os, sys, argparse, csv, json, pathlib, requests

def sha256sum(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def main(args):
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    unemp_path = outdir / "Unemployment in America Per US State.csv"
    mh_path = outdir / "mental_health_data.csv"

    print(">> Expected files:")
    print("  -", unemp_path)
    print("  -", mh_path)
    print("Primary sources:")
    print("  - BLS LAU: https://www.bls.gov/lau/")
    print("  - CDC/BRFSS: https://chronicdata.cdc.gov/ (BRFSS)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="data/raw")
    args = ap.parse_args()
    main(args)
