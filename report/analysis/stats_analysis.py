"""NST2046 report statistics. Run through report/analysis/run_all.sh.

Reads existing logs only. Writes report/analysis/tables/*.csv and report/analysis/results.json.
Section numbers follow the statistics brief. Everything from section 5 on is exploratory.
"""

from __future__ import annotations

import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import optimize, stats
from statsmodels.genmod.cov_struct import Exchangeable

from common import (B, COMPARISONS, CONDITIONS, MODELS, ROOT, RUNS, SEED, TABLES, answer_token, auc, boot_indices, exact_signflip_p, holm,
                    final_letter, item_diff, load_cases, load_run, logit, mc_signflip_p, mcnemar_exact, mean_ci, pair_mean_ci,
                    probs_from_head, ratio_ci, spearman_boot)

TABLES.mkdir(parents=True, exist_ok=True)
R: dict = {}  # everything the results file quotes
pct = lambda x: round(100 * x)


def save(df: pd.DataFrame, name: str) -> pd.DataFrame:
    df.to_csv(TABLES / f"{name}.csv", index=False)
    return df


# ---------------------------------------------------------------------------- load

cases = load_cases()
frames = {k: load_run(k, cases) for k in RUNS}
main_all = frames["r4_main"]
fact = main_all[main_all["case_kind"] == "factual"].copy()
items = sorted(fact["case_id"].unique())
n_items = len(items)
IDX = boot_indices(n_items)
screened = sorted(frames["r3_longtail"].query("case_kind == 'factual'")["case_id"].unique())
new_items = [i for i in items if i not in screened]
fact["screened"] = fact["case_id"].isin(screened)
by_model = {m: fact[fact["model"] == m] for m in MODELS}

# ---------------------------------------------------------------------------- 1. verification

checks = []


def check(section, claim, readme, value, ok=None):
    good = (str(readme) == str(value)) if ok is None else bool(ok)
    checks.append({"section": section, "claim": claim, "readme": str(readme), "recomputed": str(value),
                   "status": "match" if good else "MISMATCH"})


# scoring against the published raw table
score_rows = []
for key, df in frames.items():
    raw = pd.read_csv(f"runs/{RUNS[key]}/raw_table.csv", usecols=["trial_id", "auto_score"])
    j = df.merge(raw, on="trial_id", how="left")
    score_rows.append({"run": key, "attempt_rows": df.attrs["attempts"], "trials": len(df),
                       "cost_usd": round(df.attrs["cost"], 2),
                       "scores_differ_from_raw_table": int((j["score"] != j["auto_score"]).sum())})
integrity = save(pd.DataFrame(score_rows), "t01_run_integrity")
R["integrity"] = integrity.to_dict("records")
R["n_scores_differ"] = int(integrity["scores_differ_from_raw_table"].sum())
R["total_cost"] = round(sum(d.attrs["cost"] for d in frames.values()), 2)
R["main_retry_rows"] = int(main_all.attrs["attempts"] - len(main_all))

for key, n in [("r1_pilot", 516), ("r4_main", 3552), ("r3_longtail", 576)]:
    check("3", f"trials in {key}", n, len(frames[key]))
check("3", "trials in round 2", 828, len(frames["r2_calibration"]) + len(frames["r2_calsmall"]))

rate = fact.groupby(["model", "condition"])["y"].mean().unstack()
corr = fact.groupby(["model", "condition"])["correct"].mean().unstack()
readme_rates = {
    "mistral-nemo": [15, 55, 48, 32, 16, 2], "mistral-small": [3, 16, 11, 11, 5, 2],
    "llama-8b": [14, 15, 26, 16, 16, 12], "gemma-moe": [0, 1, 2, 0, 0, 0],
    "qwen-small": [2, 3, 2, 2, 0, 0], "claude-sonnet": [0, 0, 0, 0, 0, 0],
}
for m, vals in readme_rates.items():
    for c, v in zip(CONDITIONS, vals):
        check("4 table", f"{m} {c} false rate %", v, pct(rate.loc[m, c]))


def flips(df, cond, ref):
    w = df[df["condition"].isin([cond, ref])].pivot_table(index=["case_id", "rep", "evidence_mode"], columns="condition",
                                                         values="y", aggfunc="first").dropna()
    return int(((w[cond] == 1) & (w[ref] == 0)).sum()), int(((w[cond] == 0) & (w[ref] == 1)).sum()), len(w)


readme_pairs = [
    ("mistral-nemo", "stored_incorrect", "no_belief", 41, 2), ("mistral-nemo", "stated_incorrect", "no_belief", 34, 2),
    ("mistral-nemo", "stored_incorrect_labelled", "stored_incorrect", 1, 23),
    ("mistral-nemo", "stored_incorrect_labelled", "no_belief", 20, 3),
    ("mistral-nemo", "stored_correct", "no_belief", 0, 12), ("mistral-nemo", "stated_incorrect", "stored_incorrect", 4, 11),
    ("mistral-small", "stored_incorrect", "no_belief", 12, 0), ("mistral-small", "stored_incorrect_labelled", "no_belief", 8, 0),
    ("llama-8b", "stated_incorrect", "no_belief", 14, 2), ("llama-8b", "stated_incorrect", "stored_incorrect", 12, 1),
]
for m, c, r, t, a in readme_pairs:
    tw, aw, _ = flips(by_model[m], c, r)
    check("4 paired", f"{m} {c} vs {r} flips (toward/away)", f"{t}/{a}", f"{tw}/{aw}")

d = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", items=items)
check("4", "Nemo items raised / lowered", "25/1", f"{int((d > 0).sum())}/{int((d < 0).sum())}")
d = item_diff(by_model["mistral-small"], "stored_incorrect", "no_belief", items=items)
check("4", "Mistral Small items raised", 8, int((d > 0).sum()))
check("4/5", "Qwen unreadable answers (all 592)", 15,
      int((main_all[main_all["model"] == "qwen-small"]["score"] == "unparseable").sum() +
          (main_all[main_all["model"] == "qwen-small"]["score"] == "error").sum()))
check("5", "Llama other-wrong answers (all 592)", 74,
      int((main_all[main_all["model"] == "llama-8b"]["score"] == "other_wrong").sum()))
check("5", "belief asserts false / denies true", "42/6",
      f"{sum(bool(cases[i].get('belief_affirms_false')) for i in items)}/"
      f"{sum(not cases[i].get('belief_affirms_false') for i in items)}")

useful = main_all[main_all["case_kind"] != "factual"]
u = useful.groupby(["model", "condition"]).agg(n=("score", "size"), right=("correct", "sum"),
                                               unreadable=("y", lambda s: int(s.isna().sum()))).reset_index()
save(u, "t02_useful_memory")
R["useful"] = {"trials": len(useful), "right": int(useful["correct"].sum()), "unreadable": int(useful["y"].isna().sum())}
check("4", "useful-memory checks all correct", "100%",
      f"{100 * useful['correct'].sum() / useful['correct'].notna().sum():.0f}% of readable "
      f"({int(useful['y'].isna().sum())} unreadable)", ok=useful["correct"].sum() == useful["correct"].notna().sum())

# Earlier rounds
pil = frames["r1_pilot"].query("case_kind == 'factual'")
for m in ["claude-sonnet", "qwen-large"]:
    check("3 r1", f"{m} right in every condition", "100%", f"{100 * pil[pil.model == m]['correct'].mean():.0f}%")
check("3 r1", "Llama wrong overall", "about 15%", f"{100 * (1 - pil[pil.model == 'llama-8b']['correct'].mean()):.0f}%",
      ok=abs((1 - pil[pil.model == "llama-8b"]["correct"].mean()) - 0.15) < 0.03)


def r2(model, mode):
    f = "r2_calibration" if model == "llama-8b" else "r2_calsmall"
    d = frames[f]
    d = d[(d["model"] == model) & (d["evidence_mode"].isin(mode))]
    return d.groupby("condition")["y"].mean()


x = r2("llama-8b", ["as_written", "none"])
check("3 r2", "Llama 34% -> 26% (README gives no evidence mode; this is pooled over both)", "34->26",
      f"{pct(x['no_belief'])}->{pct(x['stored_incorrect'])}")
