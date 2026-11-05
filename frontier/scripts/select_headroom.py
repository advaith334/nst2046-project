"""Frontier test F1: pick the headroom items for stage B from track A's screen. The rule was fixed before the screen ran.

An item goes forward if, with no memory, at least one of the four frontier models answered it wrongly
at least once (room to move) and at least one of them answered it correctly at least once (not
hopeless). Both tracks then run stage B on these items, so their results can be compared. Track B's
models are not used here: they would let almost every item through. Each model is analysed on the
items it itself missed at least once in its own track's screen (frontier/analysis/analyse.py).

Usage: uv run python frontier/scripts/select_headroom.py frontier/runs/<track A screen run id>
"""

import sys
from pathlib import Path

import pandas as pd
import yaml

FRONTIER = Path(__file__).resolve().parents[1]
DATA = FRONTIER / "data"
SOURCE = DATA / "headroom.yaml"
TARGET = DATA / "headroom_selected.yaml"


def main(run_dir: Path) -> None:
    raw = pd.read_csv(run_dir / "raw_table.csv")
    raw = raw[(raw["condition"] == "no_belief") & ~raw["auto_score"].isin(["error", "unparseable"])]
    acc = (raw.assign(correct=raw["auto_score"] == "correct")
           .groupby(["case_id", "model_alias"])["correct"].agg(usable="size", accuracy="mean").reset_index())
    acc["headroom"] = acc["accuracy"] < 1
    deciders = yaml.safe_load((FRONTIER / "config" / "models.yaml").read_text(encoding="utf-8"))["sets"]["frontier_models"]
    missing = set(deciders) - set(acc["model_alias"])
    if missing:
        sys.exit(f"screen has no usable answers from {sorted(missing)}: use track A's screen, finished, to select")
    per_item = acc[acc["model_alias"].isin(deciders)].groupby("case_id")["accuracy"].agg(["min", "max"])
    keep = set(per_item[(per_item["min"] < 1) & (per_item["max"] > 0)].index)
    acc["selected"] = acc["case_id"].isin(keep)
    acc.to_csv(run_dir / "headroom.csv", index=False)

    data = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    chosen = [c for c in data["cases"] if c["id"] in keep]
    header = (f"# Selected by frontier/scripts/select_headroom.py from {run_dir} ({len(chosen)} of {len(data['cases'])} items).\n"
              "# Do not edit by hand. Per-model headroom is in that run's headroom.csv.\n")
    TARGET.write_text(header + yaml.safe_dump({"cases": chosen}, allow_unicode=True, sort_keys=False, width=110),
                      encoding="utf-8")

    print(f"selected {len(chosen)} of {len(data['cases'])} items -> {TARGET}")
    family = acc.assign(family=acc["case_id"].str.split("_").str[1])
    print("\nNo-memory accuracy by family and model:")
    print(family.pivot_table(index="family", columns="model_alias", values="accuracy").round(2).to_string())
    print("\nItems with headroom per model (missed at least once):")
    print(acc[acc["selected"]].groupby("model_alias")["headroom"].sum().to_string())
    if len(chosen) < 20:
        print("\nFewer than 20 items: consider more items per family in build_headroom.py before stage B.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
