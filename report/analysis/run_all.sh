#!/usr/bin/env bash
# Rebuilds every number, table, figure and the results file from the existing run logs.
# Calls no API, reads no .env, and leaves pyproject.toml and uv.lock untouched.
# Usage, from anywhere: bash report/analysis/run_all.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH=report/analysis PYTHONWARNINGS=ignore PYTHONDONTWRITEBYTECODE=1
run() { uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 --with scipy==1.18.1 \
  --with statsmodels==0.15.0 --with pyyaml==6.0.3 --with matplotlib==3.11.2 --with numpyro==0.22.0 \
  --with jax==0.12.0.1 python "$@"; }
run report/analysis/stats_analysis.py
run report/analysis/bayes_model.py
run report/analysis/make_figures.py
run report/analysis/write_results.py