x = r2("llama-8b", ["as_written"])
check("3 r2", "Llama 34% -> 26% if read as with-evidence only", "34->26", f"{pct(x['no_belief'])}->{pct(x['stored_incorrect'])}")
x = r2("mistral-nemo", ["as_written"])
check("3 r2", "Nemo with evidence", "37->40", f"{pct(x['no_belief'])}->{pct(x['stored_incorrect'])}")
x = r2("mistral-nemo", ["none"])
check("3 r2", "Nemo without evidence", "35->44", f"{pct(x['no_belief'])}->{pct(x['stored_incorrect'])}")
lt = frames["r3_longtail"]
x = lt[lt.model == "mistral-nemo"].groupby("condition")["y"].mean()
check("3 r3", "Nemo round 3", "19->60", f"{pct(x['no_belief'])}->{pct(x['stored_incorrect'])}")
t, a, _ = flips(lt[lt.model == "mistral-nemo"], "stored_incorrect", "no_belief")
check("3 r3", "Nemo round 3 flips", "21/1", f"{t}/{a}")
check("3 r3", "Nemo round 3 p", "~0.00001", f"{mcnemar_exact(t, a):.1e}", ok=mcnemar_exact(t, a) < 2e-5)
x = lt[lt.model == "gemma-moe"].groupby("condition")["y"].mean()
t, a, _ = flips(lt[lt.model == "gemma-moe"], "stored_incorrect", "no_belief")
check("3 r3", "Gemma round 3", "0->6, p=0.25", f"{pct(x['no_belief'])}->{pct(x['stored_incorrect'])}, p={mcnemar_exact(t, a):.2f}")
q = lt[lt.model == "qwen-large"]
R["qwen_large_r3_correct"] = float(q["correct"].mean())
R["claude_r3_correct"] = float(lt[lt.model == "claude-sonnet"]["correct"].mean())
check("4", "Qwen3.5-397B at ceiling in every round (round 3 correct rate vs Claude)",
      "matched Claude", f"{100 * q['correct'].mean():.1f}% vs {100 * R['claude_r3_correct']:.1f}%",
      ok=abs(q["correct"].mean() - R["claude_r3_correct"]) < 0.02)

check("0", "total API cost about $3.60", "about 3.60", f"{sum(d.attrs['cost'] for d in frames.values()):.2f}",
      ok=abs(sum(d.attrs["cost"] for d in frames.values()) - 3.6) < 0.06)
check("3", "round 1 cost", "0.87", f"{frames['r1_pilot'].attrs['cost']:.2f}")
check("3", "round 4 cost", "1.33", f"{frames['r4_main'].attrs['cost']:.2f}")
for needle, label in [("prime numbers", "primes"), ("hexagon", "hexagon"), ("seawater", "seawater"), ("fully independent", "Singapore")]:
    hits = [i for i in items if needle in cases[i]["question"].lower().replace("sea water", "seawater")]
    e = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", items=hits)
    check("4", f"README example '{label}': Nemo moved toward the belief", "yes", "yes" if len(hits) and (e > 0).all() else f"no ({e.to_dict()})")

# Run order. Timestamps in the logs, not manifests (manifests are rewritten on resume).
order = []
for key, df in frames.items():
    for m in df["model"].unique():
        g = df[df["model"] == m]
        order.append({"run": key, "model": m, "first_trial_utc": g["started_at"].min()[:16],
                      "last_trial_utc": g["started_at"].max()[:16]})
save(pd.DataFrame(order).sort_values("first_trial_utc"), "t03_run_chronology")
nemo_r3 = lt[lt.model == "mistral-nemo"]["started_at"].agg(["min", "max"]).tolist()
c_ = frames["r2_calsmall"]
nemo_r2 = c_[c_.model == "mistral-nemo"]["started_at"].agg(["min", "max"]).tolist()
R["chronology"] = {"nemo_r3_start": nemo_r3[0][:16], "nemo_r3_end": nemo_r3[1][:16], "nemo_r2_start": nemo_r2[0][:16],
                   "nemo_r2_end": nemo_r2[1][:16]}
check("3", "Round 2 small models ran before round 3 (Nemo first trial, r2 vs r3)", "r2 first",
      f"r3 {nemo_r3[0][11:16]}-{nemo_r3[1][11:16]} UTC, r2 {nemo_r2[0][11:16]}-{nemo_r2[1][11:16]} UTC",
      ok=nemo_r2[0] < nemo_r3[0])

# Prompt identity of the 24 items between rounds 3 and 4
j = fact[(fact.model == "mistral-nemo") & fact.condition.isin(["no_belief", "stored_incorrect"])].merge(
    lt[lt.model == "mistral-nemo"], on=["case_id", "condition", "rep"], suffixes=("_m", "_r"))
R["retest"] = {"pairs": len(j), "same_option_order": float((j["option_order_m"] == j["option_order_r"]).mean()),
               "same_answer": float((j["selected_m"] == j["selected_r"]).mean()),
               "p_inc_corr": float(j[["p_inc_m", "p_inc_r"]].corr().iloc[0, 1]),
               "p_inc_mean_abs_diff": float((j["p_inc_m"] - j["p_inc_r"]).abs().mean())}
R["round3_items_kept"] = bool(set(screened) <= set(items))
R["n_screened"], R["n_new"] = len(screened), len(new_items)

verdict = save(pd.DataFrame(checks), "t04_readme_checks")
R["checks"] = {"total": len(verdict), "mismatch": int((verdict.status == "MISMATCH").sum()),
               "mismatches": verdict[verdict.status == "MISMATCH"].to_dict("records")}

# ---------------------------------------------------------------------------- 2-3. paired tests and item CIs

naive = pd.read_csv(f"runs/{RUNS['r4_main']}/paired.csv")
rows = []
for m in MODELS:
    for cond, ref in COMPARISONS:
        t, a, n = flips(by_model[m], cond, ref)
        d = item_diff(by_model[m], cond, ref, items=items)
        ci = mean_ci(d.to_numpy(), IDX)
        w = by_model[m][by_model[m]["condition"].isin([cond, ref])].pivot_table(
            index=["case_id", "rep"], columns="condition", values="y", aggfunc="first").dropna()
        pair = (w[cond] - w[ref]).to_numpy()
        se_naive = pair.std(ddof=1) / np.sqrt(len(pair)) if len(pair) > 1 else np.nan
        rows.append({
            "model": m, "comparison": f"{cond} vs {ref}", "cond": cond, "ref": ref, "pairs": n, "toward": t, "away": a,
            "items_up": int((d > 0).sum()), "items_down": int((d < 0).sum()),
            "items_moved": int((d != 0).sum() - d.isna().sum()), "p_mcnemar": mcnemar_exact(t, a),
            "p_item": exact_signflip_p(d.to_numpy()), **ci,
            "se_trial": se_naive,
            "design_effect": (ci["se_boot"] / se_naive) ** 2 if se_naive and se_naive > 0 else np.nan,
        })
pt = pd.DataFrame(rows)
pt["p_holm_mcnemar"] = holm(pt["p_mcnemar"].to_numpy())
pt["p_holm_item"] = holm(pt["p_item"].to_numpy())
pt["survives_mcnemar"] = pt["p_holm_mcnemar"] < 0.05
pt["survives_item"] = pt["p_holm_item"] < 0.05
pt["survives_bonferroni"] = pt["p_mcnemar"] * len(pt) < 0.05
save(pt.sort_values("p_mcnemar"), "t05_holm_42_tests")
chk = naive.assign(comparison=naive["comparison"]).merge(pt, on=["model", "comparison"])
R["paired_csv_agrees"] = bool(np.allclose(chk["mcnemar_p"], chk["p_mcnemar"]) and len(chk) == 42)
R["n_tests"] = len(pt)
R["n_survive_mcnemar"] = int(pt["survives_mcnemar"].sum())
R["n_survive_item"] = int(pt["survives_item"].sum())
R["n_no_discordant"] = int(((pt.toward + pt.away) == 0).sum())

key = pt[pt["comparison"].isin(["stored_incorrect vs no_belief", "stored_incorrect_labelled vs stored_incorrect",
                                "stated_incorrect vs stored_incorrect", "stored_correct vs no_belief"])]
save(key, "t06_key_effects_item_ci")

# Rates per model and condition with item-level intervals (compare with the README's Wilson intervals)
rows = []
for m in MODELS:
    for c in CONDITIONS:
        g = by_model[m][by_model[m].condition == c]
        rt = g.groupby("case_id")["y"].mean().reindex(items).to_numpy()
        rows.append({"model": m, "condition": c, "usable": int(g["y"].notna().sum()), **mean_ci(rt, IDX),
                     "correct_rate": g["correct"].mean()})
