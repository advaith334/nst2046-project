"""Item-level statistics for the frontier tests, by the report's own method. Reads run logs only; calls no API.

The report (section 4) treats the item, not the trial, as the unit: each answer is paired with the
other arm's answer on the same item and rep, the differences are averaged within item, and the mean
over items gets a 95% BCa item bootstrap (20,000 resamples, seed 2046) and an exact sign-flip test.
This reuses report/analysis/common.py for all of that, so the numbers are comparable with Parts 1-3.
Holm runs across models within each comparison (one question asked of every model). All exploratory.

Writes frontier/analysis/item_level.csv and item_level.md. Rebuild with the report's pinned versions:
PYTHONPATH=report/analysis uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 \
  --with scipy==1.18.1 --with pyyaml==6.0.3 python frontier/analysis/item_level.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "report" / "analysis"))
from common import B, SEED, boot_indices, exact_signflip_p, holm, mean_ci  # noqa: E402

RUNS = ROOT / "frontier" / "runs"
OUT = Path(__file__).resolve().parent
TRACKS = {"A": ("frontier-probes-20261106", "frontier-screen-20261106"),
          "B": ("mainmodels-probes-20261106", "mainmodels-screen-20261106")}
ACCOMMODATION = ["frontier-accommodation-20261106", "mainmodels-accommodation-20261106"]
UNUSABLE = ["error", "unparseable"]

# (label, (variant, condition), (variant, condition)): effect = first arm minus second, in false answers.
PROBE_TESTS = [
    ("F1: stored false belief", ("base", "stored_incorrect"), ("base", "no_belief")),
    ("F1: stated false belief", ("base", "stated_incorrect"), ("base", "no_belief")),
    ("F2: test cue minus real-user cue (stored)", ("eval_cue", "stored_incorrect"), ("real_cue", "stored_incorrect")),
    ("F4: expert memory minus plain memory", ("authority", "stored_incorrect"), ("base", "stored_incorrect")),
    ("F4: repeated memory minus plain memory", ("repeated", "stored_incorrect"), ("base", "stored_incorrect")),
    ("F4: after \"Are you sure?\", stored minus none", ("pushback", "stored_incorrect"), ("pushback", "no_belief")),
    ("F4: \"Are you sure?\" minus first ask (stored)", ("pushback", "stored_incorrect"), ("base", "stored_incorrect")),
]
# (label, task, outcome): effect = share with the stored myth minus share with no memory.
F3_TESTS = [
    ("F3: corrects openly, writing task", "generate", "corrects_openly"),
    ("F3: endorses the myth, edit task", "edit", "endorses"),
    ("F3: corrects openly, edit task", "edit", "corrects_openly"),
]


def probe_rows(run: str) -> pd.DataFrame:
    frames = [pd.read_csv(p).assign(variant=p.parent.name) for p in sorted((RUNS / run).glob("*/raw_table.csv"))]
    df = pd.concat(frames, ignore_index=True)
    df["y"] = np.where(df["auto_score"].isin(UNUSABLE), np.nan, (df["auto_score"] == "accepted_incorrect").astype(float))
    return df


def headroom(screen: str) -> dict[str, set[str]]:
    """Per model, the items it got wrong at least once with no memory in its own track's screen."""
    raw = pd.read_csv(RUNS / screen / "raw_table.csv")
    raw = raw[(raw["condition"] == "no_belief") & ~raw["auto_score"].isin(UNUSABLE)]
    missed = raw[raw["auto_score"] != "correct"]
    return missed.groupby("model_alias")["case_id"].agg(set).to_dict()


def item_effect(a: pd.DataFrame, b: pd.DataFrame) -> pd.Series:
    """Pair on item and rep, difference, then the mean within item (as common.item_diff)."""
    m = a[["case_id", "rep", "y"]].merge(b[["case_id", "rep", "y"]], on=["case_id", "rep"], suffixes=("_a", "_b"))
    m = m.dropna(subset=["y_a", "y_b"])
    return (m["y_a"] - m["y_b"]).groupby(m["case_id"]).mean()


def summarise(d: pd.Series, a_rate: float, b_rate: float) -> dict:
    n = len(d)
    row = {"items": n, "items_up": int((d > 0).sum()), "items_down": int((d < 0).sum()),
           "rate_a": a_rate, "rate_b": b_rate, "effect": float(d.mean()) if n else np.nan,
           "ci_low": np.nan, "ci_high": np.nan, "p_item": exact_signflip_p(d.to_numpy()) if n else np.nan}
    if n >= 1 and not (d != 0).any():
        # Nothing moved: a bootstrap of zeros is zero-width, so give the report's upper bound instead.
        row.update(ci_low=0.0, ci_high=float(1 - 0.05 ** (1 / n)))
    elif n >= 2:
        ci = mean_ci(d.to_numpy(), boot_indices(n, B, SEED))
        row.update(ci_low=ci["ci_low"], ci_high=ci["ci_high"])
    return row


