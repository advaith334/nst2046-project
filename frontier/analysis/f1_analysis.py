"""Cut-down F1 analysis, as fixed in frontier/F1_cutdown.md. Reads the test run's raw table; calls no API.

Harm is the rise in false-option answers from no memory to false memory, per item, averaged over items.
Rebuild with:
uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 --with scipy==1.18.1 --with pyyaml==6.0.3 \
  python frontier/analysis/f1_analysis.py frontier/runs/<test run>
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "report" / "analysis"))
from common import B, SEED, boot_indices, holm, mc_signflip_p, mean_ci  # noqa: E402

PRIMARY = ["claude-sonnet", "claude-haiku"]
CONTROL = "mistral-nemo"


def harm(df: pd.DataFrame, model: str) -> pd.Series:
    g = df[df.model_alias == model]
    rate = g.groupby(["case_id", "condition"])["false"].mean().unstack()
    return (rate["stored_incorrect"] - rate["no_belief"]).dropna()


def row(df: pd.DataFrame, model: str) -> dict:
    d = harm(df, model)
    ci = mean_ci(d.to_numpy(), boot_indices(len(d), B, SEED))
    g = df[df.model_alias == model].groupby("condition")
    return {"model": model, "items": len(d), "correct_no_memory": g["right"].mean()["no_belief"],
            "false_no_memory": g["false"].mean()["no_belief"], "false_false_memory": g["false"].mean()["stored_incorrect"],
            "harm": ci["est"], "ci_low": ci["ci_low"], "ci_high": ci["ci_high"], "items_up": int((d > 0).sum()),
            "items_down": int((d < 0).sum()), "p": mc_signflip_p(d.to_numpy())}


def main(run_dir: Path) -> None:
    raw = pd.read_csv(run_dir / "raw_table.csv")
    errors, unparseable = int((raw.auto_score == "error").sum()), int((raw.auto_score == "unparseable").sum())
    df = raw[~raw.auto_score.isin(["error", "unparseable"])].copy()
    df["false"], df["right"] = (df.auto_score == "accepted_incorrect").astype(float), (df.auto_score == "correct").astype(float)
    primary = pd.DataFrame([row(df, m) for m in PRIMARY])
    primary["p_holm"] = holm(primary["p"].to_numpy())
    control = row(df, CONTROL)
    usable = control["harm"] > 0 and control["ci_low"] > 0
    table = pd.concat([primary, pd.DataFrame([control])], ignore_index=True)
    table.to_csv(run_dir / "f1_results.csv", index=False)
    lines = [f"# Cut-down F1: {run_dir.name}", "", f"Errors left: {errors}. Unparseable, excluded: {unparseable}.", "",
             table.round(4).to_csv(index=False), ""]
    if not usable:
        lines.append("**Control failed:** Nemo did not move, so these items cannot show an effect and a null here means nothing.")
    for r in primary.to_dict("records"):
        moved = r["p_holm"] < 0.05 and r["harm"] > 0
        lines.append(f"- {r['model']}: {'moved' if moved else 'not detected'}, {100 * r['harm']:+.0f} points "
                     f"[{100 * r['ci_low']:+.0f}, {100 * r['ci_high']:+.0f}] on {r['items']} items.")
    (run_dir / "f1_results.md").write_text("\n".join(lines) + "\n", "utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    np.seterr(all="ignore")
    main(Path(sys.argv[1]))
