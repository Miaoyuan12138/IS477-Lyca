#!/usr/bin/env bash
set -euo pipefail

# Simple "run everything" script for the IS477 project.
# Usage: bash run_all.sh

# 1) Create and activate a local virtual environment
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3) Run Snakemake workflow (single core by default)
snakemake --cores 1 --printshellcmds

echo "Run complete. Integrated data and quality reports are in data/processed/ and docs/quality/."