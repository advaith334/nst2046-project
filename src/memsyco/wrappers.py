"""Wrapper test: does the wording around a memory drive the effect?

Each variant replaces prompt templates (`RunConfig.templates`) and is its own run, so its prompts
and results are logged like any other run. The summary compares rates across variants.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .config import RunConfig, load_yaml
from .report import to_markdown, write_report
from .runner import run
from .schema import Case, ModelSpec


def _spent(path: Path) -> float:
    rows = (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    return sum((r.get("usage") or {}).get("cost") or 0.0 for r in rows)


def run_variants(cfg: RunConfig, config_path: Path, cases: list[Case], models: list[ModelSpec], client, out_dir: Path,
                 run_id: str, limit: int | None, dry_run: bool, max_cost: float | None) -> pd.DataFrame:
    by_id = {c.id: c for c in cases}
    rows, spent = [], 0.0
    for variant in load_yaml(config_path)["variants"]:
        name = variant["name"]
        vcfg = cfg.model_copy(update={"name": f"{cfg.name}-{name}", "templates": variant.get("templates", {})})
        vdir = out_dir / name
        left = None if max_cost is None else max_cost - spent
        if left is not None and left <= 0:
            print(f"cap reached, skipping {name}")
            continue
        path = run(vcfg, cases, models, client, vdir, f"{run_id}/{name}", limit=limit, dry_run=dry_run, max_cost=left)
        spent += _spent(path)
        summary = write_report(vdir, by_id)
        for _, r in summary.iterrows():
            rows.append({"variant": name, "model": r["model"], "condition": r["condition"], "usable": r["usable"],
                         "incorrect_rate": r["incorrect_rate"], "ci_low": r["incorrect_ci_low"], "ci_high": r["incorrect_ci_high"]})
    table = pd.DataFrame(rows)
    table.to_csv(out_dir / "wrappers.csv", index=False)
    wide = table.pivot_table(index=["variant", "model"], columns="condition", values="incorrect_rate", sort=False).reset_index()
    (out_dir / "wrappers.md").write_text(
        f"# Wrapper test {out_dir.name}\n\nIncorrect-option rate by wording. Total cost ${spent:.3f}.\n\n"
        + to_markdown(wide) + "\n", encoding="utf-8")
    return table
