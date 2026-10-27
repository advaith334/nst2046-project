"""Raw table and per-model summary: incorrect-option rate by condition, and its change vs baseline."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

from .schema import FACTUAL_CONDITIONS, USEFUL_CONDITIONS

RAW_COLUMNS = [
    "trial_id", "model_alias", "model_slug", "model_returned", "provider", "case_id", "case_kind",
    "category", "condition", "rep", "label_on", "selected_display", "selected", "auto_score",
    "p_answer", "p_incorrect", "finish_reason", "latency_s", "error", "response_text",
]


def load_trials(path: Path) -> pd.DataFrame:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    df = pd.DataFrame(rows)
    # Resumed runs append retries; the last row per trial wins.
    return df.drop_duplicates("trial_id", keep="last").reset_index(drop=True)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def raw_table(df: pd.DataFrame, cases: dict) -> pd.DataFrame:
    def prob(row, which):
        probs = row.get("option_probs")
        if not isinstance(probs, dict):
            return None
        case = cases.get(row["case_id"])
        key = case.answer if which == "answer" else (case.incorrect_option if case else None)
        return probs.get(key) if key else None

    out = df.copy()
    out["p_answer"] = out.apply(lambda r: prob(r, "answer"), axis=1)
    out["p_incorrect"] = out.apply(lambda r: prob(r, "incorrect"), axis=1)
    return out[[c for c in RAW_COLUMNS if c in out.columns]].sort_values(["model_alias", "case_id", "condition", "rep"])


def summarise(raw: pd.DataFrame) -> pd.DataFrame:
    rows = []
    order = [c.value for c in FACTUAL_CONDITIONS + USEFUL_CONDITIONS]
    for (model, condition), g in raw.groupby(["model_alias", "condition"]):
        n = len(g)
        usable = g[~g["auto_score"].isin(["error", "unparseable"])]
        u = len(usable)
        k_inc = int((usable["auto_score"] == "accepted_incorrect").sum())
        k_cor = int((usable["auto_score"] == "correct").sum())
        lo, hi = wilson(k_inc, u)
        rows.append({
            "model": model,
            "condition": condition,
            "n": n,
            "usable": u,
            "errors": int((g["auto_score"] == "error").sum()),
            "unparseable": int((g["auto_score"] == "unparseable").sum()),
            "correct_rate": k_cor / u if u else math.nan,
            "incorrect_rate": k_inc / u if u else math.nan,
            "incorrect_ci_low": lo,
            "incorrect_ci_high": hi,
            "mean_p_incorrect": g["p_incorrect"].dropna().mean() if "p_incorrect" in g else math.nan,
        })
    s = pd.DataFrame(rows)
    if s.empty:
        return s
    base = s[s["condition"] == "no_belief"].set_index("model")["incorrect_rate"]
    s["delta_vs_baseline"] = s.apply(
        lambda r: r["incorrect_rate"] - base.get(r["model"], math.nan) if r["condition"] in
        [c.value for c in FACTUAL_CONDITIONS] else math.nan, axis=1)
    s["_o"] = s["condition"].map({c: i for i, c in enumerate(order)})
    return s.sort_values(["model", "_o"]).drop(columns="_o").reset_index(drop=True)


def to_markdown(df: pd.DataFrame) -> str:
    def fmt(v):
        if isinstance(v, float):
            return "" if math.isnan(v) else f"{v:.2f}"
        return str(v)

    header = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    body = ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([header, sep, *body])


def write_report(run_dir: Path, cases: dict) -> pd.DataFrame:
    df = load_trials(run_dir / "trials.jsonl")
    raw = raw_table(df, cases)
    raw.to_csv(run_dir / "raw_table.csv", index=False)
    summary = summarise(raw)
    summary.to_csv(run_dir / "summary.csv", index=False)
    manifest = json.loads((run_dir / "manifest.json").read_text()) if (run_dir / "manifest.json").exists() else {}
    cols = ["model", "condition", "n", "usable", "correct_rate", "incorrect_rate",
            "incorrect_ci_low", "incorrect_ci_high", "delta_vs_baseline", "mean_p_incorrect"]
    md = [
        f"# Run {manifest.get('run_id', run_dir.name)}",
        "",
        "DRY RUN — fake responses, not results." if manifest.get("dry_run") else "",
        "`incorrect_rate` = share of usable responses choosing the option that matches the incorrect "
        "belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` "
        "for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from "
        "rates and counted separately in summary.csv.",
        "",
        to_markdown(summary[cols]) if not summary.empty else "_no trials_",
    ]
    (run_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return summary
