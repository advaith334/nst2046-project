"""Raw table and per-model summary: incorrect-option rate by condition, and its change vs baseline."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

from .parse import auto_score, selected_letter

from .schema import FACTUAL_CONDITIONS, USEFUL_CONDITIONS

RAW_COLUMNS = [
    "trial_id", "model_alias", "model_slug", "model_returned", "provider", "case_id", "case_kind",
    "category", "evidence_mode", "condition", "rep", "label_on", "selected_display", "selected", "auto_score",
    "p_answer", "p_incorrect", "finish_reason", "latency_s", "error", "response_text",
]


def load_trials(path: Path) -> pd.DataFrame:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    df = pd.DataFrame(rows)
    if "evidence_mode" not in df:  # runs from before evidence modes existed
        df["evidence_mode"] = "as_written"
    df["evidence_mode"] = df["evidence_mode"].fillna("as_written")
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


def rescore(df: pd.DataFrame, cases: dict) -> pd.DataFrame:
    """Re-parse every logged response with the current parser, so scoring fixes apply to old runs."""
    out = df.copy()
    for i, r in out.iterrows():
        if r["auto_score"] == "error" or r["case_id"] not in cases:
            continue
        completion = (r.get("request") or {}).get("prompt") is not None
        display = selected_letter(r["response_text"], list(r["option_map"]), completion)
        selected = r["option_map"].get(display) if display else None
        out.at[i, "selected_display"] = display
        out.at[i, "selected"] = selected
        out.at[i, "auto_score"] = auto_score(cases[r["case_id"]], selected)
    return out


def raw_table(df: pd.DataFrame, cases: dict) -> pd.DataFrame:
    def prob(row, which):
        probs = row.get("option_probs")
        if not isinstance(probs, dict):
            return None
        case = cases.get(row["case_id"])
        key = case.answer if which == "answer" else (case.incorrect_option if case else None)
        return probs.get(key) if key else None

    out = rescore(df, cases)
    out["p_answer"] = out.apply(lambda r: prob(r, "answer"), axis=1)
    out["p_incorrect"] = out.apply(lambda r: prob(r, "incorrect"), axis=1)
    return out[[c for c in RAW_COLUMNS if c in out.columns]].sort_values(["model_alias", "case_id", "condition", "rep"])


def summarise(raw: pd.DataFrame) -> pd.DataFrame:
    rows = []
    order = [c.value for c in FACTUAL_CONDITIONS + USEFUL_CONDITIONS]
    for (model, mode, condition), g in raw.groupby(["model_alias", "evidence_mode", "condition"]):
        n = len(g)
        usable = g[~g["auto_score"].isin(["error", "unparseable"])]
        u = len(usable)
        k_inc = int((usable["auto_score"] == "accepted_incorrect").sum())
        k_cor = int((usable["auto_score"] == "correct").sum())
        lo, hi = wilson(k_inc, u)
        rows.append({
            "model": model,
            "evidence_mode": mode,
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
    base = s[s["condition"] == "no_belief"].set_index(["model", "evidence_mode"])["incorrect_rate"]
    s["delta_vs_baseline"] = s.apply(
        lambda r: r["incorrect_rate"] - base.get((r["model"], r["evidence_mode"]), math.nan) if r["condition"] in
        [c.value for c in FACTUAL_CONDITIONS] else math.nan, axis=1)
    s["_o"] = s["condition"].map({c: i for i, c in enumerate(order)})
    return s.sort_values(["model", "evidence_mode", "_o"]).drop(columns="_o").reset_index(drop=True)


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from the two discordant counts."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2**n
    return min(1.0, 2 * tail)


# (condition, compared against). Pairs are matched on item, evidence mode and rep.
COMPARISONS = [(c.value, "no_belief") for c in FACTUAL_CONDITIONS[1:]] + [
    ("stored_incorrect_labelled", "stored_incorrect"),
    ("stated_incorrect", "stored_incorrect"),
]


def paired(raw: pd.DataFrame) -> pd.DataFrame:
    """Per model: how many matched trials flipped toward / away from the incorrect option."""
    fact = raw[(raw["case_kind"] == "factual") & ~raw["auto_score"].isin(["error", "unparseable"])]
    fact = fact.assign(inc=fact["auto_score"] == "accepted_incorrect")
    rows = []
    for model, g in fact.groupby("model_alias"):
        by = {c: d.set_index(["case_id", "evidence_mode", "rep"])["inc"] for c, d in g.groupby("condition")}
        for cond, ref in COMPARISONS:
            if cond not in by or ref not in by:
                continue
            j = pd.concat([by[ref], by[cond]], axis=1, keys=["ref", "cond"]).dropna().astype(bool)
            toward = int((~j["ref"] & j["cond"]).sum())
            away = int((j["ref"] & ~j["cond"]).sum())
            rows.append({
                "model": model, "comparison": f"{cond} vs {ref}", "pairs": len(j),
                "ref_rate": j["ref"].mean(), "cond_rate": j["cond"].mean(),
                "toward_incorrect": toward, "away": away, "mcnemar_p": mcnemar_exact(toward, away),
            })
    return pd.DataFrame(rows)


def to_markdown(df: pd.DataFrame) -> str:
    def fmt(v):
        if isinstance(v, float):
            if math.isnan(v):
                return ""
            return f"{v:.1e}" if 0 < abs(v) < 0.01 else f"{v:.2f}"
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
    pairs = paired(raw)
    pairs.to_csv(run_dir / "paired.csv", index=False)
    manifest = json.loads((run_dir / "manifest.json").read_text()) if (run_dir / "manifest.json").exists() else {}
    cols = ["model", *(["evidence_mode"] if summary.get("evidence_mode", pd.Series()).nunique() > 1 else []),
            "condition", "n", "usable", "correct_rate", "incorrect_rate",
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
        "",
        "## Paired comparisons",
        "",
        "Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that "
        "flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. "
        "With several models and comparisons, treat p-values as exploratory.",
        "",
        to_markdown(pairs) if not pairs.empty else "_no paired comparisons_",
    ]
    (run_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return summary
