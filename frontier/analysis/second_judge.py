"""A second AI judge on F3's replies, to see how far the first judge's result depends on the judge.

Claude Haiku 5.5 reads each F3 reply with the same rubric as DeepSeek V4 Flash, blind to condition. This is
AI against AI, not a human check. Writes frontier/analysis/second_judge.csv. Reruns skip finished rows.

Usage: uv run python frontier/analysis/second_judge.py --max-cost 0.30
"""

from __future__ import annotations

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from memsyco.client import OpenAICompatClient
from memsyco.config import load_models
from memsyco.frontier.accommodation import JUDGE_PARAMS, JUDGE_SYSTEM, judge_payload, load_items, parse_judgment
from memsyco.conditions import Rendered

ROOT = Path(__file__).resolve().parents[2]
RUNS = ["frontier-accommodation-20261106", "mainmodels-accommodation-20261106"]
OUT = ROOT / "frontier" / "analysis" / "second_judge.csv"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost", type=float, default=0.30)
    args = ap.parse_args()
    load_dotenv(ROOT / ".env")
    items = {i.id: i for i in load_items(ROOT / "frontier" / "data" / "accommodation.yaml")}
    judge = load_models(ROOT / "frontier" / "config" / "models.yaml", "second_judge")[0]
    client = OpenAICompatClient()
    table = pd.concat([pd.read_csv(ROOT / "frontier" / "runs" / r / "judged.csv") for r in RUNS], ignore_index=True)
    table = table[table["outcome"].notna() & table["response_text"].notna()].drop_duplicates("trial_id")
    done = set(pd.read_csv(OUT)["trial_id"]) if OUT.exists() else set()
    todo = table[~table["trial_id"].isin(done)].to_dict("records")
    print(f"{len(todo)} replies to judge")

    def one(r):
        user = judge_payload(items[r["case_id"]], r["condition"], r["response_text"])
        v = client.complete(judge, Rendered(system=JUDGE_SYSTEM, user=user, prompt="", messages=[
            {"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}]), JUDGE_PARAMS)
        return r["trial_id"], parse_judgment(v.text), (v.usage or {}).get("cost") or 0.0

    spent = 0.0
    new = not OUT.exists()
    with open(OUT, "a", newline="", encoding="utf-8") as f, ThreadPoolExecutor(6) as pool:
        w = csv.writer(f)
        if new:
            w.writerow(["trial_id", "second_outcome"])
        for start in range(0, len(todo), 60):
            if spent >= args.max_cost:
                print(f"stopping at ${spent:.3f}")
                break
            for tid, outcome, cost in pool.map(one, todo[start:start + 60]):
                w.writerow([tid, outcome])
                spent += cost
            f.flush()
            print(f"  {start + 60}/{len(todo)} ${spent:.3f}")
    print(f"spent ${spent:.3f}")


if __name__ == "__main__":
    main()
