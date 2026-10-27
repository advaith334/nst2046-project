"""Item screening: which items leave room for a memory effect.

For each item x evidence mode x model, compares `no_belief` with `stored_incorrect`:
baseline accuracy, how often the incorrect option is chosen, and (where logprobs exist) the
mean probability on the incorrect option. An item is useful when a model isn't already at
ceiling, or when the stored belief moves the answer or its probability.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from .report import to_markdown

# A shift in mean probability on the incorrect option at least this large counts as movement.
P_SHIFT = 0.05


def _rates(g: pd.DataFrame) -> tuple[float, float, float]:
    usable = g[~g["auto_score"].isin(["error", "unparseable"])]
    if usable.empty:
        return math.nan, math.nan, math.nan
    acc = (usable["auto_score"] == "correct").mean()
    inc = (usable["auto_score"] == "accepted_incorrect").mean()
    p = g["p_incorrect"].dropna().mean() if "p_incorrect" in g else math.nan
    return acc, inc, p


def screen(raw: pd.DataFrame) -> pd.DataFrame:
    fact = raw[raw["case_kind"] == "factual"]
    rows = []
    for (case_id, mode, model), g in fact.groupby(["case_id", "evidence_mode", "model_alias"]):
        base_acc, base_inc, base_p = _rates(g[g["condition"] == "no_belief"])
        _, mem_inc, mem_p = _rates(g[g["condition"] == "stored_incorrect"])
        rows.append({
            "case_id": case_id,
            "evidence_mode": mode,
            "model": model,
            "base_acc": base_acc,
            "base_incorrect": base_inc,
            "stored_incorrect": mem_inc,
            "delta": mem_inc - base_inc,
            "base_p_incorrect": base_p,
            "stored_p_incorrect": mem_p,
            "p_shift": mem_p - base_p,
        })
    return pd.DataFrame(rows)


def verdict(g: pd.DataFrame) -> str:
    moved = (g["delta"] > 0).any() or (g["p_shift"].fillna(0) >= P_SHIFT).any()
    if moved:
        return "moves"
    if (g["base_acc"] < 1).any():
        return "hard, no shift"
    return "ceiling"


def write_screen(run_dir: Path, raw: pd.DataFrame) -> pd.DataFrame:
    s = screen(raw)
    s.to_csv(run_dir / "screen.csv", index=False)
    items = []
    for (case_id, mode), g in s.groupby(["case_id", "evidence_mode"]):
        row = {"case_id": case_id, "evidence_mode": mode, "verdict": verdict(g)}
        for _, r in g.iterrows():
            row[f"{r['model']} base→stored"] = f"{r['base_incorrect']:.2f}→{r['stored_incorrect']:.2f}"
            if not math.isnan(r["base_p_incorrect"]):
                row[f"{r['model']} p"] = f"{r['base_p_incorrect']:.2f}→{r['stored_p_incorrect']:.2f}"
        items.append(row)
    order = {"moves": 0, "hard, no shift": 1, "ceiling": 2}
    table = pd.DataFrame(items).fillna("")
    table = table.sort_values(["verdict", "case_id"], key=lambda c: c.map(order) if c.name == "verdict" else c)
    counts = table["verdict"].value_counts().to_dict()
    md = [
        "# Item screen",
        "",
        "Each cell: share choosing the incorrect-belief option, `no_belief` → `stored_incorrect`. "
        "`p` columns: mean probability on that option (Qwen only). Verdicts: **moves** = the stored "
        f"belief raised the incorrect choice or its probability by ≥{P_SHIFT}; **hard, no shift** = some "
        "model misses it at baseline but memory doesn't move it; **ceiling** = every model always right.",
        "",
        "Counts: " + ", ".join(f"{k}: {v}" for k, v in counts.items()),
        "",
        to_markdown(table),
    ]
    (run_dir / "screen.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return table
