"""Confirmatory analysis, as fixed in report/preregistration.md before any trial ran.

Reads logged trials only: no API calls, no .env. Writes results.json, tables and confirm_results.md
next to this file. Harm is the rise in false-option answers from no belief to false memory. Benefit
is the rise in accuracy from no belief to true memory. The item is the unit. Unparseable answers are
excluded and counted. Anything not listed in the pre-registration is marked exploratory.

Rebuild with: uv run python report/analysis/confirm/confirm_analysis.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common import B, ROOT, SEED, boot_indices, exact_signflip_p, holm, mean_ci  # noqa: E402

RUNS = ROOT / "runs"
TABLES = HERE / "tables"
TABLES.mkdir(exist_ok=True)
NB, SI, LB, SC = "no_belief", "stored_incorrect", "stored_incorrect_labelled", "stored_correct"
NEMO, SMALL, LLAMA, GEMMA, QWEN, CLAUDE = ("mistral-nemo", "mistral-small", "llama-8b-deepinfra", "gemma-moe",
                                           "qwen-small", "claude-sonnet")
NAMES = {NEMO: "Nemo", SMALL: "Mistral Small", LLAMA: "Llama", GEMMA: "Gemma", QWEN: "Qwen3.5-9B", CLAUDE: "Claude"}
PLANNED = {"default": 4800, "claude": 240, "notes": 1440, "may_be_wrong": 1440, "tutor": 720, "patient": 720}
PATHS = {"default": "confirm-default-20261105", "claude": "confirm-claude-20261105",
         "notes": "confirm-wordings-20261105/notes", "may_be_wrong": "confirm-wordings-20261105/may_be_wrong",
         "tutor": "confirm-tutor-20261105", "patient": "confirm-patient-20261105"}


def load(name: str) -> tuple[pd.DataFrame, dict]:
    rows = [json.loads(line) for line in (RUNS / PATHS[name] / "trials.jsonl").read_text("utf-8").splitlines() if line.strip()]
    raw = pd.DataFrame(rows)
    cost = float(sum((u or {}).get("cost") or 0 for u in raw["usage"]))
    df = raw.drop_duplicates("trial_id", keep="last").reset_index(drop=True)
    score = df["auto_score"]
    info = {"run": name, "planned": PLANNED[name], "logged": len(df), "attempts": len(raw),
            "errors": int((score == "error").sum()), "unparseable": int((score == "unparseable").sum()),
            "cost": round(cost, 4)}
    df = df[~score.isin(["error", "unparseable"])].copy()
    df["false"] = (df["auto_score"] == "accepted_incorrect").astype(float)
    df["right"] = (df["auto_score"] == "correct").astype(float)
    df["domain"] = df["case_id"].str.split("_").str[1]
    return df, info


def item(df, model, cond, col, items) -> np.ndarray:
    g = df[(df.model_alias == model) & (df.condition == cond)].groupby("case_id")[col].mean()
    return g.reindex(items).to_numpy(float)


def effect(d: np.ndarray) -> dict:
    d = np.asarray(d, float)
    ok = d[np.isfinite(d)]
    idx = boot_indices(len(ok), B, SEED)
    res = mean_ci(ok, idx)
    res["n_items"] = int(len(ok))
    res["up"], res["down"] = int((ok > 0).sum()), int((ok < 0).sum())
    res["p"] = exact_signflip_p(ok)
    return res


def perm_groups(a, b, n=200_000) -> float:
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    both = np.concatenate([a, b])
    rng = np.random.default_rng(SEED)
    obs = abs(a.mean() - b.mean())
    hits = 0
    for _ in range(n // 1000):
        order = np.array([rng.permutation(len(both)) for _ in range(1000)])
        x = both[order]
        hits += (np.abs(x[:, : len(a)].mean(1) - x[:, len(a) :].mean(1)) >= obs - 1e-12).sum()
    return float((hits + 1) / (n + 1))


def main() -> None:
    data, info = {}, []
    for name in PATHS:
        data[name], i = load(name)
        info.append(i)
    d = data["default"]
    items = sorted(d.case_id.unique())
    school = [c for c in items if "_school_" in c]
    health = [c for c in items if "_health_" in c]
    assert len(items) == 120 and len(school) == 60 and len(health) == 60, (len(items), len(school), len(health))

    def harm(df, m, its=items):
        return item(df, m, SI, "false", its) - item(df, m, NB, "false", its)

    def ben(df, m, its=items):
        return item(df, m, SC, "right", its) - item(df, m, NB, "right", its)

    primary = [
        ("H1", "Harm above zero, Nemo", effect(harm(d, NEMO)), 1),
        ("H2", "Harm above zero, Mistral Small", effect(harm(d, SMALL)), 1),
        ("H3", "Label reduces Nemo's harm", effect(item(d, NEMO, SI, "false", items) - item(d, NEMO, LB, "false", items)), 1),
        ("H4", "Labelled false memory stays above no belief, Nemo", effect(item(d, NEMO, LB, "false", items) - item(d, NEMO, NB, "false", items)), 1),
        ("H5", "Benefit above zero, Nemo", effect(ben(d, NEMO)), 1),
    ]
    tu, pa = data["tutor"], data["patient"]
    h_school, h_health = harm(d, NEMO, school), harm(d, NEMO, health)
    # School and health are different items, so H8 uses a group permutation, not a sign flip.
    rng_idx_s = boot_indices(60, B, SEED)
    rng_idx_h = boot_indices(60, B, SEED + 1)
    diffs = np.nanmean(h_school[rng_idx_s], axis=1) - np.nanmean(h_health[rng_idx_h], axis=1)
    h8 = {"est": float(np.nanmean(h_school) - np.nanmean(h_health)), "ci_low": float(np.quantile(diffs, .025)),
          "ci_high": float(np.quantile(diffs, .975)), "n_items": 120, "p": perm_groups(h_school, h_health),
          "school": float(np.nanmean(h_school)), "health": float(np.nanmean(h_health))}
    secondary = [
        ("H6a", "Harm differs from zero, Llama", effect(harm(d, LLAMA)), 0),
        ("H6b", "Harm differs from zero, Gemma", effect(harm(d, GEMMA)), 0),
        ("H6c", "Harm differs from zero, Qwen3.5-9B", effect(harm(d, QWEN)), 0),
        ("H7a", "Tutor frame reduces Nemo's harm", effect(harm(d, NEMO, school) - harm(tu, NEMO, school)), 1),
        ("H7b", "Tutor frame reduces Nemo's benefit", effect(ben(d, NEMO, school) - ben(tu, NEMO, school)), 1),
        ("H7c", "Patient frame reduces Nemo's harm", effect(harm(d, NEMO, health) - harm(pa, NEMO, health)), 1),
        ("H7d", "Patient frame reduces Nemo's benefit", effect(ben(d, NEMO, health) - ben(pa, NEMO, health)), 1),
        ("H8", "Nemo's harm, school minus health", h8, 0),
    ]
    out_rows = []
    for fam, tests in (("primary", primary), ("secondary", secondary)):
        adj = holm(np.array([t[2]["p"] for t in tests]))
        for (hid, label, r, sign), a in zip(tests, adj):
            right_way = sign == 0 or r["est"] * sign > 0
            out_rows.append({"family": fam, "id": hid, "claim": label, "est": r["est"], "ci_low": r["ci_low"],
                             "ci_high": r["ci_high"], "n_items": r["n_items"], "up": r.get("up"), "down": r.get("down"),
                             "p": r["p"], "p_holm": float(a), "pass": bool(a < .05 and right_way)})
    tests = pd.DataFrame(out_rows)
    tests.to_csv(TABLES / "tests.csv", index=False)

    # Descriptive rates by model and condition.
    rates = []
    for name, df in data.items():
        for (m, c), g in df.groupby(["model_alias", "condition"]):
            for dom, h in [("all", g)] + list(g.groupby("domain")):
                rates.append({"run": name, "model": m, "condition": c, "domain": dom, "n": len(h),
                              "false": h["false"].mean(), "correct": h["right"].mean()})
    rates = pd.DataFrame(rates)
    rates.to_csv(TABLES / "rates.csv", index=False)

    # Q1: wordings against default wording, same items, both models. No prediction.
    q1 = []
    for m in (NEMO, SMALL):
        for v in ("notes", "may_be_wrong"):
            w = data[v]
            q1.append({"model": m, "variant": v, "harm_default": np.nanmean(harm(d, m)), "harm_variant": np.nanmean(harm(w, m)),
                       "benefit_default": np.nanmean(ben(d, m)), "benefit_variant": np.nanmean(ben(w, m)),
                       **{f"harm_cut_{k}": x for k, x in effect(harm(d, m) - harm(w, m)).items() if k in ("est", "ci_low", "ci_high", "p")},
                       **{f"benefit_cut_{k}": x for k, x in effect(ben(d, m) - ben(w, m)).items() if k in ("est", "ci_low", "ci_high", "p")}})
    q1 = pd.DataFrame(q1)
    q1.to_csv(TABLES / "q1_wordings.csv", index=False)

    # Q2: Claude's harm on items with both arms. Incomplete if a cap stopped the run.
    c = data["claude"]
    q2 = effect(harm(c, CLAUDE))
    q2["trials"] = int(len(c))

    # All five open models, same effects, for the paper's table.
    summary = []
    for m in (NEMO, SMALL, LLAMA, GEMMA, QWEN):
        h, b = effect(harm(d, m)), effect(ben(d, m))
        lab = effect(item(d, m, SI, "false", items) - item(d, m, LB, "false", items))
        row = {"model": m}
        for cond in (NB, SI, LB, SC):
            g = d[(d.model_alias == m) & (d.condition == cond)]
            row[f"false_{cond}"], row[f"correct_{cond}"], row[f"n_{cond}"] = g["false"].mean(), g["right"].mean(), len(g)
        row.update({f"harm_{k}": h[k] for k in ("est", "ci_low", "ci_high", "p")})
        row.update({f"benefit_{k}": b[k] for k in ("est", "ci_low", "ci_high", "p")})
        row.update({f"label_cut_{k}": lab[k] for k in ("est", "ci_low", "ci_high", "p")})
        summary.append(row)
    summary = pd.DataFrame(summary)
    summary.to_csv(TABLES / "models.csv", index=False)

    frames = []
    for name, df, its in (("tutor", tu, school), ("patient", pa, health)):
        for m in (NEMO, SMALL):
            frames.append({"frame": name, "model": m, "harm_default": np.nanmean(harm(d, m, its)), "harm_frame": np.nanmean(harm(df, m, its)),
                           "benefit_default": np.nanmean(ben(d, m, its)), "benefit_frame": np.nanmean(ben(df, m, its))})
    frames = pd.DataFrame(frames)
    frames.to_csv(TABLES / "frames.csv", index=False)

    # Exploratory from here on. None of this was pre-registered.
    def share_left(hd, hv, bd, bv):
        """Share of harm and of benefit left under a fix, with a joint item bootstrap of the gap."""
        keep = np.isfinite(hd) & np.isfinite(hv) & np.isfinite(bd) & np.isfinite(bv)
        hd, hv, bd, bv = hd[keep], hv[keep], bd[keep], bv[keep]
        idx = boot_indices(len(hd), B, SEED)
        s_h, s_b = hv.mean() / hd.mean(), bv.mean() / bd.mean()
        boots_h = hv[idx].mean(1) / hd[idx].mean(1)
        boots_b = bv[idx].mean(1) / bd[idx].mean(1)
        gap = boots_b - boots_h
        ql, qh = np.nanquantile(gap, [.025, .975])
        return {"harm_left": float(s_h), "benefit_left": float(s_b), "gap": float(s_b - s_h), "gap_low": float(ql), "gap_high": float(qh)}

    select = []
    for name, df, its in (("label", None, items), ("notes", data["notes"], items), ("may_be_wrong", data["may_be_wrong"], items),
                          ("tutor", tu, school), ("patient", pa, health)):
        if df is None:
            continue
        for m in (NEMO, SMALL):
            select.append({"fix": name, "model": m, **share_left(harm(d, m, its), harm(df, m, its), ben(d, m, its), ben(df, m, its))})
    select = pd.DataFrame(select)
    select.to_csv(TABLES / "x_selectivity.csv", index=False)

    frame_rates = []
    for name, df, its in (("default, school", d, school), ("default, health", d, health), ("notes", data["notes"], items),
                          ("may_be_wrong", data["may_be_wrong"], items), ("tutor", tu, school), ("patient", pa, health)):
        for m in (NEMO, SMALL):
            row = {"arm": name, "model": m}
            for cond in (NB, SI, SC):
                row[f"false_{cond}"] = np.nanmean(item(df, m, cond, "false", its))
                row[f"correct_{cond}"] = np.nanmean(item(df, m, cond, "right", its))
            frame_rates.append(row)
    frame_rates = pd.DataFrame(frame_rates)
    frame_rates.to_csv(TABLES / "x_arm_rates.csv", index=False)

    know = []
    for m in (NEMO, SMALL, LLAMA, GEMMA, QWEN):
        base = item(d, m, NB, "right", items)
        fl = item(d, m, SI, "false", items) - item(d, m, NB, "false", items)
        for label, mask in (("right both reps", base == 1), ("wrong at least once", base < 1)):
            know.append({"model": m, "baseline": label, "items": int(np.isfinite(fl[mask]).sum()),
                         "false_with_memory": float(np.nanmean(item(d, m, SI, "false", items)[mask])),
                         "harm": float(np.nanmean(fl[mask]))})
    know = pd.DataFrame(know)
    know.to_csv(TABLES / "x_knowledge.csv", index=False)

    dom = []
    for m in (NEMO, SMALL, LLAMA, GEMMA, QWEN):
        for label, its in (("school", school), ("health", health)):
            dom.append({"model": m, "domain": label, "harm": float(np.nanmean(harm(d, m, its))), "benefit": float(np.nanmean(ben(d, m, its)))})
    dom = pd.DataFrame(dom)
    dom.to_csv(TABLES / "x_domains.csv", index=False)

    lab = effect(item(d, NEMO, SI, "false", items) - item(d, NEMO, LB, "false", items))
    claude = c.groupby("condition")[["false", "right"]].mean()
    both = c[c.case_id.isin(c.groupby("case_id").condition.nunique().loc[lambda s: s == 2].index)]
    claude_both = both.groupby("condition")[["false", "right"]].mean()
    print(select.round(3).to_string(index=False), "\n")
    print(frame_rates.round(3).to_string(index=False), "\n")
    print(know.round(3).to_string(index=False), "\n")
    print(dom.round(3).to_string(index=False), "\n")
    print("label share of Nemo harm", round(lab["est"] / np.nanmean(harm(d, NEMO)), 3))
    print(claude.round(3), "\n", claude_both.round(3), "\n")

    pd.DataFrame(info).to_csv(TABLES / "runs.csv", index=False)
    (HERE / "results.json").write_text(json.dumps({"runs": info, "q2": q2}, indent=2), "utf-8")
    pc = lambda x: f"{100*x:+.0f}"  # noqa: E731
    print(pd.DataFrame(info).to_string(index=False), "\n")
    print(tests.assign(est=tests.est.map(pc), ci=[f"[{pc(a)}, {pc(b)}]" for a, b in zip(tests.ci_low, tests.ci_high)])[["id", "claim", "est", "ci", "n_items", "up", "down", "p", "p_holm", "pass"]].to_string(index=False), "\n")
    print(summary.round(3).T.to_string(), "\n")
    print(q1.round(3).T.to_string(), "\n")
    print(frames.round(3).to_string(index=False), "\n")
    print("Q2", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in q2.items()})


if __name__ == "__main__":
    main()
