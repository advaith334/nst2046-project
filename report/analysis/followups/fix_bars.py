"""Simple bar chart of the fix trade-off on Nemo: share of harm removed and share of benefit kept.

Reads report/analysis/followups/tables/q3_tradeoff.csv and writes report/figures/fig9_fix_bars.png.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
t = pd.read_csv(ROOT / "report/analysis/followups/tables/q3_tradeoff.csv")
t = t[t.model == "mistral-nemo"].set_index("variant")
names = [("label", "“Unverified” label"), ("rule", "Checking rule"), ("answer_first", "Answer before memory"),
         ("memory_gate", "Memory filter"), ("tutor", "Tutor frame"), ("patient", "Patient frame")]
harm = [100 * t.loc[v, "harm_removed"] / t.loc[v, "main_effect"] for v, _ in names]
ben = [100 * t.loc[v, "benefit_kept"] / t.loc[v, "main_benefit"] for v, _ in names]

plt.rcParams.update({"font.family": "Times New Roman", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(6.3, 3.3))
y = range(len(names))[::-1]
h = 0.36
ax.barh([i + h / 2 for i in y], harm, height=h, color="#2a78d6", label="Harm removed (share of the +41 rise in false answers)")
ax.barh([i - h / 2 for i in y], ben, height=h, color="#e07a3c", label="Benefit kept (share of the +24 rise in accuracy)")
for i, a, b in zip(y, harm, ben):
    ax.text(a + (1.5 if a >= 0 else -1.5), i + h / 2, f"{a:.0f}%", va="center", ha="left" if a >= 0 else "right", fontsize=9)
    ax.text(b + (1.5 if b >= 0 else -1.5), i - h / 2, f"{b:.0f}%", va="center", ha="left" if b >= 0 else "right", fontsize=9)
ax.set_yticks(list(y), [n for _, n in names])
ax.axvline(0, color="#555", lw=0.8)
ax.axvline(100, color="#bbb", lw=0.8, ls=":")
ax.set_xlim(-25, 110)
ax.set_xlabel("Percent")
ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=1, frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(ROOT / "report/figures/fig9_fix_bars.png", dpi=300)
print("written")