def probes() -> list[dict]:
    rows = []
    for track, (run, screen) in TRACKS.items():
        df, room = probe_rows(run), headroom(screen)
        for model, g in df.groupby("model_alias"):
            for label, (va, ca), (vb, cb) in PROBE_TESTS:
                a = g[(g["variant"] == va) & (g["condition"] == ca)]
                b = g[(g["variant"] == vb) & (g["condition"] == cb)]
                for scope, items in (("headroom", room.get(model, set())), ("all", None)):
                    sa, sb = (a, b) if items is None else (a[a["case_id"].isin(items)], b[b["case_id"].isin(items)])
                    d = item_effect(sa, sb)
                    rows.append({"track": track, "model": model, "test": label, "scope": scope,
                                 **summarise(d, sa["y"].mean(), sb["y"].mean())})
    return rows


def accommodation() -> list[dict]:
    rows = []
    for run in ACCOMMODATION:
        df = pd.read_csv(RUNS / run / "judged.csv")
        track = "A" if run.startswith("frontier") else "B"
        for model, g in df.groupby("model_alias"):
            for label, task, outcome in F3_TESTS:
                t = g[g["task"] == task].copy()
                t["y"] = np.where(t["outcome"].isna(), np.nan, (t["outcome"] == outcome).astype(float))
                a, b = t[t["memory"] == "stored"], t[t["memory"] == "none"]
                d = item_effect(a, b)
                rows.append({"track": track, "model": model, "test": label, "scope": "all",
                             **summarise(d, a["y"].mean(), b["y"].mean())})
    return rows


def main() -> None:
    np.seterr(all="ignore")
    table = pd.DataFrame(probes() + accommodation())
    table["p_holm"] = np.nan
    for _, idx in table.groupby(["test", "scope"]).groups.items():
        p = table.loc[idx, "p_item"]
        ok = p.notna()
        table.loc[p[ok].index, "p_holm"] = holm(p[ok].to_numpy())
    table.to_csv(OUT / "item_level.csv", index=False)

    def fmt(r) -> str:
        if not r["items"]:
            return "no items"
        if pd.isna(r["ci_low"]):
            return f"{100 * r['effect']:+.0f} (one item, no interval)"
        e, lo, hi = (100 * r[k] for k in ("effect", "ci_low", "ci_high"))
        return f"{e:+.0f} [{lo:+.0f}, {hi:+.0f}]"

    def markdown(df: pd.DataFrame) -> str:
        rows = [list(df.columns), ["---"] * len(df.columns), *df.astype(str).values.tolist()]
        return "\n".join("| " + " | ".join(r) + " |" for r in rows)

    show = table.assign(**{"effect, points [95% CI]": table.apply(fmt, axis=1),
                           "rates (a / b)": table.apply(lambda r: f"{r['rate_a']:.0%} / {r['rate_b']:.0%}", axis=1),
                           "items up/down": table.apply(lambda r: f"{r['items_up']}/{r['items_down']} of {r['items']}", axis=1),
                           "Holm p": table["p_holm"].map(lambda p: "" if pd.isna(p) else f"{p:.3f}")})
    cols = ["track", "model", "effect, points [95% CI]", "rates (a / b)", "items up/down", "Holm p"]
    lines = ["# Frontier tests: item-level results", "",
             "Generated by `frontier/analysis/item_level.py`, by the report's method: the item is the unit, 95% BCa "
             "item-bootstrap intervals (20,000 resamples, seed 2046) and exact sign-flip tests, with Holm across models "
             "within each comparison. Where no item moved, the interval is the report's upper bound 1 − 0.05^(1/n). "
             "`headroom` = items the model got wrong at least once with no memory in its own track's screen. "
             "Track B's F4 is missing 165 of 672 trials (credit ran out). The F3 judge is not yet hand-checked. "
             "Everything here is exploratory.", ""]
    for (test, scope), g in table.groupby(["test", "scope"], sort=False):
        lines += [f"## {test} ({scope} items)", "", markdown(show.loc[g.index, cols]), ""]
    (OUT / "item_level.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT / 'item_level.csv'} and {OUT / 'item_level.md'}")


if __name__ == "__main__":
    main()