save(pd.DataFrame(rows), "t31_rates_item_ci")

# Correct-answer version of the same contrasts: the false-option rate has a floor near zero.
rows = []
for m in MODELS:
    for cond, ref in COMPARISONS:
        d = item_diff(by_model[m], cond, ref, value="correct", items=items)
        rows.append({"model": m, "comparison": f"{cond} vs {ref}", **mean_ci(d.to_numpy(), IDX),
                     "p_item": exact_signflip_p(d.to_numpy())})
save(pd.DataFrame(rows), "t07_correct_rate_effects")

# How dependent are the two reps?
rows = []
for m in MODELS:
    for c in CONDITIONS:
        w = by_model[m][by_model[m].condition == c].pivot_table(index="case_id", columns="rep", values="y").dropna()
        y1, y2 = w[1].to_numpy(), w[2].to_numpy()
        phi = np.corrcoef(y1, y2)[0, 1] if y1.std() > 0 and y2.std() > 0 else np.nan
        rows.append({"model": m, "condition": c, "n_items": len(w), "rep_agreement": float((y1 == y2).mean()),
                     "rep_correlation": phi, "rep1_rate": y1.mean(), "rep2_rate": y2.mean()})
reps = save(pd.DataFrame(rows), "t08_rep_dependence")
rr = {}
for m in ["mistral-nemo", "mistral-small", "llama-8b"]:
    s = reps[reps.model == m]
    rr[m] = {"mean_corr": float(s["rep_correlation"].mean()), "min_corr": float(s["rep_correlation"].min()),
             "max_corr": float(s["rep_correlation"].max()), "agreement": float(s["rep_agreement"].mean())}
R["reps"] = rr
R["reps_same_order_items"] = int((fact.groupby(["case_id"])
                                  .apply(lambda g: g.groupby("rep")["option_order"].first().nunique() == 1,
                                         include_groups=False)).sum())
rows = []
for m in ["mistral-nemo", "mistral-small", "llama-8b"]:
    for cond, ref in [("stored_incorrect", "no_belief"), ("stored_incorrect_labelled", "stored_incorrect")]:
        for rep in (1, 2):
            d = item_diff(by_model[m][by_model[m].rep == rep], cond, ref, items=items)
            rows.append({"model": m, "comparison": f"{cond} vs {ref}", "rep": rep, **mean_ci(d.to_numpy(), IDX),
                         "p_item": exact_signflip_p(d.to_numpy())})
save(pd.DataFrame(rows), "t09_single_rep_estimates")

# Upper bound where nothing moved, since a bootstrap of all zeros returns a zero-width interval.
R["zero_upper_95"] = float(1 - 0.05 ** (1 / n_items))
# Fewest items, all moving one way, that could pass even the first Holm step (0.05 / 42).
R["min_items_to_pass_holm"] = int(next(k for k in range(1, 30) if 2.0 ** (1 - k) < 0.05 / 42))

# Qwen: worst-case handling of unreadable answers
qw = by_model["qwen-small"]
bounds = {}
for name, fill_stored, fill_base in [("excluded", None, None), ("all unreadable stored=false, base=not false", 1, 0),
                                     ("all unreadable stored=not false, base=false", 0, 1)]:
    q = qw.copy()
    if fill_stored is not None:
        q.loc[q.condition.eq("stored_incorrect") & q.y.isna(), "y"] = fill_stored
        q.loc[q.condition.eq("no_belief") & q.y.isna(), "y"] = fill_base
    bounds[name] = float(item_diff(q, "stored_incorrect", "no_belief", items=items).mean())
R["qwen_bounds"] = bounds

# Parser sensitivity: first answer line vs final answer line
rows = []
for m in MODELS:
    g = by_model[m]
    for c in CONDITIONS:
        s = g[g.condition == c]
        rows.append({"model": m, "condition": c, "final_rate": s["y"].mean(), "first_line_rate": s["y_first"].mean(),
                     "self_corrections": int(((s["selected"] != s["selected_first"]) & s["selected_first"].notna() &
                                              s["selected"].notna()).sum())})
fl = save(pd.DataFrame(rows), "t10_first_vs_final_answer")
R["gemma_first"] = {c: float(fl[(fl.model == "gemma-moe") & (fl.condition == c)]["first_line_rate"].iloc[0]) for c in CONDITIONS}
R["gemma_final"] = {c: float(fl[(fl.model == "gemma-moe") & (fl.condition == c)]["final_rate"].iloc[0]) for c in CONDITIONS}
R["gemma_corrections"] = {c: int(fl[(fl.model == "gemma-moe") & (fl.condition == c)]["self_corrections"].iloc[0]) for c in CONDITIONS}
g_ = by_model["gemma-moe"]
g_d = item_diff(g_, "stored_incorrect", "no_belief", value="y_first", items=items)
R["gemma_first_effect"] = {**mean_ci(g_d.to_numpy(), IDX), "p_item": exact_signflip_p(g_d.to_numpy()),
                           "items_up": int((g_d > 0).sum())}
g_d = item_diff(g_, "stated_incorrect", "no_belief", value="y_first", items=items)
R["gemma_first_effect_stated"] = {**mean_ci(g_d.to_numpy(), IDX), "p_item": exact_signflip_p(g_d.to_numpy()),
                                  "items_up": int((g_d > 0).sum())}

# Where do Nemo's false answers come from?
rows = []
for m in ["mistral-nemo", "mistral-small"]:
    for col in ["y", "correct", "other"]:
        d = item_diff(by_model[m], "stored_incorrect", "no_belief", value=col, items=items)
        rows.append({"model": m, "outcome": {"y": "false option", "correct": "correct", "other": "other wrong"}[col],
                     "no_belief": by_model[m].query("condition == 'no_belief'")[col].mean(),
                     "stored_incorrect": by_model[m].query("condition == 'stored_incorrect'")[col].mean(),
                     **mean_ci(d.to_numpy(), IDX)})
save(pd.DataFrame(rows), "t11_outcome_decomposition")

# Influence and subgroup sensitivity for the headline Nemo effect
nd = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", items=items)
loo = [(i, float(nd.drop(i).mean())) for i in items]
R["nemo_loo"] = {"min": min(v for _, v in loo), "max": max(v for _, v in loo)}
top = nd.sort_values(ascending=False)
R["nemo_top5_share"] = float(top.iloc[:5].sum() / nd.sum())
R["nemo_top10_share"] = float(top.iloc[:10].sum() / nd.sum())
rows = []
meta = pd.DataFrame({"case_id": items,
                     "category": [cases[i]["category"] for i in items],
                     "asserts_false": [bool(cases[i].get("belief_affirms_false")) for i in items],
                     "note": [str(cases[i].get("notes", "")) for i in items]}).set_index("case_id")
meta["convention_note"] = meta["note"].str.contains(r"\bdepends?\b|convention", case=False, regex=True)
for label, mask in [("all 48 items", pd.Series(True, index=items)), *[(f"category: {c}", meta.category == c)
                    for c in ["science", "general", "numerical"]],
                    ("belief asserts something false", meta.asserts_false),
                    ("belief denies something true", ~meta.asserts_false),
                    ("items without a counting/convention note", ~meta.convention_note)]:
    sub = nd[mask.reindex(items).values]
    rows.append({"subset": label, "items": len(sub), "effect": sub.mean(), "items_up": int((sub > 0).sum()),
                 "items_down": int((sub < 0).sum()), "p_item": exact_signflip_p(sub.to_numpy())})
save(pd.DataFrame(rows), "t12_nemo_subgroups")
R["n_convention_items"] = int(meta.convention_note.sum())

# ---------------------------------------------------------------------------- 4. model x condition


def wald(res, names):
    b = res.params[names].to_numpy()
    v = res.cov_params().loc[names, names].to_numpy()
    try:
        stat = float(b @ np.linalg.solve(v, b))
    except np.linalg.LinAlgError:
        return np.nan, np.nan
    return stat, float(stats.chi2.sf(stat, len(names)))


