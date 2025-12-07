#!/usr/bin/env python

# Download CDC Nutrition, Physical Activity, and Obesity datasets
# directly from official API CSV endpoints.

import argparse
import hashlib
import os
import sys
from pathlib import Path

import requests

# Official CDC / Data.gov endpoints (CSV)
ACS_URL = "https://data.cdc.gov/api/views/8mrp-rmkw/rows.csv?accessType=DOWNLOAD"
BRFSS_URL = "https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD"
POLICY_URL = "https://data.cdc.gov/api/views/k8w5-7ju6/rows.csv?accessType=DOWNLOAD"


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[acquire] Downloading {url} -> {dest}", file=sys.stderr)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    print(f"[acquire] Wrote {dest} (sha256={sha256sum(dest)})", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        default="data/raw",
        help="Directory where raw CSV files will be stored (default: data/raw).",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)

    download(ACS_URL, outdir / "acs_active_commute_raw.csv")
    download(BRFSS_URL, outdir / "brfss_obesity_raw.csv")
    download(POLICY_URL, outdir / "policy_env_raw.csv")

    print("[acquire] Done.", file=sys.stderr)


if __name__ == "__main__":
    main()