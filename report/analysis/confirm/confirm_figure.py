"""Figure 5 of the report: confirmatory rates by model. Reads tables/models.csv and tables/rates.csv.

Static PNG for a PDF. Orange and blue are the colour roles validated for the visual summary, grey is
no memory, and every series also has its own marker shape and a legend entry.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "figures" / "fig8_confirmatory.png"
INK, MUTED, HAIR = "#0b0b0b", "#52514e", "#d9d8d3"
FALSE, TRUE, NONE = "#eb6834", "#2a78d6", "#7d7c76"
plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": INK, "ytick.major.size": 0, "xtick.major.size": 3,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "axes.titlesize": 9.5,
    "axes.titleweight": "bold", "axes.titlelocation": "left", "savefig.dpi": 300, "savefig.facecolor": "white",
})
ORDER = [("mistral-nemo", "Mistral Nemo"), ("mistral-small", "Mistral Small"), ("llama-8b-deepinfra", "Llama 3.1 8B"),
         ("qwen-small", "Qwen3.5-9B"), ("gemma-moe", "Gemma 4"), ("claude-sonnet", "Claude Sonnet*")]

rates = pd.read_csv(HERE / "tables" / "rates.csv")
# Labels are the item-level estimates from the tests, so they match the report's tables.
models = pd.read_csv(HERE / "tables" / "models.csv").set_index("model")
q2 = json.loads((HERE / "results.json").read_text())["q2"]
HARM = {m: models.loc[m, "harm_est"] for m in models.index} | {"claude-sonnet": q2["est"]}
BENEFIT = {m: models.loc[m, "benefit_est"] for m in models.index}


def pts(x):
    return f"+{int(x * 100 + 0.5)}"


rates = rates[(rates.domain == "all") & rates.run.isin(["default", "claude"])]


def val(model, cond, col):
    s = rates[(rates.model == model) & (rates.condition == cond)][col]
    return float(s.iloc[0]) * 100 if len(s) else None


fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.75), sharey=True, gridspec_kw={"wspace": 0.07})
for i, (m, _) in enumerate(ORDER):
    y = len(ORDER) - 1 - i
    nb, si, lb = val(m, "no_belief", "false"), val(m, "stored_incorrect", "false"), val(m, "stored_incorrect_labelled", "false")
    a.plot([nb, si], [y, y], color=HAIR, lw=2, zorder=1, solid_capstyle="round")
    a.scatter(nb, y, s=30, color=NONE, marker="o", zorder=3, edgecolor="white", linewidth=.6)
    a.scatter(si, y, s=38, color=FALSE, marker="D", zorder=3, edgecolor="white", linewidth=.6)
    if lb is not None:
        a.scatter(lb, y, s=30, facecolor="white", edgecolor=FALSE, marker="D", zorder=3, linewidth=1.1)
    a.text(si + 3, y, pts(HARM[m]), va="center", fontsize=8, color=INK)
    nbr, sc = val(m, "no_belief", "correct"), val(m, "stored_correct", "correct")
    if sc is None:
        b.scatter(nbr, y, s=30, color=NONE, marker="o", zorder=3, edgecolor="white", linewidth=.6)
        b.text(nbr - 3, y, "no true-memory arm", va="center", ha="right", fontsize=7.5, color=MUTED)
        continue
    b.plot([nbr, sc], [y, y], color=HAIR, lw=2, zorder=1, solid_capstyle="round")
    b.scatter(nbr, y, s=30, color=NONE, marker="o", zorder=3, edgecolor="white", linewidth=.6)
    b.scatter(sc, y, s=38, color=TRUE, marker="s", zorder=3, edgecolor="white", linewidth=.6)
    b.text(nbr - 3, y, pts(BENEFIT[m]), va="center", ha="right", fontsize=8, color=INK)
a.set_yticks(range(len(ORDER)), [n for _, n in reversed(ORDER)])
a.set(xlim=(0, 100), title="a  False answers, %")
b.set(xlim=(0, 104), title="b  Correct answers, %")
for ax in (a, b):
    ax.grid(axis="x", color=HAIR, lw=.5, zorder=0)
    ax.set_axisbelow(True)
leg = [Line2D([], [], marker="o", ls="", color=NONE, label="No memory"),
       Line2D([], [], marker="D", ls="", color=FALSE, label="False memory"),
       Line2D([], [], marker="D", ls="", mfc="white", mec=FALSE, label="False memory, labelled"),
       Line2D([], [], marker="s", ls="", color=TRUE, label="True memory")]
fig.legend(handles=leg, loc="lower center", ncol=4, frameon=False, fontsize=8, bbox_to_anchor=(.5, -.06), handletextpad=.2)
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