def fit_gee(models, conds, tag):
    d = fact[fact.model.isin(models) & fact.condition.isin(conds)].dropna(subset=["y"]).copy()
    d["group"] = d["case_id"].astype("category").cat.codes
    d = d.sort_values(["group", "model", "condition", "rep"]).reset_index(drop=True)
    f = (f"y ~ C(model, Treatment('{models[0]}')) * C(condition, Treatment('no_belief'))")
    out = {"tag": tag, "models": models, "conditions": conds, "rows": len(d),
           "events_by_cell_min": int(d.groupby(["model", "condition"])["y"].sum().min())}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            mod = sm.GEE.from_formula(f, groups="group", data=d, family=sm.families.Binomial(), cov_struct=Exchangeable())
            res = mod.fit(maxiter=200, cov_type="robust")
            names = [n for n in res.params.index if ":" in n]
            out["converged"] = bool(getattr(res, "converged", True)) if hasattr(res, "converged") else True
            stat, p = wald(res, names)
            out.update(chi2_robust=stat, df=len(names), p_robust=p, max_abs_coef=float(res.params.abs().max()),
                       max_se=float(res.bse.max()), working_corr=float(res.cov_struct.dep_params))
            res2 = mod.fit(maxiter=200, cov_type="bias_reduced")
            stat2, p2 = wald(res2, names)
            out.update(chi2_bias_reduced=stat2, p_bias_reduced=p2)
            out["coefs"] = pd.DataFrame({"term": res2.params.index, "log_or": res2.params.values, "se": res2.bse.values}
                                        ).to_dict("records")
        except Exception as e:  # recorded, not hidden: this is the expected failure on sparse models
            out["failed"] = f"{type(e).__name__}: {e}"
    msgs = sorted({str(w.message)[:90] for w in caught})
    out["warnings"] = msgs[:4]
    return out


R["gee"] = {
    "three_models_two_conditions": fit_gee(["mistral-nemo", "mistral-small", "llama-8b"], ["no_belief", "stored_incorrect"], "A"),
    "two_mistrals_two_conditions": fit_gee(["mistral-nemo", "mistral-small"], ["no_belief", "stored_incorrect"], "B"),
    "three_models_all_conditions": fit_gee(["mistral-nemo", "mistral-small", "llama-8b"], CONDITIONS, "C"),
    "five_models_two_conditions": fit_gee(["mistral-nemo", "mistral-small", "llama-8b", "gemma-moe", "qwen-small"],
                                          ["no_belief", "stored_incorrect"], "D"),
    "six_models_two_conditions": fit_gee(MODELS, ["no_belief", "stored_incorrect"], "E"),
}

# Model-free tests on the risk-difference scale (cannot fail on sparse models).
E = pd.DataFrame({m: item_diff(by_model[m], "stored_incorrect", "no_belief", items=items) for m in MODELS})


