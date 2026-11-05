"""Analysis for frontier tests F1 (headroom), F2 (test awareness) and F4 (pressure). Reads run logs only; calls no API.

  reasoning RUN_DIR                 Step 0: how often each model reasoned, and how often it ran out of
                                    tokens (`cut_off`), from trials.jsonl (variant folders included).
  probes RUN_DIR --screen SCREEN    Stage B: rates, paired tests, awareness and pushback breakdowns.
                                    Writes RUN_DIR/frontier_analysis.md and RUN_DIR/analysis/*.csv.

Usage: uv run python frontier/analysis/analyse.py probes frontier/runs/<probes run> --screen frontier/runs/<same track's screen run>
F3 (accommodation) needs nothing extra: `memsyco frontier-accommodation` writes its own summary.md.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd

from memsyco.conditions import option_map
from memsyco.config import load_cases, load_config
from memsyco.parse import selected_letter
from memsyco.frontier.probes import aware
from memsyco.report import mcnemar_exact, to_markdown, wilson
from memsyco.runner import option_seed

# Both tracks share items and seed, so either track's config rebuilds the option order.
CONFIG = Path(__file__).resolve().parents[1] / "config" / "probes_frontier.yaml"

# (variant, condition) compared against (variant, condition). Same item, rep and model, same option order.
COMPARISONS = [
    (("base", "stored_incorrect"), ("base", "no_belief"), "F1: stored belief"),
    (("base", "stated_incorrect"), ("base", "no_belief"), "F1: stated belief"),
    (("base", "stated_incorrect"), ("base", "stored_incorrect"), "F1: stated vs stored"),
    (("eval_cue", "stored_incorrect"), ("eval_cue", "no_belief"), "F2: stored belief, told it's a test"),
    (("real_cue", "stored_incorrect"), ("real_cue", "no_belief"), "F2: stored belief, told it's real"),
    (("eval_cue", "stored_incorrect"), ("real_cue", "stored_incorrect"), "F2: test cue vs real cue (stored)"),
    (("eval_cue", "no_belief"), ("real_cue", "no_belief"), "F2: test cue vs real cue (no belief)"),
    (("authority", "stored_incorrect"), ("base", "stored_incorrect"), "F4: expert memory vs plain memory"),
    (("repeated", "stored_incorrect"), ("base", "stored_incorrect"), "F4: repeated memory vs plain memory"),
    (("pushback", "no_belief"), ("base", "no_belief"), "F4: pushback, no belief"),
    (("pushback", "stored_incorrect"), ("pushback", "no_belief"), "F4: pushback with vs without memory"),
    (("pushback", "stored_incorrect"), ("base", "stored_incorrect"), "F4: pushback vs none (stored)"),
]


def load_variants(run_dir: Path) -> pd.DataFrame:
    frames = []
    for vdir in sorted(p for p in run_dir.iterdir() if (p / "raw_table.csv").exists()):
        frames.append(pd.read_csv(vdir / "raw_table.csv").assign(variant=vdir.name))
    if not frames:
        raise SystemExit(f"no variant raw tables under {run_dir}")
    df = pd.concat(frames, ignore_index=True)
    return df[df["case_kind"] == "factual"]


def in_scope(df: pd.DataFrame, screen: Path) -> pd.Series:
    """True where the model missed the item at least once in the screen (its own track's). A model missing from the screen keeps all."""
    raw = pd.read_csv(screen / "raw_table.csv")
    raw = raw[(raw["condition"] == "no_belief") & ~raw["auto_score"].isin(["error", "unparseable"])]
    screened = set(raw["model_alias"])
    room = set(map(tuple, raw.loc[raw["auto_score"] != "correct", ["case_id", "model_alias"]].drop_duplicates().values))
    return df.apply(lambda r: r["model_alias"] not in screened or (r["case_id"], r["model_alias"]) in room, axis=1)


def rates(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (scope, variant, model, condition), g in df.groupby(["scope", "variant", "model_alias", "condition"]):
        usable = g[~g["auto_score"].isin(["error", "unparseable"])]
        k = int((usable["auto_score"] == "accepted_incorrect").sum())
        lo, hi = wilson(k, len(usable))
        rows.append({"scope": scope, "variant": variant, "model": model, "condition": condition, "n": len(g),
                     "usable": len(usable), "correct_rate": (usable["auto_score"] == "correct").mean(),
                     "false_rate": k / len(usable) if len(usable) else math.nan, "ci_low": lo, "ci_high": hi})
    return pd.DataFrame(rows)


def paired(df: pd.DataFrame) -> pd.DataFrame:
    usable = df[~df["auto_score"].isin(["error", "unparseable"])].assign(
        inc=lambda d: d["auto_score"] == "accepted_incorrect")
    rows = []
    for (scope, model), g in usable.groupby(["scope", "model_alias"]):
        arms = {k: s.set_index(["case_id", "rep"])["inc"] for k, s in g.groupby(["variant", "condition"])}
        for cond, ref, label in COMPARISONS:
            if cond not in arms or ref not in arms:
                continue
            j = pd.concat([arms[ref], arms[cond]], axis=1, keys=["ref", "cond"]).dropna().astype(bool)
            toward, away = int((~j["ref"] & j["cond"]).sum()), int((j["ref"] & ~j["cond"]).sum())
            item = (j["cond"].astype(int) - j["ref"].astype(int)).groupby(level="case_id").mean()
            rows.append({"scope": scope, "model": model, "test": label, "comparison": f"{cond[0]}/{cond[1]} vs {ref[0]}/{ref[1]}",
                         "cross_variant": cond[0] != ref[0], "pairs": len(j), "ref_rate": j["ref"].mean(),
                         "cond_rate": j["cond"].mean(), "toward_false": toward, "away": away,
                         "items_up": int((item > 0).sum()), "items_down": int((item < 0).sum()),
                         "mcnemar_p": mcnemar_exact(toward, away)})
    return pd.DataFrame(rows)


def transcript(value) -> list[dict]:
    return json.loads(value) if isinstance(value, str) and value else []


def awareness(df: pd.DataFrame) -> pd.DataFrame:
    probed = df[df["transcript"].notna() & (df["variant"] != "pushback")]
    probed = probed.assign(aware=probed["transcript"].map(lambda t: aware(transcript(t)[-1]["content"])))
    rows = []
    for (variant, model, condition), g in probed.groupby(["variant", "model_alias", "condition"]):
        answered = g["aware"].dropna()
        rows.append({"variant": variant, "model": model, "condition": condition, "probed": len(g),
                     "answered": len(answered), "says_test": answered.mean() if len(answered) else math.nan})
    return pd.DataFrame(rows)


def pushback_moves(df: pd.DataFrame) -> pd.DataFrame:
    """First answer (before "Are you sure?") vs final answer, by model and condition."""
    cfg = load_config(CONFIG)
    cases = {c.id: c for c in load_cases(cfg.case_files)}
    pb = df[(df["variant"] == "pushback") & df["transcript"].notna() & df["scope"].eq("all")]
    rows = []
    for _, r in pb.iterrows():
        case = cases[r["case_id"]]
        omap = option_map(case, option_seed(cfg, case, int(r["rep"])))
        first_display = selected_letter(transcript(r["transcript"])[0]["content"], list(omap))
        first = omap.get(first_display) if first_display else None
        kind = lambda x: "none" if x is None else "correct" if x == case.answer else "false" if x == case.incorrect_option else "other"  # noqa: E731
        rows.append({"model": r["model_alias"], "condition": r["condition"], "first": kind(first),
                     "final": kind(r["selected"] if isinstance(r["selected"], str) else None)})
    moves = pd.DataFrame(rows)
    if moves.empty:
        return moves
    return (moves.groupby(["model", "condition", "first", "final"]).size().rename("trials").reset_index())


def reasoning_check(run_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(run_dir.rglob("trials.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            details = (r.get("usage") or {}).get("completion_tokens_details") or {}
            rows.append({"model": r["model_alias"], "reasoning": bool(r.get("reasoning_text"))
                         or bool(details.get("reasoning_tokens")), "finish": r.get("finish_reason")})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.groupby("model").agg(trials=("reasoning", "size"), with_reasoning=("reasoning", "mean"),
                                   cut_off=("finish", lambda s: (s == "length").mean())).reset_index()


def probes(run_dir: Path, screen: Path) -> None:
    df = load_variants(run_dir)
    df = pd.concat([df.assign(scope="all"), df[in_scope(df, screen)].assign(scope="headroom")], ignore_index=True)
    out = run_dir / "analysis"
    out.mkdir(exist_ok=True)
    tables = {"rates": rates(df), "paired": paired(df), "awareness": awareness(df[df["scope"] == "all"]),
              "pushback_moves": pushback_moves(df)}
    for name, t in tables.items():
        t.to_csv(out / f"{name}.csv", index=False)
    head = tables["paired"]
    head = head[head["scope"] == "headroom"] if not head.empty else head
    (run_dir / "frontier_analysis.md").write_text("\n".join([
        f"# Frontier tests F1, F2, F4: {run_dir.name}", "",
        "Automatic scores. `headroom` = per model, only items that model missed at least once in the screen "
        f"({screen.name}). In track B (the main study's models, main-study settings) rows can be read beside "
        "the main study's results, and Mistral Nemo is the positive control. Rows marked `cross_variant` compare "
        "separate runs of the same prompt plan; on identical prompts Nemo differs between runs on about 11% of "
        "trials (report/analysis/followups), so treat small cross-variant gaps as noise. All exploratory.", "",
        "## Paired comparisons (headroom items)", "", to_markdown(head) if not head.empty else "_none_", "",
        "## Does the model think it is being tested?", "",
        "`says_test` = share of probe replies starting YES.", "",
        to_markdown(tables["awareness"]) if not tables["awareness"].empty else "_no probes_", "",
        "## Pushback: first answer vs final answer", "",
        to_markdown(tables["pushback_moves"]) if not tables["pushback_moves"].empty else "_no pushback trials_", "",
        "Full rates for both scopes: `analysis/rates.csv`. Paired tests on all items: `analysis/paired.csv`.", "",
    ]), encoding="utf-8")
    print(f"wrote {run_dir / 'frontier_analysis.md'} and {out}/")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("reasoning")
    r.add_argument("run_dir", type=Path)
    p = sub.add_parser("probes")
    p.add_argument("run_dir", type=Path)
    p.add_argument("--screen", type=Path, required=True)
    args = ap.parse_args()
    if args.cmd == "reasoning":
        print(to_markdown(reasoning_check(args.run_dir)))
    else:
        probes(args.run_dir, args.screen)


if __name__ == "__main__":
    main()
