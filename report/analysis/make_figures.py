"""Figures for the NST2046 report. Reads report/analysis/tables, writes report/figures (PNG, 300 dpi).

Colours were checked with the colour-vision validator (all pairs pass). Each model keeps one colour
and one marker shape in every figure, so identity never depends on colour alone.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from common import FIGS, MODEL_NAMES, MODELS, TABLES

FIGS.mkdir(parents=True, exist_ok=True)
INK, MUTED, HAIR, SURFACE = "#0b0b0b", "#52514e", "#d9d8d3", "#ffffff"
COLOUR = {"mistral-nemo": "#2a78d6", "mistral-small": "#eb6834", "llama-8b": "#1baf7a"}
MARKER = {"mistral-nemo": "o", "mistral-small": "s", "llama-8b": "^"}
BLUE = COLOUR["mistral-nemo"]

plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 3, "ytick.major.size": 0, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "figure.dpi": 100,
    "savefig.dpi": 300, "savefig.facecolor": SURFACE, "axes.facecolor": SURFACE, "legend.frameon": False,
})


def grid(ax, axis="x"):
    ax.grid(axis=axis, color=HAIR, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)


def t(name):
    return pd.read_csv(TABLES / f"{name}.csv")


# ------------------------------------------------------------------ figure 1


def figure_effects():
    d = t("fig_effects")
    panels = [
        ("stored_incorrect", "no_belief", "a  Stored false belief\nvs no belief"),
        ("stored_incorrect_labelled", "stored_incorrect", "b  Label on\nvs label off"),
        ("stated_incorrect", "stored_incorrect", "c  Stated by user\nvs stored"),
        ("stored_correct", "no_belief", "d  Stored correct\nvs no belief"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 3.1), sharey=True, sharex=True)
    ypos = {m: len(MODELS) - 1 - i for i, m in enumerate(MODELS)}
    for ax, (cond, ref, title) in zip(axes, panels):
        grid(ax)
        ax.axvline(0, color=MUTED, linewidth=0.8, zorder=1)
        for _, r in d[(d.cond == cond) & (d.ref == ref)].iterrows():
            y = ypos[r.model]
            e, lo, hi = 100 * r.est, 100 * r.low, 100 * r.high
            ax.plot([lo, hi], [y, y], color=BLUE, linewidth=1.3, solid_capstyle="round", zorder=2)
            filled = bool(r.survives_item)
            ax.plot(e, y, "o", ms=6.5, mfc=BLUE if filled else SURFACE, mec=BLUE, mew=1.3, zorder=3)
            if abs(e) >= 4:
                ax.annotate(f"{e:+.0f}", (e, y), xytext=(0, 6), textcoords="offset points", ha="center",
                            fontsize=7.5, color=INK)
        ax.set_title(title, fontsize=8.2)
        ax.set_xlim(-48, 62)
        ax.set_ylim(-0.6, len(MODELS) - 0.3)
        ax.set_xticks([-40, 0, 40])
    axes[0].set_yticks([ypos[m] for m in MODELS], [MODEL_NAMES[m] for m in MODELS], color=INK)
    fig.supxlabel("Change in how often the false option was chosen (percentage points)", fontsize=9, y=0.09)
    handles = [
        Line2D([], [], marker="o", color=BLUE, mfc=BLUE, mec=BLUE, lw=1.3, ms=6, label="Passes Holm across all 42 tests, by item"),
        Line2D([], [], marker="o", color=BLUE, mfc=SURFACE, mec=BLUE, mew=1.3, lw=1.3, ms=6, label="Does not pass"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=8, bbox_to_anchor=(0.55, -0.015), handletextpad=0.5)
    fig.subplots_adjust(left=0.2, right=0.99, top=0.85, bottom=0.26, wspace=0.1)
    fig.savefig(FIGS / "fig1_effects_by_model.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 2


def figure_mechanism():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3), sharey=True, sharex=True)
    bands = t("t18_mechanism_by_confidence_band")
    floor = 1e-5
    for ax, m, tag in zip(axes, ["mistral-nemo", "mistral-small"], "ab"):
        d = pd.read_csv(TABLES / f"fig_mechanism_pairs_{m}.csv")
        x = np.log10(d["unc"].clip(lower=floor))
        rng = np.random.default_rng(2046)
        x = x + rng.uniform(-0.06, 0.06, len(x))
        y = 100 * d["delta"]
        grid(ax, "y")
        ax.axhline(0, color=MUTED, linewidth=0.8, zorder=1)
        ax.axvline(-1, color=MUTED, linewidth=0.8, linestyle=(0, (3, 3)), zorder=1)
        flip = d["flip"] == 1
        c, mk = COLOUR[m], MARKER[m]
        ax.scatter(x[~flip], y[~flip], s=20, marker=mk, facecolors=SURFACE, edgecolors=c, linewidths=0.9, zorder=2, alpha=0.9)
        ax.scatter(x[flip], y[flip], s=22, marker=mk, facecolors=c, edgecolors=SURFACE, linewidths=0.5, zorder=3)
        b = bands[bands.model == m].set_index("band")
        conf, uns = b.loc["Confident and correct"], b.loc["Unsure (top option under 90%)"]
        ax.set_title(f"{tag}  {MODEL_NAMES[m]}", fontsize=9)
        ax.text(0.03, 0.03, f"Confident and correct\n{100 * conf.share_of_total_shift:.0f}% of the total shift\n"
                            f"{int(conf.flips)} of {int(conf.flips + uns.flips)} answer flips",
                transform=ax.transAxes, va="bottom", fontsize=7.6, color=INK, linespacing=1.25,
                bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5), zorder=4)
        ax.text(0.99, 0.03, f"Unsure\n{100 * uns.share_of_total_shift:.0f}% of shift\n{int(uns.flips)} flips", transform=ax.transAxes,
                va="bottom", ha="right", fontsize=7.6, color=INK, linespacing=1.25,
                bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5), zorder=4)
        ticks = [-5, -4, -3, -2, -1, np.log10(0.5)]
        ax.set_xticks(ticks, ["99.999%\nor more", "99.99%", "99.9%", "99%", "90%", "50%"], fontsize=7.6)
        ax.set_xlim(-5.3, -0.1)
        ax.set_ylim(-105, 105)
        ax.set_yticks([-100, -50, 0, 50, 100])
    axes[0].set_ylabel("Change in probability on the false option\n(stored belief minus no belief, points)", fontsize=8.5)
    fig.supxlabel("Baseline probability on the model's top answer (no memory)", fontsize=9, y=0.1)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=MUTED, mec=SURFACE, ms=6, label="Chosen answer flipped to the false option"),
        Line2D([], [], marker="o", ls="", mfc=SURFACE, mec=MUTED, ms=5.5, label="Did not flip"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=8, bbox_to_anchor=(0.52, -0.015), handletextpad=0.3)
    fig.subplots_adjust(left=0.115, right=0.99, top=0.92, bottom=0.27, wspace=0.07)
    fig.savefig(FIGS / "fig2_uncertainty_vs_shift.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 3


def figure_label():
    r = t("t31_rates_item_ci").set_index(["model", "condition"])
    lab = t("t22_label_effect")
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw={"width_ratios": [1.25, 1]})
    conds = [("no_belief", "No belief", "o", 0.17), ("stored_incorrect_labelled", "Stored + label", "D", 0.0), ("stored_incorrect", "Stored, no label", "s", -0.17)]
    grid(a)
    for i, m in enumerate(["mistral-nemo", "mistral-small"]):
        y0 = 1 - i
        for c, name, mk, off in conds:
            v = r.loc[(m, c)]
            e, lo, hi = 100 * v.est, 100 * v.ci_low, 100 * v.ci_high
            a.plot([lo, hi], [y0 + off, y0 + off], color=COLOUR[m], linewidth=1.3, solid_capstyle="round", zorder=2)
            a.plot(e, y0 + off, mk, ms=6.5, mfc=COLOUR[m], mec=SURFACE, mew=0.6, zorder=3)
            a.annotate(f"{e:.0f}%", (hi, y0 + off), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7.6, color=INK)
    a.set_yticks([1, 0], ["Mistral\nNemo 12B", "Mistral\nSmall 24B"], color=INK)
    a.set_ylim(-0.45, 1.45)
    a.set_xlim(0, 80)
    a.set_xlabel("False option chosen (% of answers)")
    a.set_title("a  How often the false answer was chosen", fontsize=9)
    a.legend(handles=[Line2D([], [], marker=mk, ls="", mfc=MUTED, mec=SURFACE, ms=6.5, label=n) for _, n, mk, _ in conds],
             loc="lower right", fontsize=7.6, handletextpad=0.2, borderaxespad=0.1)

    rows = [("mistral-nemo", "false answers chosen", "Nemo, answers chosen"),
            ("mistral-nemo", "probability on false option", "Nemo, probability"),
            ("mistral-small", "false answers chosen", "Small, answers chosen"),
            ("mistral-small", "probability on false option", "Small, probability")]
    grid(b)
    n = len(rows)
    for i, (m, meas, name) in enumerate(rows):
        v = lab[(lab.model == m) & (lab.measure == meas)].iloc[0]
        y = n - 1 - i
        e, lo, hi = 100 * v.est, 100 * v.ci_low, 100 * v.ci_high
        b.plot([lo, hi], [y, y], color=COLOUR[m], linewidth=1.3, solid_capstyle="round", zorder=2)
        b.plot(e, y, MARKER[m], ms=6.5, mfc=COLOUR[m], mec=SURFACE, mew=0.6, zorder=3)
        b.annotate(f"{e:.0f}%", (e, y), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=7.6, color=INK)
    b.set_yticks(range(n), [x[2] for x in rows][::-1], color=INK, fontsize=8)
    b.set_ylim(-0.5, n - 0.4)
    b.set_xlim(0, 104)
    b.set_xlabel("Share of memory effect removed")
    b.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    b.set_title("b  Fraction removed", fontsize=9)
    fig.subplots_adjust(left=0.1, right=0.975, top=0.9, bottom=0.17, wspace=0.55)
    fig.savefig(FIGS / "fig3_label_effect.png")
    plt.close(fig)


# ------------------------------------------------------------------ figure 4


def figure_rounds():
    r = t("t23_rounds_baseline_vs_effect")
    r = r[r["items"].notna()]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.2), gridspec_kw={"width_ratios": [1.3, 1]})
    use = {"Round 1 pilot (misconceptions, evidence)": "R1", "Round 2 harder items, evidence": "R2 evidence",
           "Round 2 harder items, no evidence": "R2 no evidence", "Round 3 long-tail (24 items)": "R3 long-tail",
           "Round 4 main, new 24": "R4 new items"}
    # (end of the interval to label, horizontal alignment)
    place = {("mistral-nemo", "R2 no evidence"): ("top", "right"), ("mistral-nemo", "R2 evidence"): ("top", "left"),
             ("mistral-nemo", "R3 long-tail"): ("top", "center"), ("mistral-nemo", "R4 new items"): ("top", "center"),
             ("llama-8b", "R1"): ("top", "center"), ("llama-8b", "R2 evidence"): ("bottom", "center"),
             ("llama-8b", "R2 no evidence"): ("bottom", "center"), ("llama-8b", "R3 long-tail"): ("bottom", "right"),
             ("llama-8b", "R4 new items"): ("bottom", "center")}
    grid(a, "both")
    a.axhline(0, color=MUTED, linewidth=0.8, zorder=1)
    for m in ["mistral-nemo", "llama-8b"]:
        for _, v in r[r.model == m].iterrows():
            if v["round"] not in use:
                continue
            short = use[v["round"]]
            x, e, lo, hi = 100 * v.baseline_correct, 100 * v.effect, 100 * v.ci_low, 100 * v.ci_high
            if (m, short) == ("llama-8b", "R2 evidence"):
                x += 0.6  # Nemo and Llama have identical accuracy here; a small dodge keeps both visible
            a.plot([x, x], [lo, hi], color=COLOUR[m], linewidth=1.2, solid_capstyle="round", zorder=2)
            a.plot(x, e, MARKER[m], ms=6.5, mfc=COLOUR[m], mec=SURFACE, mew=0.6, zorder=3)
            end, ha = place[(m, short)]
            a.annotate(short, (x, hi if end == "top" else lo), xytext=(0, 3 if end == "top" else -3), textcoords="offset points",
                       fontsize=7.2, color=INK, ha=ha, va="bottom" if end == "top" else "top")
    a.set_xlim(38, 92)
    a.set_ylim(-32, 76)
    a.set_xlabel("Baseline accuracy, no memory (% correct)")
    a.set_ylabel("Rise in false answers, stored false\nbelief vs no belief (points)", fontsize=8.5)
    a.set_title("a  Baseline accuracy vs effect, by round", fontsize=9)
    a.legend(handles=[Line2D([], [], marker=MARKER[m], ls="", mfc=COLOUR[m], mec=SURFACE, ms=6.5, label=MODEL_NAMES[m]) for m in ["mistral-nemo", "llama-8b"]],
             loc="upper left", fontsize=7.6, handletextpad=0.2, borderaxespad=0.2)

    s = t("t26_screened_vs_new_items")
    s = s[s.comparison == "stored_incorrect vs no_belief"].set_index("model")
    grid(b)
    b.axvline(0, color=MUTED, linewidth=0.8, zorder=1)
    order = ["mistral-nemo", "mistral-small", "llama-8b"]
    for i, m in enumerate(order):
        y0 = len(order) - 1 - i
        for lab_, off, fill in [("screened", 0.15, True), ("new", -0.15, False)]:
            e, lo, hi = [100 * s.loc[m, f"{lab_}_{k}"] for k in ("effect", "low", "high")]
            b.plot([lo, hi], [y0 + off, y0 + off], color=COLOUR[m], linewidth=1.3, solid_capstyle="round", zorder=2)
            b.plot(e, y0 + off, MARKER[m], ms=6.5, mfc=COLOUR[m] if fill else SURFACE, mec=COLOUR[m], mew=1.2, zorder=3)
            b.annotate(f"{e:+.0f}", (hi, y0 + off), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7.6, color=INK)
    b.set_yticks([2, 1, 0], [MODEL_NAMES[m].replace(" 12B", "").replace(" 24B", "").replace(" 3.1 8B", "") for m in order], color=INK)
    b.set_ylim(-0.55, 2.55)
    b.set_xlim(-25, 78)
    b.set_xlabel("Rise in false answers (points)")
    b.set_title("b  Screened vs new items", fontsize=9)
    b.legend(handles=[Line2D([], [], marker="o", ls="", mfc=MUTED, mec=MUTED, ms=6, label="24 screened items"),
                      Line2D([], [], marker="o", ls="", mfc=SURFACE, mec=MUTED, mew=1.2, ms=6, label="24 new items")],
             loc="lower right", fontsize=7.6, handletextpad=0.2, borderaxespad=0.1)
    fig.subplots_adjust(left=0.1, right=0.985, top=0.92, bottom=0.14, wspace=0.42)
    fig.savefig(FIGS / "fig4_rounds_and_replication.png")
    plt.close(fig)


figure_effects()
figure_mechanism()
figure_label()
figure_rounds()
print("figures written")
