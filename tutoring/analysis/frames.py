"""Frame test, as fixed in tutoring/README.md. Reads judged.csv from the seven runs; calls no API.

Rebuild with:
uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 --with scipy==1.18.1 --with pyyaml==6.0.3 python tutoring/analysis/frames.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "report" / "analysis"))
from common import B, SEED, boot_indices, holm, mc_signflip_p, mean_ci  # noqa: E402

TUTOR, ASSIST = ["tutor", "tutor_b", "tutor_c"], ["neutral", "assistant_b", "assistant_c"]
NAMES = {"mistral-nemo": "Nemo", "llama-8b-deepinfra": "Llama"}
TABLES = Path(__file__).resolve().parent / "tables"
frames = {}
for f in TUTOR + ASSIST + ["role_only"]:
    t = pd.read_csv(ROOT / f"tutoring/runs/frames-20261107-{f}/judged.csv").assign(frame=f)
    frames[f] = t
d = pd.concat(frames.values(), ignore_index=True)
print("trials", len(d), "errors", int(d.error.notna().sum()), "cost", round(d.cost.sum(), 3), "cut off", round((d.finish_1 == "length").mean(), 3),
      "no answer", round((d.answer_1_a == "none").mean(), 3))
d = d[d.answer_1_a.notna() & d.error.isna()].copy()
d["false"] = (d.answer_1_a == "target_wrong").astype(float)
d["right"] = (d.answer_1_a == "correct").astype(float)


def eff(x):
    x = x.dropna().to_numpy(float)
    r = mean_ci(x, boot_indices(len(x), B, SEED))
    return {"est": r["est"], "low": r["ci_low"], "high": r["ci_high"], "items": len(x), "up": int((x > 0).sum()), "down": int((x < 0).sum()), "p": mc_signflip_p(x)}


def rise(model, fr, col="false", arm="note_false"):
    """Per item, mean rise across the given frames."""
    g = d[(d.model_alias == model) & d.frame.isin(fr)]
    w = g.pivot_table(index=["case_id", "frame"], columns="condition", values=col)
    return (w[arm] - w["none"]).groupby(level="case_id").mean()


plan = []
for m, tag in (("mistral-nemo", "R1"), ("llama-8b-deepinfra", "R2")):
    plan.append({"id": tag, "claim": f"{NAMES[m]} rise larger in assistant than tutor frames", **eff(rise(m, ASSIST) - rise(m, TUTOR))})
for m, tag in (("mistral-nemo", "R3"), ("llama-8b-deepinfra", "R4")):
    plan.append({"id": tag, "claim": f"{NAMES[m]} rise above zero in assistant frames", **eff(rise(m, ASSIST))})
plan = pd.DataFrame(plan)
plan["p_holm"] = holm(plan.p.to_numpy())
plan["pass"] = (plan.p_holm < .05) & (plan.est > 0)
plan.to_csv(TABLES / "frames_tests.csv", index=False)
rows = []
for m in NAMES:
    for f in TUTOR + ASSIST + ["role_only"]:
        g = d[(d.model_alias == m) & (d.frame == f)]
        p = g.pivot_table(index="condition", values=["false", "right"])
        rows.append({"model": m, "frame": f, **eff(rise(m, [f])), "false_none": p.loc["none", "false"], "false_note": p.loc["note_false", "false"],
                     "right_none": p.loc["none", "right"], "right_note_false": p.loc["note_false", "right"], "right_note_true": p.loc["note_true", "right"],
                     "cut_right": eff(rise(m, [f], "right", "note_false"))["est"], "gain_true": eff(rise(m, [f], "right", "note_true"))["est"]})
fr = pd.DataFrame(rows)
fr.to_csv(TABLES / "frames_each.csv", index=False)
extra = []
for m in NAMES:
    for name, x in (("tutor rise", rise(m, TUTOR)), ("assistant rise", rise(m, ASSIST)), ("role_only rise", rise(m, ["role_only"])),
                    ("assistant minus role_only", rise(m, ASSIST) - rise(m, ["role_only"])), ("role_only minus tutor", rise(m, ["role_only"]) - rise(m, TUTOR)),
                    ("right cut, assistant", rise(m, ASSIST, "right")), ("right cut, tutor", rise(m, TUTOR, "right")),
                    ("right gain true, assistant", rise(m, ASSIST, "right", "note_true")), ("right gain true, tutor", rise(m, TUTOR, "right", "note_true")),
                    ("right gap assistant minus tutor", rise(m, ASSIST, "right") - rise(m, TUTOR, "right")),
                    ("gain gap assistant minus tutor", rise(m, ASSIST, "right", "note_true") - rise(m, TUTOR, "right", "note_true"))):
        extra.append({"model": m, "effect": name, **eff(x)})
extra = pd.DataFrame(extra)
extra.to_csv(TABLES / "frames_extra.csv", index=False)
pd.set_option("display.width", 200, "display.max_columns", 30, "display.max_rows", 100)
print(plan.round(3).to_string(index=False))
print(fr[["model", "frame", "est", "low", "high", "false_none", "false_note", "right_none", "right_note_false", "right_note_true"]].round(3).to_string(index=False))
print(extra.round(3).to_string(index=False))
