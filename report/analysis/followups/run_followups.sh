#!/usr/bin/env bash
# Rebuilds every follow-up number, table and figure from the logged trials.
# Calls no API, reads no .env, and leaves pyproject.toml and uv.lock untouched.
# Usage, from anywhere: bash report/analysis/followups/run_followups.sh
set -euo pipefail
cd "$(dirname "$0")/../../.."
export PYTHONPATH=report/analysis PYTHONWARNINGS=ignore PYTHONDONTWRITEBYTECODE=1
run() { uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 --with scipy==1.18.1 \
  --with pyyaml==6.0.3 --with matplotlib==3.11.2 python "$@"; }
run report/analysis/followups/followup_analysis.py
run report/analysis/followups/followup_figures.py
run report/analysis/followups/write_followup_results.py
