"""Cut-down F1, between the steps: apply the stop rule and pick the items. Rules are in frontier/F1_cutdown.md.

An item goes forward if Sonnet missed it at least once with no memory, and Sonnet or Haiku got it right
at least once. Fewer than 8 such items: stop, exit code 3, and write no item file. More than 24: a seeded
draw keeps 24.

Usage: uv run python frontier/scripts/select_f1.py frontier/runs/<screen run>
"""

import random
import sys
from pathlib import Path

import pandas as pd
import yaml

FRONTIER = Path(__file__).resolve().parents[1]
SOURCE = FRONTIER / "data" / "headroom.yaml"
TARGET = FRONTIER / "data" / "f1_items.yaml"
SONNET, HAIKU = "claude-sonnet", "claude-haiku"
MIN_ITEMS, MAX_ITEMS, SEED = 8, 24, 2046


def pick(raw: pd.DataFrame) -> list[str]:
    """Item IDs that qualify, before the cap."""
    usable = raw[(raw["condition"] == "no_belief") & ~raw["auto_score"].isin(["error", "unparseable"])]
    right = usable.assign(right=usable["auto_score"] == "correct").pivot_table(
        index="case_id", columns="model_alias", values="right", aggfunc="mean")
    for model in (SONNET, HAIKU):
        if model not in right:
            raise SystemExit(f"no usable screen answers from {model}")
    missed = right[SONNET] < 1
    some_right = (right[SONNET] > 0) | (right[HAIKU] > 0)
    return sorted(right.index[missed & some_right])


def cap(ids: list[str]) -> list[str]:
    return sorted(random.Random(SEED).sample(sorted(ids), MAX_ITEMS)) if len(ids) > MAX_ITEMS else sorted(ids)


def main(run_dir: Path) -> int:
    ids = pick(pd.read_csv(run_dir / "raw_table.csv"))
    print(f"{len(ids)} items qualify")
    if len(ids) < MIN_ITEMS:
        print(f"Fewer than {MIN_ITEMS}: stop here. Report that Sonnet stayed near ceiling. Do not run step 2.")
        return 3
    chosen = set(cap(ids))
    cases = [c for c in yaml.safe_load(SOURCE.read_text("utf-8"))["cases"] if c["id"] in chosen]
    TARGET.write_text(f"# Selected by frontier/scripts/select_f1.py from {run_dir.name}: {len(cases)} of {len(ids)} qualifying items.\n"
                      + yaml.safe_dump({"cases": cases}, allow_unicode=True, sort_keys=False, width=110), "utf-8")
    print(f"wrote {len(cases)} items to {TARGET}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
