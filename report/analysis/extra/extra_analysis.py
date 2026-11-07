"""Exploratory analyses added after the outside review. No API calls. Reads committed tables only.

Rebuild with:
uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 python report/analysis/extra/extra_analysis.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "tables"
rng = np.random.default_rng(2046)
MODELS = ["mistral-nemo", "llama-8b-deepinfra", "mistral-small", "gemma-moe", "qwen-small"]


def ci(x, b=20000):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    m = x[rng.integers(0, len(x), (b, len(x)))].mean(1)
    return float(x.mean()), float(np.quantile(m, .025)), float(np.quantile(m, .975)), len(x)


def truth_sensitivity():
    """Part 3 truth-sensitivity: follows a true memory minus follows a false one, by whether the model knew the item.

    One no-memory rep picks 'knew', the other rep is not used for the outcome, so selection does not touch the
    outcome, which comes from the memory arms. Each rep takes a turn as the picker and the two are averaged.
    """
    d = pd.read_csv(ROOT / "runs/confirm-default-20261105/raw_table.csv")
    d = d[~d.auto_score.isin(["error", "unparseable"])].assign(right=lambda x: (x.auto_score == "correct").astype(float),
                                                               false=lambda x: (x.auto_score == "accepted_incorrect").astype(float))
    rows = []
    for m in MODELS:
        g = d[d.model_alias == m]
        wide = g.pivot_table(index="case_id", columns="condition", values="right", aggfunc="mean")
        base = g[g.condition == "no_belief"].pivot_table(index="case_id", columns="rep", values="right")
        follows_false = g[g.condition == "stored_incorrect"].groupby("case_id").false.mean()
        sens = (wide.stored_correct - follows_false).dropna()
        known = [(base[r] == 1).reindex(sens.index).fillna(False).astype(bool) for r in (1, 2)]
        unsure = [(base[r] == 0).reindex(sens.index).fillna(False).astype(bool) for r in (1, 2)]
        row = {"model": m, "accuracy": g[g.condition == "no_belief"].right.mean()}
        row.update(dict(zip(("all", "all_low", "all_high", "n"), ci(sens))))
        k = pd.concat([sens[known[0]], sens[known[1]]]).groupby(level=0).mean()
        u = pd.concat([sens[unsure[0]], sens[unsure[1]]]).groupby(level=0).mean()
        row.update(dict(zip(("knew", "knew_low", "knew_high", "knew_n"), ci(k))))
        row.update(dict(zip(("unsure", "unsure_low", "unsure_high", "unsure_n"), ci(u))))
        rows.append(row)
    return pd.DataFrame(rows)


def part5():
    long_ = pd.read_csv(ROOT / "tutoring/runs/tutoring-long-20261107/judged.csv")
    plan = pd.read_csv(ROOT / "tutoring/runs/tutoring-20261107/judged.csv")
    frames = {"mistral-nemo": long_, "llama-8b-deepinfra": long_, "mistral-small": long_, "claude-haiku": plan, "claude-sonnet": plan}
    rows = []
    for m, t in frames.items():
        g = t[t.model_alias == m].copy()
        g["told"] = g.told_1_a.astype(str).str.lower().eq("true").astype(float)
        g["right"] = (g.answer_1_a == "correct").astype(float)
        g["told_right"] = g.told * g.right
        w = g.pivot_table(index="case_id", columns="condition", values="told")
        k = g[g.condition == "none"].set_index("case_id").right == 1
        row = {"model": m, "knew_items": int(k.sum()), "unsure_items": int((~k).sum())}
        for arm in ("note", "purpose"):
            gap = w[f"{arm}_false"] - w[f"{arm}_true"]
            row[f"{arm}_gap_knew"], row[f"{arm}_gap_knew_low"], row[f"{arm}_gap_knew_high"], _ = ci(gap[k.reindex(gap.index).fillna(False).astype(bool)])
            if (~k).sum() >= 5:
                row[f"{arm}_gap_unsure"], row[f"{arm}_gap_unsure_low"], row[f"{arm}_gap_unsure_high"], _ = ci(gap[~k.reindex(gap.index).fillna(False).astype(bool)])
        for c in ("note_false", "purpose_false"):
            row[f"told_and_right_{c}"] = g[g.condition == c].told_right.mean()
        rows.append(row)
    return pd.DataFrame(rows)


def log_odds():
    """Nemo local pair: log p(false) - log p(key), by item. Gap is minus that with no belief. Push is the rise with a note."""
    rows = []
    for run, m, name in (("local-base-20261105", "nemo-base-local", "base"), ("local-instruct-20261105", "nemo-instruct-local", "instruct")):
        d = pd.read_csv(ROOT / f"runs/{run}/raw_table.csv")
        d = d[(d.model_alias == m) & d.p_answer.notna() & d.p_incorrect.notna()].copy()
        d["L"] = np.log(d.p_incorrect.clip(lower=1e-4)) - np.log(d.p_answer.clip(lower=1e-4))
        w = d.pivot_table(index="case_id", columns="condition", values="L")
        L0 = w.no_belief
        row = {"arm": name, "median_gap": float((-L0).median()), "sd": float(L0.std())}
        for c in ("stored_incorrect", "stored_incorrect_labelled", "stored_correct"):
            row[c], row[c + "_low"], row[c + "_high"], _ = ci(w[c] - L0)
        row["push_in_sd"] = row["stored_incorrect"] / row["sd"]
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 220, "display.max_columns", 40)
    for name, f in (("truth_sensitivity", truth_sensitivity), ("part5_knowledge", part5), ("log_odds", log_odds)):
        t = f()
        t.to_csv(OUT / f"{name}.csv", index=False)
        print(name)
        print(t.round(3).T.to_string())