def perm_heterogeneity(mat: np.ndarray, b=200_000, seed=SEED) -> tuple[float, float]:
    mat = np.nan_to_num(mat, nan=0.0)
    obs = np.nanmean(mat, axis=0).var()
    rng = np.random.default_rng(seed)
    count, chunk = 0, 20_000
    for _ in range(b // chunk):
        order = rng.random((chunk, mat.shape[0], mat.shape[1])).argsort(axis=2)
        shuffled = mat[np.arange(mat.shape[0])[None, :, None], order]
        count += (shuffled.mean(axis=1).var(axis=1) >= obs - 1e-12).sum()
    return float(obs), float((1 + count) / (b // chunk * chunk + 1))


R["perm_all_six"] = dict(zip(["stat", "p"], perm_heterogeneity(E[MODELS].to_numpy())))
R["perm_excl_nemo"] = dict(zip(["stat", "p"], perm_heterogeneity(E[[m for m in MODELS if m != "mistral-nemo"]].to_numpy())))

counts = {}
for m in MODELS:
    g = by_model[m]
    for c in CONDITIONS:
        s = g[g.condition == c].dropna(subset=["y"]).groupby("case_id")["y"].agg(["sum", "count"]).reindex(items).fillna(0)
        counts[(m, c)] = s


def log_or(m, cond="stored_incorrect", ref="no_belief", index=None):
    """Log odds ratio with the 0.5 Haldane correction, optionally on a resampled item index."""
    a, b = counts[(m, cond)], counts[(m, ref)]
    if index is None:
        ka, na, kb, nb = a["sum"].sum(), a["count"].sum(), b["sum"].sum(), b["count"].sum()
    else:
        ka, na = a["sum"].to_numpy()[index].sum(axis=-1), a["count"].to_numpy()[index].sum(axis=-1)
        kb, nb = b["sum"].to_numpy()[index].sum(axis=-1), b["count"].to_numpy()[index].sum(axis=-1)
    return np.log((ka + .5) / (na - ka + .5)) - np.log((kb + .5) / (nb - kb + .5))


rows = []
for i, a in enumerate(MODELS):
    for b in MODELS[i + 1:]:
        D = (E[a] - E[b]).to_numpy()
        ci = mean_ci(D, IDX)
        la, lb = log_or(a), log_or(b)
        ba, bb = log_or(a, index=IDX), log_or(b, index=IDX)
        rows.append({"contrast": f"{a} minus {b}", "rd_diff": ci["est"], "rd_low": ci["ci_low"], "rd_high": ci["ci_high"],
                     "items_differ": int(np.nansum(D != 0)), "p_item": exact_signflip_p(D),
                     "log_or_diff": la - lb, "log_or_low": float(np.quantile(ba - bb, .025)),
                     "log_or_high": float(np.quantile(ba - bb, .975))})
pw = pd.DataFrame(rows)
pw["p_holm"] = holm(pw["p_item"].to_numpy())
save(pw, "t13_model_contrasts_stored_vs_baseline")

rows = []
for m in MODELS:
    a_, b_ = counts[(m, "stored_incorrect")]["sum"].sum(), counts[(m, "no_belief")]["sum"].sum()
    rows.append({"model": m, "false_answers_stored": int(a_), "false_answers_baseline": int(b_),
                 # With almost no events the 0.5 correction, not the data, sets the ratio.
                 "estimable": bool(min(a_, b_) >= 3), "log_or": log_or(m), "or": float(np.exp(log_or(m))),
                 "or_low": float(np.exp(np.quantile(log_or(m, index=IDX), .025))),
                 "or_high": float(np.exp(np.quantile(log_or(m, index=IDX), .975)))})
save(pd.DataFrame(rows), "t14_odds_ratios_stored_vs_baseline")

# Does the channel (stored vs stated) work differently across models?
S = pd.DataFrame({m: item_diff(by_model[m], "stated_incorrect", "stored_incorrect", items=items) for m in MODELS})
rows = []
for a, b in [("llama-8b", "mistral-nemo"), ("llama-8b", "mistral-small"), ("mistral-nemo", "mistral-small")]:
    D = (S[a] - S[b]).to_numpy()
    rows.append({"contrast": f"(stated - stored): {a} minus {b}", **mean_ci(D, IDX), "p_item": exact_signflip_p(D)})
save(pd.DataFrame(rows), "t15_channel_by_model")

# ---------------------------------------------------------------------------- 5. mechanism (exploratory)

nb = fact[fact.condition == "no_belief"].set_index(["model", "case_id", "rep"])
rows = []
for m in MODELS:
    g = by_model[m]
    base = g[g.condition == "no_belief"]
    p = base["pmax"].dropna()
    r1 = base[base.rep == 1].set_index("case_id")["p_inc"]
    r2_ = base[base.rep == 2].set_index("case_id")["p_inc"]
    both = pd.concat([r1, r2_], axis=1, keys=["a", "b"]).dropna()
    rows.append({"model": m, "trials_with_probs": len(p), "logged": int((g["prob_source"] == "logged").sum()),
                 "recovered": int((g["prob_source"] == "recovered").sum()),
                 "mean_top_prob": p.mean() if len(p) else np.nan, "share_top_prob_over_099": (p > .99).mean() if len(p) else np.nan,
                 "share_top_prob_under_090": (p < .9).mean() if len(p) else np.nan,
                 "rep_corr_false_prob": both.corr().iloc[0, 1] if len(both) > 3 else np.nan,
                 "has_reasoning": float(g["has_reasoning"].mean())})
cov = save(pd.DataFrame(rows), "t16_probability_coverage")
R["coverage"] = cov.to_dict("records")

# Mistral Small: logged vs recovered probabilities, and whether logging failure is related to anything
ms = by_model["mistral-small"].copy()
ms["logged"] = (ms["prob_source"] == "logged").astype(float)
R["ms_recover"] = {
    "n_trials": len(ms), "n_logged": int(ms.logged.sum()), "n_recovered": int((ms.prob_source == "recovered").sum()),
    "logged_rate_false_chosen": float(ms[ms.y == 1]["logged"].mean()), "logged_rate_not_false": float(ms[ms.y == 0]["logged"].mean()),
    "chi2_p_condition": float(stats.chi2_contingency(pd.crosstab(ms.condition, ms.logged))[1]),
    "chi2_p_choice": float(stats.chi2_contingency(pd.crosstab(ms.y, ms.logged))[1]),
    "rate_false_logged_subset_stored": float(ms[(ms.logged == 1) & (ms.condition == "stored_incorrect")]["y"].mean()),
    "rate_false_all_stored": float(ms[ms.condition == "stored_incorrect"]["y"].mean()),
    "rate_false_missing_subset_stored": float(ms[(ms.logged == 0) & (ms.condition == "stored_incorrect")]["y"].mean()),
}

# Reproducible versions of the recovery checks
_raw = [json.loads(line) for line in (ROOT / "runs" / RUNS["r4_main"] / "trials.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
_raw = list({r["trial_id"]: r for r in _raw}.values())
_ms = [r for r in _raw if r["model_alias"] == "mistral-small" and r.get("case_kind") == "factual"]
_diffs, _letter_ok, _prefix_ok = [], [], []
for r in _ms:
    rec = probs_from_head(r["logprobs_head"], r["option_map"])
    if isinstance(r.get("option_probs"), dict):
        _diffs.append(max(abs(rec[k] - v) for k, v in r["option_probs"].items()))
    else:
        head_text = "".join(t["token"] for t in r["logprobs_head"]).strip()
        _prefix_ok.append(r["response_text"].strip().startswith(head_text))
    _letter_ok.append(answer_token(r["logprobs_head"], r["option_map"]) == final_letter(r["response_text"], list(r["option_map"])))
R["ms_recover"].update(max_diff_when_both=float(max(_diffs)), letter_match_rate=float(np.mean(_letter_ok)),
                       head_prefix_rate=float(np.mean(_prefix_ok)))

BANDS = ["Confident and correct", "Unsure (top option under 90%)", "Confident and wrong"]


def band(row):
    if row["pmax"] < .9:
        return BANDS[1]
    return BANDS[0] if row["p_ans"] >= .9 else BANDS[2]


def pairs_for(m, cond="stored_incorrect", ref="no_belief"):
    g = by_model[m]
    a = g[g.condition == ref].set_index(["case_id", "rep"])
    b = g[g.condition == cond].set_index(["case_id", "rep"])
    j = a.merge(b, left_index=True, right_index=True, how="inner", suffixes=("_b", "_s"))
    j = j.dropna(subset=["p_inc_b", "p_inc_s"]).reset_index()
    j["delta"] = j["p_inc_s"] - j["p_inc_b"]
    j["unc"] = 1 - j["pmax_b"]
    j["flip"] = ((j["y_b"] == 0) & (j["y_s"] == 1)).astype(float)
    j["at_risk"] = j["y_b"] == 0
    j["band"] = j.apply(lambda r: band({"pmax": r["pmax_b"], "p_ans": r["p_ans_b"]}), axis=1)
    return j


def item_mean(j, col):
    return j.groupby("case_id")[col].mean().reindex(items)


mech_rows, band_rows, shift_rows = [], [], []
for m in ["mistral-nemo", "mistral-small", "gemma-moe", "qwen-small"]:
    j = pairs_for(m)
    U = item_mean(j, "unc")
    H = item_mean(j, "entropy_b")
    D = item_mean(j, "delta")
    # Three versions of the key correlation. The second and third avoid re-using the noise in the baseline.
    res = {"model": m, "items": int(D.notna().sum()), "mean_shift": float(D.mean()),
           "share_items_any_uncertainty": float((U > .1).mean())}
    res.update({f"rho_{k}": v for k, v in spearman_boot(U, D, IDX).items() if k != "n"})
    a = j[j.rep == 1].set_index("case_id")
    b = j[j.rep == 2].set_index("case_id")
    cf = []
    for x, y in [(a, b), (b, a)]:
        c = pd.concat([x["unc"], y["delta"]], axis=1).dropna()
        if len(c) > 3 and c["unc"].std() > 0:
            cf.append(stats.spearmanr(c["unc"], c["delta"]).statistic)
    res["rho_crossrep"] = float(np.mean(cf)) if cf else np.nan
    g = by_model[m]
    alt = (g[g.condition == "stored_incorrect"].groupby("case_id")["p_inc"].mean() -
           g[g.condition == "stored_unrelated"].groupby("case_id")["p_inc"].mean()).reindex(items)
    x = pd.concat([U, alt], axis=1).dropna()
    res["rho_vs_unrelated_baseline"] = float(stats.spearmanr(x.iloc[:, 0], x.iloc[:, 1]).statistic) if x.iloc[:, 0].std() > 0 else np.nan
    # Flip prediction: at-risk pairs only (model did not already give the false answer at baseline)
    r = j[j.at_risk]
    res.update(at_risk_pairs=len(r), flips=int(r["flip"].sum()), auc_uncertainty=auc(r["unc"], r["flip"]),
               auc_false_prob=auc(logit(r["p_inc_b"]), r["flip"]))
    res["auc_uncertainty_low"], res["auc_uncertainty_high"] = np.nan, np.nan
    res["auc_false_low"], res["auc_false_high"] = np.nan, np.nan
    if r["flip"].sum() >= 5:
        groups = {k: v for k, v in r.groupby("case_id")}
        keys = items
        au, af = [], []
        for row in IDX[:4000]:
            s = pd.concat([groups[keys[i]] for i in row if keys[i] in groups])
            au.append(auc(s["unc"], s["flip"]))
            af.append(auc(logit(s["p_inc_b"]), s["flip"]))
        res["auc_uncertainty_low"], res["auc_uncertainty_high"] = [float(v) for v in np.nanquantile(au, [.025, .975])]
        res["auc_false_low"], res["auc_false_high"] = [float(v) for v in np.nanquantile(af, [.025, .975])]
    res["logit_shift_vs_unc_rho"] = float(stats.spearmanr(U, item_mean(j.assign(ds=logit(j.p_inc_s) - logit(j.p_inc_b)), "ds"),
                                                          nan_policy="omit").statistic) if U.std() > 0 else np.nan
    mech_rows.append(res)

    total = j["delta"].sum()
    for bname in BANDS:
        s = j[j["band"] == bname]
        if not len(s):
            continue
        ci = pair_mean_ci(s, "delta", items, IDX)
        ar = s[s.at_risk]
        band_rows.append({"model": m, "band": bname, "pairs": len(s), "items": s["case_id"].nunique(),
                          "mean_false_prob_base": s["p_inc_b"].mean(), "mean_false_prob_stored": s["p_inc_s"].mean(),
                          "mean_shift": ci["est"], "shift_ci_low": ci["ci_low"], "shift_ci_high": ci["ci_high"],
                          "share_of_total_shift": s["delta"].sum() / total if total else np.nan,
                          "at_risk_pairs": len(ar), "flips": int(ar["flip"].sum()),
                          "flip_rate": ar["flip"].mean() if len(ar) else np.nan})

    # Probability shift with the chosen answer unchanged (MS1 prediction), with the unrelated memory as placebo
    for cond, nm in [("stored_incorrect", "stored false belief"), ("stored_incorrect_labelled", "stored + label"),
                     ("stored_unrelated", "unrelated memory (placebo)")]:
        p = pairs_for(m, cond)
        same = p[p["selected_b"] == p["selected_s"]]
        for lab, sub in [("all pairs", p), ("chosen answer unchanged", same),
                         ("correct in both", same[same["selected_b"] == same["case_id"].map(lambda c: cases[c]["answer"])])]:
            di = sub.groupby("case_id")["delta"].mean().reindex(items)
            ci = pair_mean_ci(sub, "delta", items, IDX)
            ratio = np.exp((np.log(sub["p_inc_s"].clip(1e-6)) - np.log(sub["p_inc_b"].clip(1e-6))).mean())
            shift_rows.append({"model": m, "memory": nm, "subset": lab, "pairs": len(sub), "items": int(di.notna().sum()),
                               "mean_shift": ci["est"], "ci_low": ci["ci_low"], "ci_high": ci["ci_high"],
                               "median_shift": sub["delta"].median(), "share_up": (sub["delta"] > 0).mean(),
                               "geo_mean_ratio": float(ratio), "p_item_mc": mc_signflip_p(di.to_numpy())})

# Sensitivity to the 90% cut-off, which was chosen after seeing the data, and where flips actually sit
R["cutoff_sensitivity"] = {}
for m in ["mistral-nemo", "mistral-small"]:
    j = pairs_for(m)
    tot = j["delta"].sum()
    res = {}
    for cut in (0.8, 0.9, 0.95, 0.99):
        conf = j[(j["pmax_b"] >= cut) & (j["p_ans_b"] >= cut)]
        res[str(cut)] = {"pairs": len(conf), "share_of_shift": float(conf["delta"].sum() / tot), "flips": int(conf["flip"].sum())}
    r = j[j.at_risk]
    res["median_top_prob_flipped"] = float(r[r.flip == 1]["pmax_b"].median())
    res["median_top_prob_not_flipped"] = float(r[r.flip == 0]["pmax_b"].median())
    R["cutoff_sensitivity"][m] = res

mech = save(pd.DataFrame(mech_rows), "t17_mechanism_uncertainty")
bands = save(pd.DataFrame(band_rows), "t18_mechanism_by_confidence_band")
shifts = save(pd.DataFrame(shift_rows), "t19_shift_without_answer_change")

# Constant-boost null: add the same log-odds to the false option on every item. If this reproduces the
# pattern, "memory works where the model is unsure" is what a sigmoid does anyway, not a separate mechanism.
rows, nulls = [], {}
for m in ["mistral-nemo", "mistral-small"]:
    j = pairs_for(m)
    pb = j["p_inc_b"].clip(1e-6, 1 - 1e-6).to_numpy()
    target = j["p_inc_s"].mean()
    fn = lambda dl: (pb * np.exp(dl) / (1 - pb + pb * np.exp(dl))).mean() - target
    dl = optimize.brentq(fn, -5, 25)
    j["pred_s"] = pb * np.exp(dl) / (1 - pb + pb * np.exp(dl))
    j["pred_delta"] = j["pred_s"] - j["p_inc_b"]
    obs = item_mean(j, "delta")
    pred = item_mean(j, "pred_delta")
    U = item_mean(j, "unc")
    nulls[m] = {"boost_log_odds": float(dl), "boost_odds_ratio": float(np.exp(dl)),
                "rho_pred_obs": float(stats.spearmanr(pred, obs).statistic),
                "rho_unc_predicted": float(stats.spearmanr(U, pred).statistic),
                "rho_unc_observed": float(stats.spearmanr(U, obs).statistic)}
    for bname in BANDS:
        s = j[j["band"] == bname]
        rows.append({"model": m, "band": bname, "observed": s["delta"].mean(), "predicted_constant_boost": s["pred_delta"].mean(),
                     "pairs": len(s)})
    j[["case_id", "rep", "unc", "delta", "pred_delta", "band", "flip", "at_risk", "p_inc_b", "p_inc_s", "p_ans_b"]].assign(model=m).to_csv(
        TABLES / f"fig_mechanism_pairs_{m}.csv", index=False)
save(pd.DataFrame(rows), "t20_constant_boost_null")
R["constant_boost"] = nulls

# Mistral Small sensitivity: the 278 recovered trials dropped, logged probabilities only.
ms_log = by_model["mistral-small"][by_model["mistral-small"]["prob_source"] == "logged"]
ms_base = ms_log[ms_log.condition == "no_belief"].set_index(["case_id", "rep"])
ms_st = ms_log[ms_log.condition == "stored_incorrect"].set_index(["case_id", "rep"])
ms_j = ms_base.merge(ms_st, left_index=True, right_index=True, how="inner", suffixes=("_b", "_s")).reset_index()
ms_j["delta"] = ms_j["p_inc_s"] - ms_j["p_inc_b"]
ms_j["unc"] = 1 - ms_j["pmax_b"]
ms_i = ms_j.groupby("case_id")[["delta", "unc"]].mean()
R["ms_logged_only"] = {"pairs": len(ms_j), "items": len(ms_i), "mean_shift": float(ms_j["delta"].mean()),
                       "rho": float(stats.spearmanr(ms_i["unc"], ms_i["delta"]).statistic),
                       "mean_p_stored_logged": float(ms_log[ms_log.condition == "stored_incorrect"]["p_inc"].mean()),
                       "mean_p_stored_all": float(by_model["mistral-small"].query("condition == 'stored_incorrect'")["p_inc"].mean())}

# Between-model view: does a less accurate model move more?
rows = []
for m in MODELS:
    g = by_model[m]
    rows.append({"model": m, "baseline_correct": g[g.condition == "no_belief"]["correct"].mean(),
                 "stored_effect": item_diff(g, "stored_incorrect", "no_belief", items=items).mean(),
                 "stated_effect": item_diff(g, "stated_incorrect", "no_belief", items=items).mean()})
save(pd.DataFrame(rows), "t30_model_level_accuracy_vs_effect")

# Do the same items move in different models?
up = {m: item_diff(by_model[m], "stored_incorrect", "no_belief", items=items) > 0 for m in ["mistral-nemo", "mistral-small"]}
tab = pd.crosstab(up["mistral-nemo"], up["mistral-small"])
R["item_overlap"] = {"nemo_up": int(up["mistral-nemo"].sum()), "small_up": int(up["mistral-small"].sum()),
                     "both": int((up["mistral-nemo"] & up["mistral-small"]).sum()),
                     "fisher_p": float(stats.fisher_exact(tab.to_numpy())[1])}
ls = item_diff(by_model["llama-8b"], "stated_incorrect", "no_belief", items=items) > 0
ns = item_diff(by_model["mistral-nemo"], "stated_incorrect", "no_belief", items=items) > 0
R["item_overlap_stated"] = {"llama_up": int(ls.sum()), "nemo_up": int(ns.sum()), "both": int((ls & ns).sum()),
                            "fisher_p": float(stats.fisher_exact(pd.crosstab(ls, ns).to_numpy())[1])}

# Baseline accuracy version, usable for Llama too. Effect measured against the unrelated-memory arm so
# the baseline trials that define the groups are not also the trials that define the effect.
rows = []
for m in ["mistral-nemo", "mistral-small", "llama-8b"]:
    g = by_model[m]
    acc = g[g.condition == "no_belief"].groupby("case_id")["correct"].mean().reindex(items)
    for level, name in [(1.0, "right both times"), (0.5, "right once"), (0.0, "wrong both times")]:
        mask = acc == level
        if not mask.any():
            continue
        sub = [i for i in items if mask[i]]
        s = g[g.case_id.isin(sub)]
        d_ = item_diff(s, "stored_incorrect", "stored_unrelated", items=sub)
        d2 = item_diff(s, "stored_incorrect", "no_belief", items=sub)
        idx = boot_indices(len(sub), 5000)
        ci = mean_ci(d_.to_numpy(), idx)
        rows.append({"model": m, "baseline_accuracy_group": name, "items": len(sub),
                     "false_rate_unrelated": s[s.condition == "stored_unrelated"]["y"].mean(),
                     "false_rate_stored": s[s.condition == "stored_incorrect"]["y"].mean(),
                     "effect_vs_unrelated": ci["est"], "ci_low": ci["ci_low"], "ci_high": ci["ci_high"],
                     "effect_vs_no_belief": d2.mean()})
save(pd.DataFrame(rows), "t21_mechanism_by_baseline_accuracy")

# ---------------------------------------------------------------------------- 6. label effect

rows = []
stack = {}
for m in ["mistral-nemo", "mistral-small"]:
    g = by_model[m]
    for measure, col in [("false answers chosen", "y"), ("probability on false option", "p_inc")]:
        s = g[g.condition == "stored_incorrect"].groupby("case_id")[col].mean().reindex(items)
        lb = g[g.condition == "stored_incorrect_labelled"].groupby("case_id")[col].mean().reindex(items)
        b = g[g.condition == "no_belief"].groupby("case_id")[col].mean().reindex(items)
        stack[(m, col)] = (s, lb, b)
        res = ratio_ci((s - lb).to_numpy(), (s - b).to_numpy(), IDX)
        resid = mean_ci((lb - b).to_numpy(), IDX)
        rows.append({"model": m, "measure": measure, "baseline": b.mean(), "stored": s.mean(), "labelled": lb.mean(), **res,
                     "residual_above_baseline": resid["est"], "residual_low": resid["ci_low"], "residual_high": resid["ci_high"]})
    # correct answers restored
    s = g[g.condition == "stored_incorrect"].groupby("case_id")["correct"].mean().reindex(items)
    lb = g[g.condition == "stored_incorrect_labelled"].groupby("case_id")["correct"].mean().reindex(items)
    b = g[g.condition == "no_belief"].groupby("case_id")["correct"].mean().reindex(items)
    res = ratio_ci((lb - s).to_numpy(), (b - s).to_numpy(), IDX)
    resid = mean_ci((b - lb).to_numpy(), IDX)
    rows.append({"model": m, "measure": "correct answers restored", "baseline": b.mean(), "stored": s.mean(), "labelled": lb.mean(), **res,
                 "residual_above_baseline": resid["est"], "residual_low": resid["ci_low"], "residual_high": resid["ci_high"]})
# Pooled Mistrals
s = stack[("mistral-nemo", "y")][0] + stack[("mistral-small", "y")][0]
lb = stack[("mistral-nemo", "y")][1] + stack[("mistral-small", "y")][1]
b = stack[("mistral-nemo", "y")][2] + stack[("mistral-small", "y")][2]
res = ratio_ci((s - lb).to_numpy(), (s - b).to_numpy(), IDX)
rows.append({"model": "both Mistrals pooled", "measure": "false answers chosen", "baseline": b.mean() / 2, "stored": s.mean() / 2,
             "labelled": lb.mean() / 2, **res})
lab = save(pd.DataFrame(rows), "t22_label_effect")
# Do the two Mistrals differ in how much the label removes?
s1, l1, b1 = stack[("mistral-nemo", "y")]
s2, l2, b2 = stack[("mistral-small", "y")]
f1 = ((s1 - l1).to_numpy()[IDX].mean(1)) / (s1 - b1).to_numpy()[IDX].mean(1)
with np.errstate(divide="ignore", invalid="ignore"):
    den2 = (s2 - b2).to_numpy()[IDX].mean(1)
    f2 = np.where(den2 > 0, (s2 - l2).to_numpy()[IDX].mean(1) / den2, np.nan)
R["label_diff_mistrals"] = {"p50": float(np.nanmedian(f1 - f2)), "low": float(np.nanquantile(f1 - f2, .025)), "high": float(np.nanquantile(f1 - f2, .975))}
# Item view of the label for Nemo
nl = item_diff(by_model["mistral-nemo"], "stored_incorrect_labelled", "stored_incorrect", items=items)
ne = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", items=items)
moved = ne > 0
R["nemo_label_items"] = {"moved_items": int(moved.sum()), "moved_items_label_helped": int((nl[moved] < 0).sum()),
                         "moved_items_label_no_change": int((nl[moved] == 0).sum()), "moved_items_label_worse": int((nl[moved] > 0).sum()),
                         "moved_items_fully_back": int(((by_model["mistral-nemo"].query("condition == 'stored_incorrect_labelled'").groupby("case_id")["y"].mean() <=
                                                         by_model["mistral-nemo"].query("condition == 'no_belief'").groupby("case_id")["y"].mean()).reindex(items)[moved]).sum())}

# ---------------------------------------------------------------------------- 7. rounds (post hoc)

ROUND_ROWS = [
    ("Round 1 pilot (misconceptions, evidence)", "r1_pilot", ["as_written"]),
    ("Round 2 harder items, evidence", None, ["as_written"]),
    ("Round 2 harder items, no evidence", None, ["none"]),
    ("Round 3 long-tail (24 items)", "r3_longtail", ["as_written"]),
    ("Round 4 main, screened 24", "r4_main", ["as_written"]),
    ("Round 4 main, new 24", "r4_main", ["as_written"]),
    ("Round 4 main, all 48", "r4_main", ["as_written"]),
]
rows, pools = [], {}
for model in ["mistral-nemo", "llama-8b"]:
    for name, key, modes in ROUND_ROWS:
        if key is None:
            key_ = "r2_calsmall" if model == "mistral-nemo" else "r2_calibration"
        else:
            key_ = key
        d_ = frames[key_]
        g = d_[(d_.model == model) & d_.evidence_mode.isin(modes) & (d_.case_kind == "factual")]
        if name.endswith("screened 24"):
            g = g[g.case_id.isin(screened)]
        if name.endswith("new 24"):
            g = g[g.case_id.isin(new_items)]
        if g.empty:
            rows.append({"model": model, "round": name, "note": "model not in this round"})
            continue
        its = sorted(g.case_id.unique())
        d1 = item_diff(g, "stored_incorrect", "no_belief", items=its)
        idx = boot_indices(len(its))
        ci = mean_ci(d1.to_numpy(), idx)
        base = g[g.condition == "no_belief"]
        st = g[g.condition == "stored_incorrect"]
        # "conversion": of the answers that were not already the false option, what share did the memory capture?
        conv_den = 1 - base["y"].mean()
        pools[(model, name)] = (d1, base["y"].groupby(base.case_id).mean().reindex(its))
        band_p = base["pmax"].dropna() if model == "mistral-nemo" else pd.Series(dtype=float)  # Llama: probabilities unusable
        shift = mean_ci(item_diff(g, "stored_incorrect", "no_belief", value="p_inc", items=its).to_numpy(), idx) if len(band_p) else None
        rows.append({"model": model, "round": name, "items": len(its), "trial_pairs": int(item_diff(g, "stored_incorrect", "no_belief").shape[0]),
                     "baseline_correct": base["correct"].mean(), "baseline_false": base["y"].mean(),
                     "baseline_other_wrong": base["other"].mean(), "stored_false": st["y"].mean(),
                     "effect": ci["est"], "ci_low": ci["ci_low"], "ci_high": ci["ci_high"], "p_item": exact_signflip_p(d1.to_numpy()),
                     "conversion": ci["est"] / conv_den if conv_den > 0 else np.nan,
                     "median_top_prob": band_p.median() if len(band_p) else np.nan,
                     "share_unsure": (band_p < .9).mean() if len(band_p) else np.nan,
                     "mean_prob_shift": shift["est"] if shift else np.nan, "prob_shift_low": shift["ci_low"] if shift else np.nan,
                     "prob_shift_high": shift["ci_high"] if shift else np.nan})
rounds = save(pd.DataFrame(rows), "t23_rounds_baseline_vs_effect")

# Same uncertainty, different item type? Nemo only, because only Nemo has probabilities in rounds 2-4.
g2 = frames["r2_calsmall"].query("model == 'mistral-nemo' and case_kind == 'factual'")
g4 = by_model["mistral-nemo"]


def prob_pairs(g):
    a = g[g.condition == "no_belief"].set_index(["case_id", "rep", "evidence_mode"])
    b = g[g.condition == "stored_incorrect"].set_index(["case_id", "rep", "evidence_mode"])
    j = a.merge(b, left_index=True, right_index=True, how="inner", suffixes=("_b", "_s")).dropna(
        subset=["p_inc_b", "p_inc_s"]).reset_index()
    j["delta"] = j["p_inc_s"] - j["p_inc_b"]
    j["band"] = j.apply(lambda r: band({"pmax": r["pmax_b"], "p_ans": r["p_ans_b"]}), axis=1)
    j["flip"] = ((j["y_b"] == 0) & (j["y_s"] == 1)).astype(float)
    j["at_risk"] = j["y_b"] == 0
    return j


rows = []
pp = {"Round 2 harder items": prob_pairs(g2), "Long-tail (main, 48)": prob_pairs(g4)}
for setname, j in pp.items():
    for bname in BANDS:
        s = j[j["band"] == bname]
        its = sorted(s.case_id.unique())
        if not its:
            continue
        ci = pair_mean_ci(s, "delta", its, boot_indices(len(its), 5000))
        ar = s[s.at_risk]
        rows.append({"item_set": setname, "band": bname, "pairs": len(s), "items": len(its), "share_of_pairs": len(s) / len(j),
                     "mean_shift": ci["est"], "ci_low": ci["ci_low"], "ci_high": ci["ci_high"],
                     "at_risk": len(ar), "flips": int(ar["flip"].sum()), "flip_rate": ar["flip"].mean() if len(ar) else np.nan,
                     "mean_false_prob_base": s["p_inc_b"].mean()})
save(pd.DataFrame(rows), "t24_nemo_same_uncertainty_by_itemset")

# Difference between item sets in Nemo's effect (independent item samples), and in Llama's
rows = []
for model, r2key in [("mistral-nemo", "r2_calsmall"), ("llama-8b", "r2_calibration")]:
    a = item_diff(frames[r2key].query(f"model == '{model}' and case_kind == 'factual'"), "stored_incorrect", "no_belief")
    b = item_diff(by_model[model], "stored_incorrect", "no_belief", items=items)
    ia, ib = boot_indices(len(a)), boot_indices(len(b), seed=SEED + 1)
    bd = b.to_numpy()[ib].mean(1) - a.to_numpy()[ia].mean(1)
    rows.append({"model": model, "round2_items": len(a), "round2_effect": a.mean(), "longtail_items": len(b), "longtail_effect": b.mean(),
                 "difference": b.mean() - a.mean(), "ci_low": float(np.quantile(bd, .025)), "ci_high": float(np.quantile(bd, .975))})
save(pd.DataFrame(rows), "t25_longtail_vs_round2_difference")

# ---------------------------------------------------------------------------- 8. selection and internal replication

rows = []
perm_rng = np.random.default_rng(SEED)
for m in MODELS:
    for cond, ref in [("stored_incorrect", "no_belief"), ("stored_incorrect_labelled", "stored_incorrect"),
                      ("stated_incorrect", "no_belief"), ("stored_correct", "no_belief")]:
        d = item_diff(by_model[m], cond, ref, items=items)
        mask = d.index.isin(screened)
        res = {"model": m, "comparison": f"{cond} vs {ref}"}
        for lab, sel in [("screened", mask), ("new", ~mask)]:
            sub = d[sel].to_numpy()
            ci = mean_ci(sub, boot_indices(len(sub)))
            base_ = by_model[m][(by_model[m].condition == ref) & (by_model[m].case_id.isin(d.index[sel]))]
            res.update({f"{lab}_ref_rate": base_["y"].mean(), f"{lab}_ref_correct": base_["correct"].mean(), f"{lab}_effect": ci["est"],
                        f"{lab}_low": ci["ci_low"], f"{lab}_high": ci["ci_high"], f"{lab}_items_up": int((sub > 0).sum()),
                        f"{lab}_items_down": int((sub < 0).sum()), f"{lab}_p_item": exact_signflip_p(sub)})
        vals = np.nan_to_num(d.to_numpy())
        obs = vals[mask].mean() - vals[~mask].mean()
        perms = np.array([perm_rng.permuted(vals) for _ in range(50_000)])
        null = perms[:, :24].mean(1) - perms[:, 24:].mean(1)
        ia = boot_indices(24)
        ib = boot_indices(24, seed=SEED + 1)
        bd = d[mask].to_numpy()[ia]
        bn = d[~mask].to_numpy()[ib]
        diff = np.nanmean(bd, 1) - np.nanmean(bn, 1)
        res.update(diff=float(obs), diff_low=float(np.quantile(diff, .025)), diff_high=float(np.quantile(diff, .975)),
                   p_perm=float((1 + (np.abs(null) >= abs(obs) - 1e-12).sum()) / 50_001))
        rows.append(res)
rep_tab = save(pd.DataFrame(rows), "t26_screened_vs_new_items")

# Fraction removed by the label on new items only
s, lb, b = stack[("mistral-nemo", "y")]
mask = s.index.isin(new_items)
R["label_new_items"] = ratio_ci((s - lb)[mask].to_numpy(), (s - b)[mask].to_numpy(), boot_indices(24))
R["label_screened_items"] = ratio_ci((s - lb)[~mask].to_numpy(), (s - b)[~mask].to_numpy(), boot_indices(24))

# Item-level agreement between round 3 and round 4 on the 24 shared prompts
g3 = lt[lt.model == "mistral-nemo"]
e3 = item_diff(g3, "stored_incorrect", "no_belief", items=screened)
e4 = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", items=screened)
p3 = item_diff(g3, "stored_incorrect", "no_belief", value="p_inc", items=screened)
p4 = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", value="p_inc", items=screened)
R["r3_r4"] = {"effect_r3": float(e3.mean()), "effect_r4_same_items": float(e4.mean()), "rho_choice": float(stats.spearmanr(e3, e4).statistic),
              "rho_prob_shift": float(stats.spearmanr(p3, p4).statistic), "prob_shift_r3": float(p3.mean()), "prob_shift_r4": float(p4.mean())}

# Nemo probability shift, screened vs new (less noisy than chosen answers)
pd_ = item_diff(by_model["mistral-nemo"], "stored_incorrect", "no_belief", value="p_inc", items=items)
R["nemo_prob_shift"] = {"screened": float(pd_[pd_.index.isin(screened)].mean()), "new": float(pd_[pd_.index.isin(new_items)].mean())}
vs = pd_.to_numpy()
null = np.array([(lambda v: v[:24].mean() - v[24:].mean())(perm_rng.permutation(vs)) for _ in range(50_000)])
obs = R["nemo_prob_shift"]["screened"] - R["nemo_prob_shift"]["new"]
R["nemo_prob_shift"]["p_perm"] = float((1 + (np.abs(null) >= abs(obs) - 1e-12).sum()) / 50_001)

# Stored vs stated on the continuous probability measure
rows = []
for m in ["mistral-nemo", "mistral-small", "gemma-moe"]:
    d = item_diff(by_model[m], "stated_incorrect", "stored_incorrect", value="p_inc", items=items)
    rows.append({"model": m, "measure": "probability on false option", **mean_ci(d.to_numpy(), IDX), "p_mc": mc_signflip_p(d.to_numpy()),
                 "items_higher_stored": int((d < 0).sum()), "items_higher_stated": int((d > 0).sum())})
save(pd.DataFrame(rows), "t27_stated_vs_stored_probability")

# Does a model refer to the stored belief in its reply? A rough text search, checked against the
# no-memory conditions, where the same search should find almost nothing.
PAT = r"(?i)saved memor|memory|memories|you believe|user believes|your belief|you (?:may|might) (?:think|believe)|previous conversation"
main_text = pd.DataFrame([{"trial_id": r["trial_id"], "text": r.get("response_text") or ""} for r in _raw])
ft = fact.merge(main_text, on="trial_id", how="left")
ft["mentions"] = ft["text"].str.contains(PAT)
rows = []
for m in MODELS:
    g = ft[ft.model == m]
    si = g[g.condition == "stored_incorrect"]
    row = {"model": m, "stored_false_mentions": si["mentions"].mean(), "stored_correct_mentions": g[g.condition == "stored_correct"]["mentions"].mean(),
           "no_belief_mentions": g[g.condition == "no_belief"]["mentions"].mean(), "unrelated_mentions": g[g.condition == "stored_unrelated"]["mentions"].mean(),
           "stored_false_mention_trials": int(si["mentions"].sum()), "false_chosen_when_mentioned": int(si[si.mentions]["y"].sum()),
           "false_rate_when_not_mentioned": si[~si.mentions]["y"].mean()}
    rows.append(row)
save(pd.DataFrame(rows), "t32_replies_mentioning_the_belief")
pref = main_text.merge(useful[useful.model == "llama-8b"], on="trial_id")
pref = pref[pref.case_id.isin(["useful_vegetarian", "useful_metric"])]
R["llama_preference"] = {"trials": len(pref), "right": int(pref["correct"].sum()),
                         "cites_memory": int(pref["text"].str.contains(r"(?i)you prefer|your preference|user's preference|as a vegetarian|your previous|you are a vegetarian|you're a vegetarian|you don't eat").sum())}

# Rows for figure 1
fig = []
for m in MODELS:
    for cond, ref in COMPARISONS:
        s = pt[(pt.model == m) & (pt.cond == cond) & (pt.ref == ref)].iloc[0]
        fig.append({"model": m, "cond": cond, "ref": ref, "est": s["est"], "low": s["ci_low"], "high": s["ci_high"],
                    "items_moved": s["items_moved"], "survives_item": s["survives_item"], "survives_mcnemar": s["survives_mcnemar"]})
save(pd.DataFrame(fig), "fig_effects")
rate.reset_index().to_csv(TABLES / "fig_rates.csv", index=False)

R["meta"] = {"bootstrap_resamples": B, "seed": SEED, "n_items": n_items}
R["nemo_rates"] = rate.loc["mistral-nemo"].to_dict()
R["nemo_correct"] = corr.loc["mistral-nemo"].to_dict()
(TABLES.parent / "results.json").write_text(json.dumps(R, indent=1, default=float))
print("checks", R["checks"]["total"], "mismatches", R["checks"]["mismatch"])
