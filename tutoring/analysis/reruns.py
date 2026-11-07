"""Post hoc reruns of the tutoring simulation (tutoring/README.md, "After the run"). Primary judge only. Calls no API.

Run with:
uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 --with scipy==1.18.1 --with pyyaml==6.0.3 \
  python tutoring/analysis/reruns.py
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "report" / "analysis"))
from common import B, SEED, boot_indices, exact_signflip_p, mean_ci  # noqa: E402

RUNS = ROOT / "tutoring" / "runs"
TABLES = Path(__file__).resolve().parent / "tables"
TABLES.mkdir(exist_ok=True)


def load(name):
    t = pd.read_csv(RUNS / name / "judged.csv")
    t = t[t.answer_1_a.notna() & t.error.isna()].copy()
    t["false1"] = (t.answer_1_a == "target_wrong").astype(float)
    t["right1"] = (t.answer_1_a == "correct").astype(float)
    t["told"] = t.told_1_a.astype(str).str.lower().eq("true").astype(float)
    if "answer_2_a" in t:
        two = t.answer_2_a.notna()
        t["false2"] = (t.answer_2_a == "target_wrong").astype(float).where(two)
        t["right2"] = (t.answer_2_a == "correct").astype(float).where(two)
    return t


def eff(d):
    x = d.dropna().to_numpy(float)
    r = mean_ci(x, boot_indices(len(x), B, SEED))
    return {"est": r["est"], "low": r["ci_low"], "high": r["ci_high"], "items": len(x), "up": int((x > 0).sum()), "down": int((x < 0).sum()), "p": exact_signflip_p(x)}


def wide(t, model, col):
    return t[t.model_alias == model].pivot_table(index="case_id", columns="condition", values=col, aggfunc="mean")


def main():
    rows, tests = [], []
    long_, plan, neutral = load("tutoring-long-20261107"), load("tutoring-20261107"), load("tutoring-neutral-20261107")
    frames = {"mistral-nemo": long_, "mistral-small": long_, "llama-8b-deepinfra": long_, "claude-haiku": plan, "claude-sonnet": plan}
    for m, t in frames.items():
        g = t[t.model_alias == m]
        row = {"model": m, "items": g.case_id.nunique(), "cut_off": (g.finish_1 == "length").mean(), "no_answer": (g.answer_1_a == "none").mean()}
        for c, h in g.groupby("condition"):
            row.update({f"right_{c}": h.right1.mean(), f"false_{c}": h.false1.mean(), f"told_{c}": h.told.mean(),
                        f"false2_{c}": h.false2.mean(), f"right2_{c}": h.right2.mean()})
        rows.append(row)
        f, r, k, s = wide(t, m, "false1"), wide(t, m, "right1"), wide(t, m, "told"), wide(t, m, "false2")
        for name, d in (("harm", f.note_false - f.none), ("benefit", r.note_true - r.none), ("purpose_harm_cut", f.note_false - f.purpose_false),
                        ("purpose_benefit_cut", r.note_true - r.purpose_true), ("purpose_told_false", k.purpose_false - k.note_false),
                        ("purpose_told_true", k.purpose_true - k.note_true), ("told_false_vs_true", k.note_false - k.note_true),
                        ("turn2_note_vs_none", s.note_false - s.none)):
            tests.append({"model": m, "effect": name, **eff(d)})
    for m in ("mistral-nemo", "mistral-small", "llama-8b-deepinfra"):
        f = wide(neutral, m, "false1")
        tests.append({"model": m, "effect": "neutral_harm", **eff(f.note_false - f.none)})
        g = neutral[neutral.model_alias == m]
        rows.append({"model": m + " neutral", "items": g.case_id.nunique(), "cut_off": (g.finish_1 == "length").mean(), "no_answer": (g.answer_1_a == "none").mean(),
                     "false_none": g[g.condition == "none"].false1.mean(), "false_note_false": g[g.condition == "note_false"].false1.mean(),
                     "right_none": g[g.condition == "none"].right1.mean(), "right_note_false": g[g.condition == "note_false"].right1.mean()})
    models, tests = pd.DataFrame(rows), pd.DataFrame(tests)
    models.to_csv(TABLES / "reruns_models.csv", index=False)
    tests.to_csv(TABLES / "reruns_tests.csv", index=False)
    pd.set_option("display.width", 200, "display.max_columns", 40, "display.max_rows", 100)
    print(models.round(3).T.to_string())
    print(tests.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
