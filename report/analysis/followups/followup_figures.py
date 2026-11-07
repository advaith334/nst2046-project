"""Follow-up figures 5-7. Reads report/analysis/followups/tables, writes report/figures (PNG, 300 dpi).

Uses the same palette as make_figures.py (blue, orange, green; run through the colour-vision
validator: all pairs pass) and the same rule: a model keeps one colour, and identity never depends
on colour alone, because each series also has its own marker shape and a direct or legend label.
All three figures are post hoc.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
TABLES = HERE / "tables"
FIGS = HERE.parents[1] / "figures"
INK, MUTED, HAIR, SURFACE = "#0b0b0b", "#52514e", "#d9d8d3", "#ffffff"
NEMO, SMALL = "mistral-nemo", "mistral-small"
COLOUR = {NEMO: "#2a78d6", SMALL: "#eb6834"}
NAME = {NEMO: "Mistral Nemo 12B", SMALL: "Mistral Small 24B"}

plt.rcParams.update({"font.family": "Times New Roman",
    
    "font.size": 9, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 3, "ytick.major.size": 0, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "figure.dpi": 100,
    "savefig.dpi": 300, "savefig.facecolor": SURFACE, "axes.facecolor": SURFACE, "legend.frameon": False,
})


def t(name):
    return pd.read_csv(TABLES / f"{name}.csv")


def signed(v):
    r = round(100 * v)
    return f"+{r}" if r > 0 else f"{r}".replace("-", "−")


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=HAIR, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)


# ------------------------------------------------------------------ figure 5


def figure_dose():
    rates = t("fig5_rates")
    q = t("q1_dose_response")
    q = q[q["items"] == "all 48"]
    levels = ["none", "weak", "strong"]
    long = {"none": "No passage", "weak": "Weak passage", "strong": "Stating passage"}
    conds = [("stored_incorrect", "Stored false belief", "s", "-", 0.07), ("stored_incorrect_labelled", "Stored + unverified label", "D", "--", 0.0),
             ("no_belief", "No belief", "o", ":", -0.07)]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3), sharey=True)
    for ax, m, tag in zip(axes, [NEMO, SMALL], "ab"):
        grid(ax)
        d = rates[rates.model == m]
        for c, _, mk, ls, off in conds:
            v = d[d.condition == c].set_index("evidence").loc[levels]
            xs = [i + off for i in range(3)]
            ax.plot(xs, 100 * v.rate, ls=ls, color=COLOUR[m], lw=1.3, zorder=2)
            ax.vlines(xs, 100 * v.low, 100 * v.high, color=COLOUR[m], lw=1.1, zorder=2)
            ax.plot(xs, 100 * v.rate, mk, ms=6, mfc=COLOUR[m], mec=SURFACE, mew=0.7, ls="", zorder=3)
        qq = q[q.model == m].set_index("evidence")
        hi = d[d.condition == "stored_incorrect"].set_index("evidence").high
        for i, lev in enumerate(levels):
            r = qq.loc[lev]
            ax.annotate(f"{signed(r.effect)} [{signed(r.effect_low)}, {signed(r.effect_high)}]", (i + 0.07, 100 * hi[lev]), xytext=(0, 5),
                        textcoords="offset points", ha="center", fontsize=7.6, color=INK)
        ax.set_xticks(range(3), [f"{long[lev]}\n{100 * qq.loc[lev].nb_accuracy:.0f}% correct" for lev in levels], color=INK, fontsize=8)
        ax.set_xlim(-0.4, 2.4)
        ax.set_ylim(-2, 84)
        ax.set_title(f"{tag}  {NAME[m]}", fontsize=9)
    axes[0].set_ylabel("False option chosen (% of answers)")
    handles = [Line2D([], [], marker=mk, ls=ls, color=MUTED, mfc=MUTED, mec=SURFACE, ms=6, lw=1.3, label=n) for _, n, mk, ls, _ in conds]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8, bbox_to_anchor=(0.54, -0.012), handletextpad=0.5, columnspacing=1.6, handlelength=2.6)
    fig.subplots_adjust(left=0.085, right=0.99, top=0.92, bottom=0.235, wspace=0.06)
    fig.savefig(FIGS / "fig5_dose_response.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 6


FAMILY = {"frame": ("o", "Frame"), "harness fix": ("s", "Harness fix"), "tutor part": ("^", "One part of the tutor frame"), "label (reference)": ("D", "Unverified label")}
SHOW = {"tutor": "Tutor", "patient": "Patient", "rule": "Rule", "answer_first": "Answer first", "memory_gate": "Memory gate", "role_only": "Role", "heading_only": "Heading", "student_only": "Student", "label": "Label"}
# Nemo labels sit beside their points (offsets in points). Small's points overlap, so its labels use leader lines (data coordinates).
PLACE = {"tutor": (-4, 7, "right"), "patient": (-6, -9, "right"), "rule": (7, -9, "left"), "answer_first": (7, -9, "left"), "memory_gate": (6, -9, "left"),
         "role_only": (5, 7, "left"), "heading_only": (-7, -9, "right"), "student_only": (6, 6, "left"), "label": (6, 6, "left")}
LEADER = {"tutor": (9.4, -9.3, "center"), "patient": (6.5, 11.5, "center"), "rule": (-11, 5.5, "center"), "answer_first": (15.5, 8.5, "center"), "memory_gate": (20, -6, "center"),
          "role_only": (-4.5, -4.5, "center"), "heading_only": (0.5, 9, "center"), "student_only": (0.5, -9, "center")}


def figure_tradeoff():
    d = t("q3_tradeoff")
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.75), gridspec_kw={"width_ratios": [1.45, 1]})
    for ax, m, tag in zip(axes, [NEMO, SMALL], "ab"):
        v = d[d.model == m]
        h, b = 100 * v.main_effect.iloc[0], 100 * v.main_benefit.iloc[0]
        grid(ax, "both")
        ax.axhline(0, color=MUTED, lw=0.8, zorder=1)
        ax.axvline(0, color=MUTED, lw=0.8, zorder=1)
        ax.plot([0, h], [b, 0], color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
        c = COLOUR[m]
        for r in v.itertuples():
            x, y = 100 * r.harm_removed, 100 * r.benefit_kept
            ax.plot([100 * r.harm_low, 100 * r.harm_high], [y, y], color=c, lw=0.8, alpha=0.4, zorder=2, solid_capstyle="round")
            ax.plot([x, x], [100 * r.benefit_low, 100 * r.benefit_high], color=c, lw=0.8, alpha=0.4, zorder=2, solid_capstyle="round")
            ax.plot(x, y, FAMILY[r.family][0], ms=6.5, mfc=c, mec=SURFACE, mew=0.7, zorder=4)
            box = dict(facecolor=SURFACE, edgecolor="none", pad=0.4, alpha=0.85)
            if m == NEMO:
                dx, dy, ha = PLACE[r.variant]
                ax.annotate(SHOW[r.variant], (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=7.6, ha=ha, color=INK, zorder=5, bbox=box)
            elif r.variant != "label":  # Label and Heading sit on exactly the same point in panel b
                lx, ly, ha = LEADER[r.variant]
                name = "Heading, Label" if r.variant == "heading_only" else SHOW[r.variant]
                ax.annotate(name, (x, y), xytext=(lx, ly), textcoords="data", fontsize=7.6, ha=ha, va="center", color=INK, zorder=5, bbox=box,
                            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5, shrinkA=0, shrinkB=3))
        places = {NEMO: [(0, b, "No fix", (0, 9), "center"), (h, 0, "Memory off", (6, 7), "left")], SMALL: [(0, b, "No fix", (-7, 3), "right"), (h, 0, "Memory off", (7, 4), "left")]}
        for (x, y, name, off, ha) in places[m]:
            ax.plot(x, y, "*", ms=10, mfc=INK, mec=SURFACE, mew=0.5, zorder=5)
            ax.annotate(name, (x, y), xytext=off, textcoords="offset points", fontsize=7.6, ha=ha, color=INK, fontweight="bold", zorder=5,
                        bbox=dict(facecolor=SURFACE, edgecolor="none", pad=0.4, alpha=0.85))
        ax.set_title(f"{tag}  {NAME[m]}", fontsize=9)
        ax.set_xlabel("Harm removed (points)")
    axes[0].set_xlim(-6, 54)
    axes[0].set_ylim(-14, 36)
    axes[1].set_xlim(-18, 26)
    axes[1].set_ylim(-14, 14)
    axes[0].set_ylabel("Benefit kept (points)")
    handles = [Line2D([], [], marker=mk, ls="", mfc=MUTED, mec=SURFACE, ms=6.5, label=n) for mk, n in FAMILY.values()]
    handles += [Line2D([], [], marker="*", ls="", mfc=INK, mec=SURFACE, ms=10, label="Reference"), Line2D([], [], color=MUTED, lw=0.9, ls=(0, (4, 3)), label="Equal shares lost")]
    fig.legend(handles=handles, loc="lower center", ncol=6, fontsize=7.4, bbox_to_anchor=(0.52, -0.012), handletextpad=0.25, columnspacing=1.0)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.925, bottom=0.215, wspace=0.14)
    fig.savefig(FIGS / "fig6_fix_tradeoff.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 7


def figure_pair():
    e = t("q6_effects")
    f = t("q6_label_fraction")
    arms = [("nemo-base-local", "Local base\n(plain text)", "#eb6834", "o"), ("nemo-instruct-local", "Local instruct\n(plain text)", "#2a78d6", "s"),
            ("nemo-instruct-local-chat", "Local instruct\n(chat)", "#2a78d6", "D"), ("hosted", "Hosted instruct\n(main run)", "#2a78d6", "^")]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
    n = len(arms)
    for ax, title in [(a, "a  Rise from a stored false belief"), (b, "b  Share of the rise removed by the label")]:
        grid(ax, "x")
        ax.set_title(title, fontsize=9)
    for i, (arm, _, c, mk) in enumerate(arms):
        y0 = n - 1 - i
        v = e[(e.arm == arm) & (e.comparison == "memory effect")].iloc[0]
        w = f[f.arm == arm].set_index("measure")
        for ax, (est, lo, hi), (est2, lo2, hi2) in [(a, (v.ans_est, v.ans_low, v.ans_high), (v.prob_est, v.prob_low, v.prob_high)),
                                                    (b, tuple(w.loc["answers", ["fraction_removed", "low", "high"]]), tuple(w.loc["probabilities", ["fraction_removed", "low", "high"]]))]:
            for off, val, lo_, hi_, fill in [(0.15, est, lo, hi, True), (-0.15, est2, lo2, hi2, False)]:
                ax.plot([100 * lo_, 100 * hi_], [y0 + off] * 2, color=c, lw=1.3, solid_capstyle="round", zorder=2)
                ax.plot(100 * val, y0 + off, mk, ms=6.5, mfc=c if fill else SURFACE, mec=c, mew=1.2, zorder=3)
                ax.annotate(f"{100 * val:.0f}", (100 * hi_, y0 + off), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7.6, color=INK)
    a.set_yticks(range(n), [x[1] for x in arms][::-1], color=INK, fontsize=8)
    a.set_ylim(-0.55, n - 0.45)
    a.set_xlim(0, 74)
    a.set_xlabel("Points")
    b.set_xlim(0, 92)
    b.set_xticks([0, 25, 50, 75], ["0%", "25%", "50%", "75%"])
    b.set_xlabel("Share removed")
    handles = [Line2D([], [], marker="o", ls="", mfc=MUTED, mec=MUTED, ms=6, label="Answers chosen"), Line2D([], [], marker="o", ls="", mfc=SURFACE, mec=MUTED, mew=1.2, ms=6, label="Token probability on the false option")]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=8, bbox_to_anchor=(0.55, -0.012), handletextpad=0.3)
    fig.subplots_adjust(left=0.135, right=0.985, top=0.92, bottom=0.215, wspace=0.09)
    fig.savefig(FIGS / "fig7_base_vs_instruct.png")
    plt.close(fig)


figure_dose()
figure_tradeoff()
figure_pair()
print("figures written")
