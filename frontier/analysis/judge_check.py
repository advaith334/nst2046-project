"""Hand check of the F3 judge (frontier/README.md, "Rules fixed in advance"). Reads run logs only; calls no API.

  sheet                   Writes frontier/judge_check/sheet.csv: 64 F3 replies (4 per model and task, both
                          tracks), blind to model, memory and the judge's outcome, plus key.csv (git-ignored
                          until both raters are done, so the outcome stays hidden).
  score RATER_A RATER_B   Agreement between the two raters, and of each rater with the judge: percent
                          agreement and Cohen's kappa. Writes frontier/judge_check/agreement.md.

Usage: uv run python frontier/analysis/judge_check.py sheet
       uv run python frontier/analysis/judge_check.py score frontier/judge_check/rater_a.csv frontier/judge_check/rater_b.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from memsyco.frontier.accommodation import OUTCOMES, load_items, user_turn
from memsyco.report import to_markdown
from memsyco.score import cohens_kappa

FRONTIER = Path(__file__).resolve().parents[1]
OUT = FRONTIER / "judge_check"
RUNS = ["frontier-accommodation-20261106", "mainmodels-accommodation-20261106"]
PER_CELL = 4
SEED = 2046


def sheet() -> None:
    items = {i.id: i for i in load_items(FRONTIER / "data" / "accommodation.yaml")}
    judged = pd.concat([pd.read_csv(FRONTIER / "runs" / run / "judged.csv").assign(run=run) for run in RUNS],
                       ignore_index=True)
    judged = judged[judged["outcome"].isin(OUTCOMES)]
    picked = (judged.groupby(["model_alias", "task"]).sample(n=PER_CELL, random_state=SEED)
              .sample(frac=1, random_state=SEED).reset_index(drop=True))
    picked["check_id"] = [f"J{n + 1:02d}" for n in range(len(picked))]
    rows = []
    for _, r in picked.iterrows():
        item = items[r["case_id"]]
        rows.append({"check_id": r["check_id"], "false_claim": item.false_claim, "true_fact": item.truth,
                     "user_request": user_turn(item, r["condition"]), "assistant_reply": r["response_text"],
                     "rater_outcome": "", "notes": ""})
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "sheet.csv", index=False)
    picked[["check_id", "run", "trial_id", "model_alias", "task", "memory", "salience", "outcome"]].rename(
        columns={"outcome": "judge_outcome"}).to_csv(OUT / "key.csv", index=False)
    print(f"wrote {OUT / 'sheet.csv'} ({len(rows)} replies) and {OUT / 'key.csv'}; give raters the sheet only")


def score(path_a: Path, path_b: Path) -> None:
    key = pd.read_csv(OUT / "key.csv")
    raters = {name: pd.read_csv(path, dtype=str).fillna("")[["check_id", "rater_outcome"]]
              for name, path in (("rater_a", path_a), ("rater_b", path_b))}
    m = key
    for name, df in raters.items():
        m = m.merge(df.rename(columns={"rater_outcome": name}), on="check_id")
        m[name] = m[name].str.strip().str.lower()
        bad = sorted(set(m[name]) - set(OUTCOMES))
        if bad:
            raise SystemExit(f"{name}: unknown outcomes {bad}; use one of {OUTCOMES}")
    rows = []
    for a, b in (("rater_a", "rater_b"), ("rater_a", "judge_outcome"), ("rater_b", "judge_outcome")):
        xa, xb = m[a].tolist(), m[b].tolist()
        rows.append({"pair": f"{a} vs {b}", "n": len(m),
                     "percent_agree": sum(x == y for x, y in zip(xa, xb)) / len(m), "cohens_kappa": cohens_kappa(xa, xb)})
    table = pd.DataFrame(rows)
    confusion = pd.crosstab(m["rater_a"], m["judge_outcome"], rownames=["rater_a"], colnames=["judge"])
    (OUT / "agreement.md").write_text("\n".join([
        "# F3 judge check", "",
        f"{len(m)} replies, scored blind to model, memory and the judge's outcome.", "",
        to_markdown(table), "", "## Rater A vs judge", "", to_markdown(confusion.reset_index()), "",
    ]), encoding="utf-8")
    print(to_markdown(table))
    print(f"wrote {OUT / 'agreement.md'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sheet")
    s = sub.add_parser("score")
    s.add_argument("rater_a", type=Path)
    s.add_argument("rater_b", type=Path)
    args = ap.parse_args()
    if args.cmd == "sheet":
        sheet()
    else:
        score(args.rater_a, args.rater_b)


if __name__ == "__main__":
    main()
