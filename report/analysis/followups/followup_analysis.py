"""Follow-up analyses for NST2046 (runs dated 2026-11-05). All of this is post hoc.

Reads logged trials only: no API calls, no .env, nothing written outside
report/analysis/followups/ and report/figures/. Reuses the helpers in report/analysis/common.py
(item bootstrap with BCa intervals, exact McNemar, exact sign-flip, Holm).

Rebuild with: bash report/analysis/followups/run_followups.sh
"""

from __future__ import annotations

import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common import (B, ROOT, SEED, bca, boot_indices, exact_signflip_p, final_letter, first_letter, holm, load_cases,  # noqa: E402
                    mc_signflip_p, mcnemar_exact, mean_ci, probs_from_head, ratio_ci)

TABLES = HERE / "tables"
TABLES.mkdir(parents=True, exist_ok=True)
RUNS = ROOT / "runs"
MAIN = "main-20261027"
NEMO, SMALL = "mistral-nemo", "mistral-small"
SUSCEPTIBLE = [NEMO, SMALL]
FOLLOWUP_MODELS = [NEMO, SMALL, "llama-8b", "gemma-moe", "qwen-small"]
NAMES = {NEMO: "Mistral Nemo 12B", SMALL: "Mistral Small 24B", "llama-8b": "Llama 3.1 8B", "gemma-moe": "Gemma 4 26B",
         "qwen-small": "Qwen3.5-9B", "nemo-base-local": "Local base (completion)",
         "nemo-instruct-local": "Local instruct (completion)", "nemo-instruct-local-chat": "Local instruct (chat)",
         "hosted": "Hosted instruct (main run)"}
ALIAS = {"llama-8b-deepinfra": "llama-8b", "qwen-small-nothink": "qwen-small"}
ARMS_LOCAL = ["nemo-base-local", "nemo-instruct-local", "nemo-instruct-local-chat"]

SI, LB, NB, SC, SCL, ST, UN = ("stored_incorrect", "stored_incorrect_labelled", "no_belief", "stored_correct",
                               "stored_correct_labelled", "stated_incorrect", "stored_unrelated")

_LEADING_COMMA = re.compile(r"^\s*\**\s*\(?([A-H])\)?,")
_LEADING = re.compile(r"^\s*\**\s*\(?([A-H])\)?(?:[.):\s*]|$)")

RESULTS: dict = {}
AUDIT: dict = {}


def save(df: pd.DataFrame, name: str) -> pd.DataFrame:
    df.to_csv(TABLES / f"{name}.csv", index=False, float_format="%.6g")
    return df


# ------------------------------------------------------------------ loading and scoring


def read_rows(run: str) -> list[dict]:
    path = RUNS / run / "trials.jsonl"
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def load_mcq(run: str, cases: dict) -> pd.DataFrame:
    """One row per trial (last attempt). Re-scores every response and checks it against the log."""
    rows = read_rows(run)
    last = {r["trial_id"]: r for r in rows}
    out, mismatches = [], 0
    for r in last.values():
        case, omap = cases[r["case_id"]], r["option_map"]
        valid = list(omap)
        text = r.get("response_text")
        completion = "prompt" in (r.get("request") or {})
        err = r.get("auto_score") == "error"
        if completion:
            m = _LEADING.match(text or "")
            letter = m.group(1).upper() if m and m.group(1).upper() in valid else None
            rescue = letter
            if rescue is None:
                m = _LEADING_COMMA.match(text or "")
                rescue = m.group(1) if m and m.group(1) in valid else None
            # The harness parser now reads these comma answers; the logged scores predate that fix.
            logged_miss = letter is None and rescue is not None
            letter = rescue
            first = letter
        else:
            letter = None if err else final_letter(text, valid)
            rescue = letter
            first = None if err else first_letter(text, valid)
        ans, wrong = case["answer"], case.get("incorrect_option")

        def code(d):
            sel = omap.get(d) if d else None
            return ("unparseable" if sel is None else "correct" if sel == ans
                    else "accepted_incorrect" if sel == wrong else "other_wrong"), sel

        score, sel = code(letter)
        if err:
            score = "error"
        mismatches += score != r.get("auto_score") and not (completion and logged_miss)
        s2, _ = code(rescue)
        s3, _ = code(first)
        model = ALIAS.get(r["model_alias"], r["model_alias"])
        probs = r.get("option_probs") if isinstance(r.get("option_probs"), dict) else None
        if probs is None and model == SMALL:
            probs = probs_from_head(r.get("logprobs_head"), omap)
        usable = score in ("correct", "accepted_incorrect", "other_wrong")
        usable2 = s2 in ("correct", "accepted_incorrect", "other_wrong")
        usable3 = s3 in ("correct", "accepted_incorrect", "other_wrong")
        rec = {"run": run, "trial_id": r["trial_id"], "model": model, "alias": r["model_alias"],
               "case_id": r["case_id"], "kind": r.get("case_kind", "factual"), "category": r.get("category"),
               "condition": r["condition"], "rep": int(r["rep"]), "score": score, "provider": r.get("provider"),
               "y": float(score == "accepted_incorrect") if usable else np.nan,
               "correct": float(score == "correct") if usable else np.nan,
               "other": float(score == "other_wrong") if usable else np.nan,
               "y_rescued": float(s2 == "accepted_incorrect") if usable2 else np.nan,
               "correct_rescued": float(s2 == "correct") if usable2 else np.nan,
               "y_first": float(s3 == "accepted_incorrect") if usable3 else np.nan,
               "correct_first": float(s3 == "correct") if usable3 else np.nan,
               "p_inc": probs.get(wrong, np.nan) if probs and wrong else np.nan,
               "p_ans": probs.get(ans, np.nan) if probs else np.nan,
               "note": r.get("reasoning_text") if isinstance(r.get("reasoning_text"), str) else None}
        out.append(rec)
    AUDIT[run] = {"attempt_rows": len(rows), "trials": len(last), "score_mismatches": int(mismatches)}
    return pd.DataFrame(out)


def check_case_files() -> None:
    """The evidence item files must differ from longtail.yaml only in the passage fields."""
    base = {c["id"]: c for c in yaml.safe_load((ROOT / "data/cases/longtail.yaml").read_text())["cases"]}
    for f in ["longtail_evidence", "longtail_weak_evidence", "longtail_stale_source"]:
        other = {c["id"]: c for c in yaml.safe_load((ROOT / f"data/cases/{f}.yaml").read_text())["cases"]}
        assert set(other) == set(base), f
        for k, c in base.items():
            for field, v in c.items():
                if field not in ("evidence", "evidence_strength", "sources", "notes"):
                    assert other[k][field] == v, (f, k, field)


check_case_files()
CASES = load_cases()
ITEMS = sorted(c["id"] for c in yaml.safe_load((ROOT / "data/cases/longtail.yaml").read_text())["cases"])
NUMERICAL = sorted(i for i in ITEMS if CASES[i]["category"] == "numerical")
ARITH_EXTRA = ["lt_newborn_bones", "lt_potato_chromosomes", "lt_sound_in_water"]  # science, but the weak passage gives sums
IDX = boot_indices(len(ITEMS), B, SEED)

RUN_NAMES = (
    [MAIN, "longtail-20261027", "evidence-20261105", "weak-evidence-20261105", "stale-source-20261105", "label-correct-20261105",
     "patient-frame-20261105", "local-base-20261105", "local-instruct-20261105"]
    + [f"wrappers-20261105/{v}" for v in ["base", "notes", "verified_profile", "may_be_wrong", "bare_fact", "said_once",
                                         "label_short", "label_source", "label_check"]]
    + [f"fixes-20261105/{v}" for v in ["tutor", "rule", "answer_first", "memory_gate"]]
    + [f"tutor-split-20261105/{v}" for v in ["role_only", "heading_only", "student_only"]]
)
DATA = {r: load_mcq(r, CASES) for r in RUN_NAMES}
ALL = pd.concat(DATA.values(), ignore_index=True)
FACT = ALL[ALL.kind == "factual"]
_INDEX = {k: g.set_index(["case_id", "rep"]) for k, g in FACT.groupby(["run", "model", "condition"])}


def S(run: str, model: str, cond: str, value: str = "y") -> pd.Series:
    """Trial values for one cell, indexed by (item, rep)."""
    return _INDEX[(run, model, cond)][value]


def item_means(s: pd.Series, items) -> np.ndarray:
    return s.groupby("case_id").mean().reindex(items).to_numpy()


def idx_for(items) -> np.ndarray:
    return IDX if len(items) == len(ITEMS) else boot_indices(len(items), B, SEED)


def rate(s: pd.Series, items=None) -> dict:
    items = ITEMS if items is None else items
    s = s[s.index.get_level_values("case_id").isin(items)]
    d = mean_ci(item_means(s, items), idx_for(items))
    d["n"] = int(s.notna().sum())
    return d


def compare(a: pd.Series, b: pd.Series, items=None, binary: bool = True) -> dict:
    """a minus b, matched on item and rep, then averaged within item."""
    items = ITEMS if items is None else items
    a = a[a.index.get_level_values("case_id").isin(items)]
    d = (a - b).dropna()
    v = item_means(d, items)
    out = mean_ci(v, idx_for(items))
    out["pairs"] = int(len(d))
    out["items_up"], out["items_down"] = int((v > 0).sum()), int((v < 0).sum())
    if binary:
        out["toward"], out["away"] = int((d > 0).sum()), int((d < 0).sum())
        out["mcnemar_p"] = mcnemar_exact(out["toward"], out["away"])
        out["item_p"] = exact_signflip_p(v)
    else:
        out["item_p"] = mc_signflip_p(v)
    return out


def contrast(parts: list[tuple[float, pd.Series]], items=None, binary: bool = True) -> dict:
    """Weighted sum of item-level means, keeping only items present in every part. For difference-in-differences."""
    items = ITEMS if items is None else items
    vs = [w * item_means(s[s.index.get_level_values("case_id").isin(items)], items) for w, s in parts]
    v = np.sum(vs, axis=0)  # NaN if an item is missing from any part
    out = mean_ci(v, idx_for(items))
    out["items_up"], out["items_down"] = int((v > 0).sum()), int((v < 0).sum())
    w = v[np.isfinite(v)]
    on_grid = np.allclose(np.rint(np.abs(w) * 4) / 4, np.abs(w))
    out["item_p"] = exact_signflip_p(v) if (binary and on_grid) else mc_signflip_p(v)
    return out


def add_holm(df: pd.DataFrame, cols=("item_p", "mcnemar_p")) -> pd.DataFrame:
    for c in cols:
        if c in df:
            ok = df[c].notna()
            df.loc[ok, f"holm_{c}"] = holm(df.loc[ok, c].to_numpy())
    return df


# ------------------------------------------------------------------ Q1 dose-response


def q1() -> None:
    levels = [("none", MAIN), ("weak", "weak-evidence-20261105"), ("strong", "evidence-20261105")]
    sets = {"all 48": ITEMS, "drop lt_most_islands": [i for i in ITEMS if i != "lt_most_islands"],
            "drop 8 numerical": [i for i in ITEMS if i not in NUMERICAL],
            "drop islands + numerical": [i for i in ITEMS if i not in NUMERICAL and i != "lt_most_islands"],
            "drop islands + numerical + 3 sum-based science": [i for i in ITEMS if i not in NUMERICAL + ARITH_EXTRA and i != "lt_most_islands"],
            "only 8 numerical": NUMERICAL}
    rows, cons, strength = [], [], []
    for sname, items in sets.items():
        for m in SUSCEPTIBLE:
            for lev, run in levels:
                nb, si, lb = S(run, m, NB), S(run, m, SI), S(run, m, LB)
                e, l, lvb = compare(si, nb, items), compare(lb, si, items), compare(lb, nb, items)
                a = rate(S(run, m, NB, "correct"), items)
                ids = idx_for(items)
                frac = ratio_ci(item_means(si - lb, items), item_means(si - nb, items), ids) if abs(e["est"]) >= 0.05 else {}
                rows.append({"items": sname, "n_items": len(items), "model": m, "evidence": lev, "nb_accuracy": a["est"], "nb_acc_low": a["ci_low"], "nb_acc_high": a["ci_high"],
                             "nb_false": rate(nb, items)["est"], "nb_other": rate(S(run, m, NB, "other"), items)["est"], "si_false": rate(si, items)["est"], "lb_false": rate(lb, items)["est"],
                             "si_correct": rate(S(run, m, SI, "correct"), items)["est"],
                             "effect": e["est"], "effect_low": e["ci_low"], "effect_high": e["ci_high"], "effect_toward": e["toward"], "effect_away": e["away"],
                             "effect_mcnemar_p": e["mcnemar_p"], "effect_item_p": e["item_p"], "effect_items_up": e["items_up"], "effect_items_down": e["items_down"],
                             "label_change": l["est"], "label_low": l["ci_low"], "label_high": l["ci_high"], "label_toward": l["toward"], "label_away": l["away"],
                             "label_mcnemar_p": l["mcnemar_p"], "label_item_p": l["item_p"],
                             "label_vs_nb": lvb["est"], "label_vs_nb_low": lvb["ci_low"], "label_vs_nb_high": lvb["ci_high"],
                             "fraction_removed": frac.get("est", np.nan), "fraction_low": frac.get("ci_low", np.nan), "fraction_high": frac.get("ci_high", np.nan)})
            for (la, ra), (lb_, rb) in [(levels[0], levels[1]), (levels[1], levels[2]), (levels[0], levels[2])]:
                for what, cond in [("memory effect", SI), ("label-arm effect", LB)]:
                    c = contrast([(1, S(ra, m, cond)), (-1, S(ra, m, NB)), (-1, S(rb, m, cond)), (1, S(rb, m, NB))], items)
                    cons.append({"items": sname, "model": m, "measure": what, "contrast": f"{la} minus {lb_}", "est": c["est"], "ci_low": c["ci_low"], "ci_high": c["ci_high"], "item_p": c["item_p"]})
                d = contrast([(1, S(ra, m, SI)), (-1, S(ra, m, LB)), (-1, S(rb, m, SI)), (1, S(rb, m, LB))], items)
                cons.append({"items": sname, "model": m, "measure": "label reduction", "contrast": f"{la} minus {lb_}", "est": d["est"], "ci_low": d["ci_low"], "ci_high": d["ci_high"], "item_p": d["item_p"]})
            # How far along the road from no passage to a stating passage is the weak passage?
            a0, a1, a2 = (item_means(S(r, m, NB, "correct")[lambda s: s.index.get_level_values("case_id").isin(items)], items) for _, r in levels)
            st = ratio_ci(a1 - a0, a2 - a0, idx_for(items)) if (a2 - a0).mean() > 0 else {"est": np.nan, "ci_low": np.nan, "ci_high": np.nan}
            f0, f1, f2 = (item_means(S(r, m, NB)[lambda s: s.index.get_level_values("case_id").isin(items)], items) for _, r in levels)
            gain = contrast([(1, S(levels[1][1], m, NB, "correct")), (-1, S(levels[0][1], m, NB, "correct"))], items)
            left = contrast([(1, S(levels[2][1], m, NB, "correct")), (-1, S(levels[1][1], m, NB, "correct"))], items)
            strength.append({"items": sname, "model": m, "acc_none": a0.mean(), "acc_weak": a1.mean(), "acc_strong": a2.mean(),
                             "weak_gain": gain["est"], "weak_gain_low": gain["ci_low"], "weak_gain_high": gain["ci_high"], "weak_gain_p": gain["item_p"],
                             "strong_minus_weak": left["est"], "smw_low": left["ci_low"], "smw_high": left["ci_high"], "smw_p": left["item_p"],
                             "share_of_gap_closed": st["est"], "share_low": st["ci_low"], "share_high": st["ci_high"],
                             "false_none": f0.mean(), "false_weak": f1.mean(), "false_strong": f2.mean(),
                             "items_perfect_none": int((a0 == 1).sum()), "items_perfect_weak": int((a1 == 1).sum()), "items_perfect_strong": int((a2 == 1).sum()), "n_items": len(items)})
    t = pd.DataFrame(rows)
    # Holm over the primary family only: effect and label change, two models, three levels, all items.
    prim = t["items"] == "all 48"
    ps = np.r_[t.loc[prim, "effect_item_p"], t.loc[prim, "label_item_p"]]
    adj = holm(ps)
    t.loc[prim, "effect_holm_item"], t.loc[prim, "label_holm_item"] = adj[:prim.sum()], adj[prim.sum():]
    ps = np.r_[t.loc[prim, "effect_mcnemar_p"], t.loc[prim, "label_mcnemar_p"]]
    adj = holm(ps)
    t.loc[prim, "effect_holm_trial"], t.loc[prim, "label_holm_trial"] = adj[:prim.sum()], adj[prim.sum():]
    save(t, "q1_dose_response")
    save(pd.DataFrame(cons), "q1_contrasts")
    save(pd.DataFrame(strength), "q1_weak_passage_strength")
    rows = []
    for m in SUSCEPTIBLE:
        for lev, run in levels:
            for cond in (NB, LB, SI):
                r_ = rate(S(run, m, cond))
                rows.append({"model": m, "evidence": lev, "condition": cond, "rate": r_["est"], "low": r_["ci_low"], "high": r_["ci_high"]})
    save(pd.DataFrame(rows), "fig5_rates")
    # Strong evidence on all five models, with the stated arm.
    rows = []
    r = "evidence-20261105"
    for m in FOLLOWUP_MODELS:
        e, s, lb_ = compare(S(r, m, SI), S(r, m, NB)), compare(S(r, m, ST), S(r, m, NB)), compare(S(r, m, LB), S(r, m, NB))
        rows.append({"model": m, "nb_accuracy": rate(S(r, m, NB, "correct"))["est"], "nb_false": rate(S(r, m, NB))["est"], "si_false": rate(S(r, m, SI))["est"],
                     "st_false": rate(S(r, m, ST))["est"], "lb_false": rate(S(r, m, LB))["est"], "si_effect": e["est"], "si_low": e["ci_low"], "si_high": e["ci_high"],
                     "si_toward": e["toward"], "si_away": e["away"], "si_p": e["mcnemar_p"], "st_effect": s["est"], "st_low": s["ci_low"], "st_high": s["ci_high"],
                     "lb_effect": lb_["est"], "lb_low": lb_["ci_low"], "lb_high": lb_["ci_high"]})
    save(pd.DataFrame(rows), "q1_strong_all_models")
    # Which items still move under weak evidence?
    rows = []
    for m in SUSCEPTIBLE:
        w = "weak-evidence-20261105"
        v = pd.DataFrame({"none": item_means(S(MAIN, m, SI) - S(MAIN, m, NB), ITEMS), "weak": item_means(S(w, m, SI) - S(w, m, NB), ITEMS)}, index=ITEMS)
        v["model"] = m
        v["numerical"] = v.index.isin(NUMERICAL)
        rows.append(v.reset_index(names="case_id"))
    save(pd.concat(rows), "q1_item_effects_none_vs_weak")


# ------------------------------------------------------------------ Q2 wrappers


WRAP = "wrappers-20261105/"
MEMORY_WORDINGS = ["notes", "verified_profile", "may_be_wrong", "bare_fact", "said_once"]
LABEL_WORDINGS = ["label_short", "label_source", "label_check"]
SI_REPLICATES = [MAIN, WRAP + "base"] + [WRAP + v for v in LABEL_WORDINGS]  # byte-identical prompts in the stored_incorrect arm


def pooled_si(model: str, value: str = "y") -> pd.Series:
    return pd.concat([S(r, model, SI, value) for r in SI_REPLICATES], axis=1).mean(axis=1)


def simulate_noise(cells: list[pd.Series], seed: int = SEED, sims: int = 20000) -> dict:
    """Run-to-run spread if each trial is a fresh draw from its own pooled probability."""
    p = pd.concat(cells, axis=1).mean(axis=1).to_numpy()
    rng = np.random.default_rng(seed)
    runs = rng.random((sims, len(cells), len(p))) < p
    rates = runs.mean(axis=2)
    sd = rates.std(axis=1, ddof=1)
    gap = rates.max(axis=1) - rates.min(axis=1)
    two = np.abs(rates[:, 0] - rates[:, 1])
    obs = np.array([c.mean() for c in cells])
    obs_sd, obs_gap = obs.std(ddof=1), obs.max() - obs.min()
    return {"sd_run_sim": float(np.sqrt((rates.var(axis=1, ddof=1)).mean())), "sd_run_obs": float(obs_sd), "gap_obs": float(obs_gap), "gap_sim_median": float(np.median(gap)),
            "p_sd_as_large": float((sd >= obs_sd - 1e-12).mean()), "two_run_abs_diff_95": float(np.quantile(two, 0.95))}


def q2() -> None:
    noise_rows = []
    for m in SUSCEPTIBLE:
        cells = [S(r, m, SI) for r in SI_REPLICATES]
        sim = simulate_noise(cells)
        rates_ = {r.split("/")[-1]: float(S(r, m, SI).mean()) for r in SI_REPLICATES}
        bm = compare(S(WRAP + "base", m, SI), S(MAIN, m, SI))
        lbm = compare(S(WRAP + "base", m, LB), S(MAIN, m, LB))
        mp = contrast([(1, pd.concat([S(r, m, SI) for r in SI_REPLICATES[1:]], axis=1).mean(axis=1)), (-1, S(MAIN, m, SI))], binary=False)
        same = pd.concat([S(r, m, SI) for r in SI_REPLICATES], axis=1)
        agree = float(np.mean([(same.iloc[:, i] == same.iloc[:, j]).mean() for i, j in itertools.combinations(range(5), 2)]))
        noise_rows.append({"model": m, **{f"rate_{k}": v for k, v in rates_.items()}, "pooled_si": float(np.nanmean(same.to_numpy())),
                           "base_minus_main_si": bm["est"], "bm_low": bm["ci_low"], "bm_high": bm["ci_high"], "bm_toward": bm["toward"], "bm_away": bm["away"], "bm_mcnemar_p": bm["mcnemar_p"], "bm_item_p": bm["item_p"],
                           "base_minus_main_lb": lbm["est"], "lbm_low": lbm["ci_low"], "lbm_high": lbm["ci_high"], "lbm_toward": lbm["toward"], "lbm_away": lbm["away"], "lbm_mcnemar_p": lbm["mcnemar_p"], "lbm_item_p": lbm["item_p"],
                           "same_day_minus_main": mp["est"], "sdm_low": mp["ci_low"], "sdm_high": mp["ci_high"], "sdm_p": mp["item_p"],
                           "trial_agreement_between_replicates": agree, **sim,
                           "noise_band": max(sim["two_run_abs_diff_95"], abs(bm["est"]), abs(lbm["est"]), sim["gap_obs"])})
    noise = save(pd.DataFrame(noise_rows), "q2_noise").set_index("model")
    rows = []
    base = WRAP + "base"
    for m in SUSCEPTIBLE:
        for v in MEMORY_WORDINGS + LABEL_WORDINGS:
            r = WRAP + v
            arms = [("stored", SI), ("labelled", LB)] if v in MEMORY_WORDINGS else [("labelled", LB)]
            for arm, cond in arms:
                c = compare(S(r, m, cond), S(base, m, cond))
                rows.append({"family": "memory wording" if v in MEMORY_WORDINGS else "label wording", "variant": v, "model": m, "arm": arm, "base_rate": S(base, m, cond).mean(),
                             "variant_rate": S(r, m, cond).mean(), **{k: c[k] for k in ("est", "ci_low", "ci_high", "toward", "away", "mcnemar_p", "item_p", "items_up", "items_down", "pairs")}})
    t = add_holm(pd.DataFrame(rows))
    t["noise_band"] = t.model.map(noise["noise_band"])
    t["beyond_noise"] = t.est.abs() > t.noise_band
    t["verdict"] = np.where((t.holm_item_p < 0.05) & t.beyond_noise, "real", np.where((t.holm_mcnemar_p < 0.05) & t.beyond_noise, "real on trials only",
                            np.where((t.ci_low > 0) | (t.ci_high < 0), "suggestive", "within noise")))
    save(t, "q2_wrappers_vs_base")
    # Label effect within each wording, and how much of the effect above baseline remains.
    rows = []
    for m in SUSCEPTIBLE:
        for v in ["base"] + MEMORY_WORDINGS + LABEL_WORDINGS:
            r = WRAP + v
            si, lb = S(r, m, SI), S(r, m, LB)
            nb = S(MAIN, m, NB)
            c = compare(lb, si)
            e = compare(si, nb)
            acc = rate(S(r, m, SI, "correct"))
            frac = ratio_ci(item_means(si - lb, ITEMS), item_means(si - nb, ITEMS), IDX)
            dd = contrast([(1, lb), (-1, si), (-1, S(base, m, LB)), (1, S(base, m, SI))]) if v != "base" else {}
            rows.append({"variant": v, "model": m, "si_false": si.mean(), "lb_false": lb.mean(), "si_correct": acc["est"], "other_wrong_si": S(r, m, SI, "other").mean(),
                         "effect_vs_main_nb": e["est"], "effect_low": e["ci_low"], "effect_high": e["ci_high"],
                         "label_change": c["est"], "label_low": c["ci_low"], "label_high": c["ci_high"], "toward": c["toward"], "away": c["away"], "mcnemar_p": c["mcnemar_p"], "item_p": c["item_p"],
                         "fraction_removed": frac["est"], "fraction_low": frac["ci_low"], "fraction_high": frac["ci_high"],
                         "label_change_vs_base": dd.get("est", np.nan), "lcb_low": dd.get("ci_low", np.nan), "lcb_high": dd.get("ci_high", np.nan), "lcb_p": dd.get("item_p", np.nan)})
    save(add_holm(pd.DataFrame(rows)), "q2_label_within_wording")


# ------------------------------------------------------------------ Q3 fixes and frames


FIX = "fixes-20261105/"
SPLIT = "tutor-split-20261105/"
PATIENT = "patient-frame-20261105"
LABEL_RUN = "label-correct-20261105"
VARIANTS = [("tutor", FIX + "tutor", "frame", "own"), ("patient", PATIENT, "frame", "own"),
            ("rule", FIX + "rule", "harness fix", "main, same prompt"), ("answer_first", FIX + "answer_first", "harness fix", "main, same prompt"),
            ("memory_gate", FIX + "memory_gate", "harness fix", "main, same prompt"),
            ("role_only", SPLIT + "role_only", "tutor part", "main, prompt differs, not run"),
            ("heading_only", SPLIT + "heading_only", "tutor part", "main, same prompt"),
            ("student_only", SPLIT + "student_only", "tutor part", "main, same prompt"),
            ("label", MAIN, "label (reference)", "main, same prompt")]


def nb_for(run: str, source: str, model: str, value: str) -> pd.Series:
    return S(run if source == "own" else MAIN, model, NB, value)


def q3() -> None:
    rows = []
    for m in SUSCEPTIBLE:
        si_m, sc_m, nb_y, nb_c = S(MAIN, m, SI), S(MAIN, m, SC, "correct"), S(MAIN, m, NB), S(MAIN, m, NB, "correct")
        eff_m, ben_m = item_means(si_m - nb_y, ITEMS), item_means(sc_m - nb_c, ITEMS)
        for name, run, family, source in VARIANTS:
            # The label row borrows the main run's labelled arm and the separate labelled-true-memory run.
            si_v = S(MAIN, m, LB) if name == "label" else S(run, m, SI)
            sc_v = S(LABEL_RUN, m, SCL, "correct") if name == "label" else S(run, m, SC, "correct")
            nv_y, nv_c = nb_for(run, source, m, "y"), nb_for(run, source, m, "correct")
            harm = compare(si_v, si_m)
            bene = compare(sc_v, sc_m)
            harm_pool = contrast([(1, si_v), (-1, pooled_si(m))], binary=False)
            eff_pool = item_means(pooled_si(m), ITEMS) - item_means(nb_y, ITEMS)
            eff_v, ben_v = item_means(si_v - nv_y, ITEMS), item_means(sc_v - nv_c, ITEMS)
            x = mean_ci(eff_m - eff_v, IDX)
            y = mean_ci(ben_v, IDX)
            within = compare(si_v, nv_y)
            within_ben = compare(sc_v, nv_c)
            fx = ratio_ci(eff_m - eff_v, eff_m, IDX)
            fy = ratio_ci(ben_v, ben_m, IDX)

            def selective(ix, ref):
                """Share of harm removed plus share of benefit kept, minus 1. Zero means a pure volume knob."""
                return (np.mean((ref - eff_v)[ix], axis=-1) / np.mean(ref[ix], axis=-1)
                        + np.mean(ben_v[ix], axis=-1) / np.mean(ben_m[ix], axis=-1) - 1)

            sel, sel_pool = {}, {}
            for out, ref in ((sel, eff_m), (sel_pool, eff_pool)):
                with np.errstate(divide="ignore", invalid="ignore"):
                    th = float(selective(np.arange(48), ref))
                    bo, ja = selective(IDX, ref), np.array([selective(np.delete(np.arange(48), j), ref) for j in range(48)])
                bo = np.where(np.isfinite(bo), bo, np.nan)
                out["est"], (out["lo"], out["hi"]) = th, bca(th, bo, ja)
            rows.append({"variant": name, "family": family, "baseline_source": source, "model": m,
                         "si_false_main": si_m.mean(), "si_false_variant": si_v.mean(), "si_change": harm["est"], "si_low": harm["ci_low"], "si_high": harm["ci_high"],
                         "si_toward": harm["toward"], "si_away": harm["away"], "si_mcnemar_p": harm["mcnemar_p"], "si_item_p": harm["item_p"],
                         "si_change_vs_pool": harm_pool["est"], "si_pool_low": harm_pool["ci_low"], "si_pool_high": harm_pool["ci_high"], "si_pool_p": harm_pool["item_p"],
                         "sc_acc_main": sc_m.mean(), "sc_acc_variant": sc_v.mean(), "sc_change": bene["est"], "sc_low": bene["ci_low"], "sc_high": bene["ci_high"],
                         "sc_toward": bene["toward"], "sc_away": bene["away"], "sc_mcnemar_p": bene["mcnemar_p"], "sc_item_p": bene["item_p"],
                         "nb_false_used": nv_y.mean(), "nb_acc_used": nv_c.mean(),
                         "harm_removed": x["est"], "harm_low": x["ci_low"], "harm_high": x["ci_high"], "harm_share": fx["est"], "harm_share_low": fx["ci_low"], "harm_share_high": fx["ci_high"],
                         "benefit_kept": y["est"], "benefit_low": y["ci_low"], "benefit_high": y["ci_high"], "benefit_share": fy["est"], "benefit_share_low": fy["ci_low"], "benefit_share_high": fy["ci_high"],
                         "effect_in_frame": within["est"], "eif_low": within["ci_low"], "eif_high": within["ci_high"], "eif_item_p": within["item_p"], "eif_mcnemar_p": within["mcnemar_p"],
                         "benefit_in_frame_p": within_ben["item_p"],
                         "sc_false": S(LABEL_RUN, m, SCL).mean() if name == "label" else S(run, m, SC).mean(), "main_effect": eff_m.mean(), "main_benefit": ben_m.mean(),
                         "selectivity": sel["est"], "sel_low": sel["lo"], "sel_high": sel["hi"], "selectivity_pool": sel_pool["est"], "selp_low": sel_pool["lo"], "selp_high": sel_pool["hi"]})
    t = pd.DataFrame(rows)
    fam = t.variant != "label"  # Holm over the 8 variants x 2 models x 2 sides; the label row is a reference only
    n = fam.sum()
    adj = holm(np.r_[t.loc[fam, "si_item_p"], t.loc[fam, "sc_item_p"]])
    t.loc[fam, "si_holm_item"], t.loc[fam, "sc_holm_item"] = adj[:n], adj[n:]
    adj = holm(np.r_[t.loc[fam, "si_mcnemar_p"], t.loc[fam, "sc_mcnemar_p"]])
    t.loc[fam, "si_holm_trial"], t.loc[fam, "sc_holm_trial"] = adj[:n], adj[n:]
    t.loc[fam, "si_pool_holm"] = holm(t.loc[fam, "si_pool_p"].to_numpy())
    save(t, "q3_tradeoff")
    # Frame baselines: does the frame itself move no-memory answers?
    rows = []
    for m in SUSCEPTIBLE:
        for name, run in [("tutor", FIX + "tutor"), ("patient", PATIENT)]:
            f, c = compare(S(run, m, NB), S(MAIN, m, NB)), compare(S(run, m, NB, "correct"), S(MAIN, m, NB, "correct"))
            l = compare(S(run, m, LB), S(run, m, SI))
            rows.append({"frame": name, "model": m, "nb_false": S(run, m, NB).mean(), "nb_acc": S(run, m, NB, "correct").mean(), "lb_false": S(run, m, LB).mean(),
                         "nb_false_change": f["est"], "f_low": f["ci_low"], "f_high": f["ci_high"], "nb_acc_change": c["est"], "c_low": c["ci_low"], "c_high": c["ci_high"],
                         "label_change": l["est"], "l_low": l["ci_low"], "l_high": l["ci_high"], "l_toward": l["toward"], "l_away": l["away"], "l_p": l["mcnemar_p"]})
    save(pd.DataFrame(rows), "q3_frame_baselines")
    # Useful-memory checks (no replicate of a no-memory control; 16 answers per cell).
    u = ALL[ALL.kind != "factual"].copy()
    u = u[u.model.isin(SUSCEPTIBLE) & u.run.isin([MAIN] + [FIX + v for v in ["tutor", "rule", "answer_first", "memory_gate"]])]
    g = u.groupby(["run", "model", "kind"]).agg(n=("correct", "size"), right=("correct", "sum")).reset_index()
    save(g, "q3_useful_checks")
    gate = ALL[ALL.run == FIX + "memory_gate"].copy()
    gate["withheld"] = gate.note.fillna("").str.contains("withheld")
    save(gate.groupby(["model", "kind", "condition"]).agg(n=("withheld", "size"), withheld=("withheld", "sum"), right=("correct", "sum")).reset_index(), "q3_gate_decisions")
    # answer_first: the draft is a free no-memory sample inside every trial.
    a = ALL[(ALL.run == FIX + "answer_first") & (ALL.kind == "factual")].copy()
    rows = []
    for (m, cond), g2 in a.groupby(["model", "condition"]):
        draft = []
        for r in g2.itertuples():
            txt = (r.note or "").replace("draft before memory: ", "", 1)
            omap = next(x for x in OMAPS if x[0] == (r.case_id, r.rep))[1]
            d = final_letter(txt, list(omap))
            draft.append(omap.get(d))
        g2 = g2.assign(draft=draft)
        wrong = g2.case_id.map(lambda i: CASES[i]["incorrect_option"])
        ans = g2.case_id.map(lambda i: CASES[i]["answer"])
        rows.append({"model": m, "condition": cond, "draft_false": float((g2.draft == wrong).mean()), "final_false": g2.y.mean(), "draft_correct": float((g2.draft == ans).mean()), "final_correct": g2.correct.mean(),
                     "draft_right_final_false": int(((g2.draft == ans) & (g2.y == 1)).sum()), "draft_false_final_right": int(((g2.draft == wrong) & (g2.correct == 1)).sum())})
    save(pd.DataFrame(rows), "q3_answer_first_draft")
    # Is the combined tutor frame more than the sum of its parts?
    rows = []
    parts = ["role_only", "heading_only", "student_only"]
    for m in SUSCEPTIBLE:
        for ref_name, ref in [("main run only", S(MAIN, m, SI)), ("mean of 5 identical runs", pooled_si(m))]:
            t_ = S(FIX + "tutor", m, SI)
            ps = [S(SPLIT + p, m, SI) for p in parts]
            M, T, P = item_means(ref, ITEMS), item_means(t_, ITEMS), [item_means(p, ITEMS) for p in ps]
            comb, summed = M - T, sum(M - p for p in P)
            inter = comb - summed
            c, s_, i = mean_ci(comb, IDX), mean_ci(summed, IDX), mean_ci(inter, IDX)
            pv = mc_signflip_p(inter)

            def lo(v):
                q = np.clip(v, 1e-3, 1 - 1e-3)
                return np.log(q / (1 - q))

            def stat(ix):
                mm = np.mean(M[ix], axis=-1)
                return (lo(mm) - lo(np.mean(T[ix], axis=-1))) - sum(lo(mm) - lo(np.mean(p[ix], axis=-1)) for p in P)

            theta = float(stat(np.arange(48)))
            boots = stat(IDX)
            jack = np.array([stat(np.delete(np.arange(48), j)) for j in range(48)])
            llo, lhi = bca(theta, boots, jack)
            # Multiplicative prediction on the share of effect left above the main baseline.
            nb = item_means(S(MAIN, m, NB), ITEMS).mean()
            left = np.prod([(p.mean() - nb) / (M.mean() - nb) for p in P])
            rows.append({"model": m, "reference": ref_name, "ref_rate": M.mean(), "tutor_rate": T.mean(), **{f"{n}_rate": p.mean() for n, p in zip(parts, P)},
                         **{f"{n}_reduction": M.mean() - p.mean() for n, p in zip(parts, P)},
                         "combined": c["est"], "combined_low": c["ci_low"], "combined_high": c["ci_high"], "sum_parts": s_["est"], "sum_low": s_["ci_low"], "sum_high": s_["ci_high"],
                         "interaction": i["est"], "int_low": i["ci_low"], "int_high": i["ci_high"], "int_p": pv,
                         "logodds_interaction": theta, "lo_low": llo, "lo_high": lhi,
                         "multiplicative_prediction": nb + left * (M.mean() - nb)})
    save(pd.DataFrame(rows), "q3_tutor_sum_of_parts")
    # The same question on the true-memory side (no replicate of this arm exists, so main run only).
    rows = []
    for m in SUSCEPTIBLE:
        M, T = item_means(S(MAIN, m, SC, "correct"), ITEMS), item_means(S(FIX + "tutor", m, SC, "correct"), ITEMS)
        P = [item_means(S(SPLIT + p, m, SC, "correct"), ITEMS) for p in parts]
        comb, summed = T - M, sum(p - M for p in P)
        c, s_, i = mean_ci(comb, IDX), mean_ci(summed, IDX), mean_ci(comb - summed, IDX)
        pat = item_means(S(PATIENT, m, SC, "correct"), ITEMS)
        cp = mean_ci((pat - M) - summed, IDX)

        def lo2(v):
            q = np.clip(v, 1e-3, 1 - 1e-3)
            return np.log(q / (1 - q))

        def stat2(ix):
            mm = lo2(np.mean(M[ix], axis=-1))
            return (lo2(np.mean(T[ix], axis=-1)) - mm) - sum(lo2(np.mean(p[ix], axis=-1)) - mm for p in P)

        th = float(stat2(np.arange(48)))
        lo_l, lo_h = bca(th, stat2(IDX), np.array([stat2(np.delete(np.arange(48), j)) for j in range(48)]))
        rows.append({"model": m, "main_acc": M.mean(), "tutor_acc": T.mean(), **{f"{n}_acc": p.mean() for n, p in zip(parts, P)}, "combined": c["est"], "combined_low": c["ci_low"], "combined_high": c["ci_high"],
                     "sum_parts": s_["est"], "sum_low": s_["ci_low"], "sum_high": s_["ci_high"], "interaction": i["est"], "int_low": i["ci_low"], "int_high": i["ci_high"], "int_p": mc_signflip_p(comb - summed),
                     "logodds_interaction": th, "lo_low": lo_l, "lo_high": lo_h, "patient_interaction": cp["est"], "pint_low": cp["ci_low"], "pint_high": cp["ci_high"], "pint_p": mc_signflip_p((pat - M) - summed)})
    save(pd.DataFrame(rows), "q3_tutor_sum_of_parts_benefit")


OMAPS: list = []


# ------------------------------------------------------------------ Q4 wrong source


def q4() -> None:
    r = "stale-source-20261105"
    rows = []
    for m in SUSCEPTIBLE:
        c = compare(S(r, m, SC), S(r, m, NB))
        a = compare(S(r, m, SC, "correct"), S(r, m, NB, "correct"))
        pv = compare(S(r, m, NB), S(MAIN, m, NB))
        ms = compare(S(r, m, SC, "correct"), S(MAIN, m, SC, "correct"))
        n_, s_ = rate(S(r, m, NB)), rate(S(r, m, SC))
        kept = ratio_ci(item_means(S(r, m, NB) - S(r, m, SC), ITEMS), item_means(S(r, m, NB), ITEMS), IDX)
        rows.append({"model": m, "passage_only_follow": n_["est"], "po_low": n_["ci_low"], "po_high": n_["ci_high"], "passage_plus_truth_follow": s_["est"], "pt_low": s_["ci_low"], "pt_high": s_["ci_high"],
                     "follow_change": c["est"], "change_low": c["ci_low"], "change_high": c["ci_high"], "toward": c["toward"], "away": c["away"], "mcnemar_p": c["mcnemar_p"], "item_p": c["item_p"],
                     "items_up": c["items_up"], "items_down": c["items_down"], "acc_passage_only": S(r, m, NB, "correct").mean(), "acc_with_truth": S(r, m, SC, "correct").mean(),
                     "acc_change": a["est"], "acc_low": a["ci_low"], "acc_high": a["ci_high"],
                     "main_nb_false": S(MAIN, m, NB).mean(), "main_sc_acc": S(MAIN, m, SC, "correct").mean(),
                     "passage_rise": pv["est"], "pr_low": pv["ci_low"], "pr_high": pv["ci_high"],
                     "truth_acc_vs_main_sc": ms["est"], "tv_low": ms["ci_low"], "tv_high": ms["ci_high"],
                     "share_of_following_removed": kept["est"], "sr_low": kept["ci_low"], "sr_high": kept["ci_high"]})
    save(add_holm(pd.DataFrame(rows)), "q4_wrong_source")


# ------------------------------------------------------------------ Q5 label on true memories


def q5() -> None:
    r = "label-correct-20261105"
    rows = []
    for m in FOLLOWUP_MODELS:
        scl, sc, nb = S(r, m, SCL, "correct"), S(MAIN, m, SC, "correct"), S(MAIN, m, NB, "correct")
        lv, ln, sn = compare(scl, sc), compare(scl, nb), compare(sc, nb)
        fy, fsc = compare(S(r, m, SCL), S(MAIN, m, SC)), S(MAIN, m, SC).mean()
        den = item_means(sc - nb, ITEMS)
        fr = ratio_ci(item_means(scl - nb, ITEMS), den, IDX) if sn["est"] >= 0.05 else {}
        h = FACT[(FACT.run == r) & (FACT.model == m)].provider.value_counts().to_dict()
        rows.append({"model": m, "acc_no_belief": nb.mean(), "acc_true_memory": sc.mean(), "acc_true_labelled": scl.mean(), "false_true_memory": fsc, "false_true_labelled": S(r, m, SCL).mean(),
                     "label_change": lv["est"], "lc_low": lv["ci_low"], "lc_high": lv["ci_high"], "toward": lv["toward"], "away": lv["away"], "mcnemar_p": lv["mcnemar_p"], "item_p": lv["item_p"], "items_up": lv["items_up"], "items_down": lv["items_down"],
                     "labelled_vs_nb": ln["est"], "ln_low": ln["ci_low"], "ln_high": ln["ci_high"], "ln_mcnemar_p": ln["mcnemar_p"], "ln_item_p": ln["item_p"],
                     "unlabelled_vs_nb": sn["est"], "sn_low": sn["ci_low"], "sn_high": sn["ci_high"],
                     "false_change": fy["est"], "fc_low": fy["ci_low"], "fc_high": fy["ci_high"],
                     "benefit_kept": fr.get("est", np.nan), "bk_low": fr.get("ci_low", np.nan), "bk_high": fr.get("ci_high", np.nan), "hosts": json.dumps(h), "main_host": FACT[(FACT.run == MAIN) & (FACT.model == m)].provider.iloc[0]})
    t = pd.DataFrame(rows)
    adj = holm(np.r_[t.item_p, t.ln_item_p])
    t["holm_item_label"], t["holm_item_vs_nb"] = adj[:len(t)], adj[len(t):]
    adj = holm(np.r_[t.mcnemar_p, t.ln_mcnemar_p])
    t["holm_trial_label"], t["holm_trial_vs_nb"] = adj[:len(t)], adj[len(t):]
    save(t, "q5_label_on_true")


# ------------------------------------------------------------------ Q6 base vs instruct


LB_ = "local-base-20261105"
LI = "local-instruct-20261105"
ARM = {"nemo-base-local": (LB_, "nemo-base-local"), "nemo-instruct-local": (LI, "nemo-instruct-local"),
       "nemo-instruct-local-chat": (LI, "nemo-instruct-local-chat"), "hosted": (MAIN, NEMO)}


def logit_s(s: pd.Series, eps: float = 1e-4) -> pd.Series:
    p = s.clip(eps, 1 - eps)
    return np.log(p / (1 - p))


def q6() -> None:
    def A(arm, cond, value="y"):
        run, model = ARM[arm]
        return S(run, model, cond, value)

    rows = []
    for arm in ARM:
        for cond in [NB, SI, ST, LB, UN, SC]:
            y, c, p = rate(A(arm, cond)), rate(A(arm, cond, "correct")), rate(A(arm, cond, "p_inc"))
            yr = rate(A(arm, cond, "y_rescued"))
            rows.append({"arm": arm, "condition": cond, "usable": y["n"], "false_rate": y["est"], "low": y["ci_low"], "high": y["ci_high"], "accuracy": c["est"], "mean_p_false": p["est"], "p_low": p["ci_low"], "p_high": p["ci_high"], "false_rate_rescued": yr["est"], "usable_rescued": yr["n"]})
    save(pd.DataFrame(rows), "q6_rates")
    # Within-arm effects, on answers (as logged and with the comma answers read) and on probabilities.
    comps = [("memory effect", SI, NB), ("stated effect", ST, NB), ("unrelated memory", UN, NB), ("true memory", SC, NB), ("label vs stored", LB, SI), ("label vs no belief", LB, NB)]
    rows = []
    for arm in ARM:
        for name, a, b in comps:
            e = compare(A(arm, a), A(arm, b))
            r = compare(A(arm, a, "y_rescued"), A(arm, b, "y_rescued"))
            p = compare(A(arm, a, "p_inc"), A(arm, b, "p_inc"), binary=False)
            lo = compare(logit_s(A(arm, a, "p_inc")), logit_s(A(arm, b, "p_inc")), binary=False)
            rows.append({"arm": arm, "comparison": name, "ans_est": e["est"], "ans_low": e["ci_low"], "ans_high": e["ci_high"], "toward": e["toward"], "away": e["away"], "mcnemar_p": e["mcnemar_p"], "item_p": e["item_p"], "pairs": e["pairs"],
                         "ans_rescued": r["est"], "ans_rescued_low": r["ci_low"], "ans_rescued_high": r["ci_high"], "toward_rescued": r["toward"], "away_rescued": r["away"],
                         "prob_est": p["est"], "prob_low": p["ci_low"], "prob_high": p["ci_high"], "prob_p": p["item_p"], "logodds_est": lo["est"], "lo_low": lo["ci_low"], "lo_high": lo["ci_high"]})
    t = save(pd.DataFrame(rows), "q6_effects")
    # Share of the effect the label removes.
    rows = []
    for arm in ARM:
        for meas, val in [("answers", "y"), ("answers, comma read", "y_rescued"), ("probabilities", "p_inc")]:
            si, lb, nb = A(arm, SI, val), A(arm, LB, val), A(arm, NB, val)
            ids = pd.concat([si, lb, nb], axis=1).dropna().index
            num, den = item_means((si - lb).reindex(ids), ITEMS), item_means((si - nb).reindex(ids), ITEMS)
            f = ratio_ci(num, den, IDX)
            rows.append({"arm": arm, "measure": meas, "fraction_removed": f["est"], "low": f["ci_low"], "high": f["ci_high"], "fieller_low": f["fieller_low"], "fieller_high": f["fieller_high"]})
    save(pd.DataFrame(rows), "q6_label_fraction")
    # Interactions: base minus instruct on the same plain-text prompt (the fair pair), and base minus chat.
    rows = []
    for other in ["nemo-instruct-local", "nemo-instruct-local-chat", "hosted"]:
        for name, a, b in comps:
            for meas, val, binary in [("answers", "y", True), ("answers, comma read", "y_rescued", True), ("probabilities", "p_inc", False), ("log-odds of probability", "logit", False)]:
                g = (lambda arm, c: logit_s(A(arm, c, "p_inc"))) if val == "logit" else (lambda arm, c: A(arm, c, val))
                # Keep only (item, rep) pairs observed in both conditions within each arm.
                d1 = (g("nemo-base-local", a) - g("nemo-base-local", b)).dropna()
                d2 = (g(other, a) - g(other, b)).dropna()
                c = contrast([(1, d1), (-1, d2)], binary=binary)
                rows.append({"base_minus": other, "comparison": name, "measure": meas, "base": float(np.nanmean(item_means(d1, ITEMS))), "other": float(np.nanmean(item_means(d2, ITEMS))), "est": c["est"], "ci_low": c["ci_low"], "ci_high": c["ci_high"], "item_p": c["item_p"], "items_up": c["items_up"], "items_down": c["items_down"]})
    save(pd.DataFrame(rows), "q6_base_vs_instruct")
    # Log-odds depend on the clip and on how peaked a model is, so show both.
    rows = []
    for eps in (1e-4, 1e-3, 1e-2):
        vals = {arm: float(np.nanmean(item_means(logit_s(A(arm, SI, "p_inc"), eps) - logit_s(A(arm, NB, "p_inc"), eps), ITEMS))) for arm in ARM}
        c = contrast([(1, logit_s(A("nemo-base-local", SI, "p_inc"), eps) - logit_s(A("nemo-base-local", NB, "p_inc"), eps)), (-1, logit_s(A("nemo-instruct-local", SI, "p_inc"), eps) - logit_s(A("nemo-instruct-local", NB, "p_inc"), eps))], binary=False)
        rows.append({"clip": eps, **vals, "base_minus_instruct": c["est"], "ci_low": c["ci_low"], "ci_high": c["ci_high"]})
    save(pd.DataFrame(rows), "q6_logodds_clip")
    rows = []
    for arm in ARM:
        run, model = ARM[arm]
        d = _INDEX[(run, model, NB)]
        top = d[["p_inc", "p_ans"]]
        rows.append({"arm": arm, "median_false_prob_no_belief": float(d.p_inc.median()), "share_false_prob_below_1pct": float((d.p_inc < 0.01).mean()), "median_answer_prob_no_belief": float(d.p_ans.median())})
    save(pd.DataFrame(rows), "q6_peakedness")
    # Direct arm comparisons, same condition.
    rows = []
    for a1, a2, label in [("nemo-base-local", "nemo-instruct-local", "base minus instruct, same prompt"), ("nemo-instruct-local-chat", "nemo-instruct-local", "chat minus completion, same weights"), ("nemo-instruct-local-chat", "hosted", "local chat minus hosted")]:
        for cond in [NB, SI, ST, LB, UN, SC]:
            c = compare(A(a1, cond), A(a2, cond))
            p = compare(A(a1, cond, "p_inc"), A(a2, cond, "p_inc"), binary=False)
            rows.append({"comparison": label, "condition": cond, "a_rate": A(a1, cond).mean(), "b_rate": A(a2, cond).mean(), "est": c["est"], "ci_low": c["ci_low"], "ci_high": c["ci_high"], "toward": c["toward"], "away": c["away"], "mcnemar_p": c["mcnemar_p"], "item_p": c["item_p"],
                         "prob_est": p["est"], "prob_low": p["ci_low"], "prob_high": p["ci_high"]})
    save(pd.DataFrame(rows), "q6_arm_differences")
    # Reproduction: hosted vs local chat. The local reply stops at 16 tokens, so the first answer line is the fair hosted score.
    rows = []
    for cond in [NB, SI, ST, LB, UN, SC]:
        loc, h_last, h_first = A("nemo-instruct-local-chat", cond), A("hosted", cond), A("hosted", cond, "y_first")
        c = compare(loc, h_first)
        rows.append({"condition": cond, "local_chat": loc.mean(), "hosted_final_line": h_last.mean(), "hosted_first_line": h_first.mean(), "local_minus_hosted_first": c["est"], "ci_low": c["ci_low"], "ci_high": c["ci_high"], "toward": c["toward"], "away": c["away"], "mcnemar_p": c["mcnemar_p"], "item_p": c["item_p"],
                     "p_local": A("nemo-instruct-local-chat", cond, "p_inc").mean(), "p_hosted": A("hosted", cond, "p_inc").mean(),
                     "item_r_answers": np.corrcoef(item_means(loc, ITEMS), item_means(h_first, ITEMS))[0, 1],
                     "item_r_probs": np.corrcoef(item_means(A("nemo-instruct-local-chat", cond, "p_inc"), ITEMS), item_means(A("hosted", cond, "p_inc"), ITEMS))[0, 1],
                     "same_answer_share": float(np.mean(np.equal(*FACT_LETTER("nemo-instruct-local-chat", cond).align(FACT_LETTER("hosted", cond)))))})
    rep = pd.DataFrame(rows)
    rep.loc[:, "holm_mcnemar"] = holm(rep.mcnemar_p.to_numpy())
    rep.loc[:, "holm_item"] = holm(rep.item_p.to_numpy())
    save(rep, "q6_reproduction")
    # Local chat against the mean of the five hosted runs of the same stored-belief prompt.
    p = pooled_si(NEMO)
    c = contrast([(1, A("nemo-instruct-local-chat", SI)), (-1, p)], binary=False)
    RESULTS["q6_repro_vs_pool"] = {"pool": float(p.mean()), **c}
    e = {}
    for arm in ["hosted", "nemo-instruct-local-chat"]:
        v = "y_first" if arm == "hosted" else "y"
        e[arm] = (A(arm, SI, v) - A(arm, NB, v))
    c = contrast([(1, e["nemo-instruct-local-chat"]), (-1, e["hosted"])])
    l = contrast([(1, A("nemo-instruct-local-chat", LB) - A("nemo-instruct-local-chat", SI)), (-1, A("hosted", LB, "y_first") - A("hosted", SI, "y_first"))])
    RESULTS["q6_repro_effect"] = {"effect_local": float(item_means(e["nemo-instruct-local-chat"], ITEMS).mean()), "effect_hosted_first": float(item_means(e["hosted"], ITEMS).mean()), **c}
    RESULTS["q6_repro_label"] = l
    # Unparseable trials: how they fall, and what they were.
    un = FACT[FACT.run.isin([LB_, LI]) & (FACT.score == "unparseable")]
    save(un.groupby(["model", "condition"]).size().reset_index(name="unparseable"), "q6_unparseable")
    RESULTS["q6_unparseable_rescued"] = {m: {"logged": int(len(g)), "read_with_comma": int(g.y_rescued.notna().sum())} for m, g in un.groupby("model")}


def FACT_LETTER(arm: str, cond: str) -> pd.Series:
    """Option chosen on the first answer line, reduced to correct/false/other/none, for a same-answer check."""
    run, model = ARM[arm]
    d = _INDEX[(run, model, cond)]
    col, cor = ("y_first", "correct_first") if arm == "hosted" else ("y", "correct")
    return d[col].fillna(-1) * 2 + d[cor].fillna(-1)


# ------------------------------------------------------------------ Q7 MemSyco-Bench


def q7() -> None:
    rows = read_rows("memsyco-bench-20261105")
    last = {r["trial_id"]: r for r in rows}
    t = pd.DataFrame([{"trial_id": r["trial_id"], "case_id": r["case_id"], "condition": r["condition"], "alias": r["model_alias"], "model": ALIAS.get(r["model_alias"], r["model_alias"]),
                       "provider": r.get("provider"), "finish": r.get("finish_reason"), "judge_provider": r.get("judge_provider"), "source_id": r.get("source_id"),
                       "correct": (r.get("judgment") or {}).get("objective_correctness"), "endorsed": (r.get("judgment") or {}).get("preference_misconception_endorsed"),
                       "contaminated": (r.get("judgment") or {}).get("preference_contamination")} for r in last.values()])
    scored = pd.read_csv(RUNS / "memsyco-bench-20261105" / "scored.csv")
    chk = t.merge(scored, on="trial_id", suffixes=("", "_s"))
    assert len(chk) == 2000 and (chk.endorsed == chk.endorsed_s).all() and (chk.correct == chk.correct_s).all()
    items = sorted(t.case_id.unique())
    assert len(items) == 100
    idx = boot_indices(100, B, SEED)
    conds = ["no_memory", "full_dialogue", "snippet", "snippet_labelled"]

    def V(m, c, val="endorsed", data=t):
        g = data[(data.model == m) & (data.condition == c)].set_index("case_id")[val].astype(float)
        return g.reindex(items).to_numpy()

    def diff(m, a, b, val="endorsed", data=t):
        d = V(m, a, val, data) - V(m, b, val, data)
        o = mean_ci(d, idx)
        ok = d[np.isfinite(d)]
        o.update(toward=int((ok > 0).sum()), away=int((ok < 0).sum()))
        o["mcnemar_p"] = mcnemar_exact(o["toward"], o["away"])
        return o

    rate_rows, pair_rows = [], []
    for m in FOLLOWUP_MODELS:
        for c in conds:
            r = mean_ci(V(m, c), idx)
            acc = mean_ci(V(m, c, "correct"), idx)
            n = int(np.nansum(V(m, c)))
            w = stats.binomtest(n, 100).proportion_ci(method="wilson")
            rate_rows.append({"model": m, "condition": c, "sycophancy": r["est"], "low": r["ci_low"], "high": r["ci_high"], "wilson_low": w.low, "wilson_high": w.high, "accuracy": acc["est"], "acc_low": acc["ci_low"], "acc_high": acc["ci_high"], "contamination": np.nanmean(V(m, c, "contaminated"))})
        for a, b in [("full_dialogue", "no_memory"), ("snippet", "no_memory"), ("snippet_labelled", "no_memory"), ("snippet_labelled", "snippet"), ("full_dialogue", "snippet")]:
            o = diff(m, a, b)
            ac = diff(m, a, b, "correct")
            pair_rows.append({"model": m, "comparison": f"{a} vs {b}", "est": o["est"], "ci_low": o["ci_low"], "ci_high": o["ci_high"], "toward": o["toward"], "away": o["away"], "mcnemar_p": o["mcnemar_p"], "acc_change": ac["est"], "acc_low": ac["ci_low"], "acc_high": ac["ci_high"]})
    save(pd.DataFrame(rate_rows), "q7_rates")
    pairs = pd.DataFrame(pair_rows)
    pairs["holm_p"] = holm(pairs.mcnemar_p.to_numpy())
    save(pairs, "q7_paired")
    # Share of the snippet effect the label removes.
    rows = []
    for m in FOLLOWUP_MODELS:
        n, s, l = V(m, "no_memory"), V(m, "snippet"), V(m, "snippet_labelled")
        f = ratio_ci(s - l, s - n, idx)
        rows.append({"model": m, "fraction_removed": f["est"], "low": f["ci_low"], "high": f["ci_high"]})
    save(pd.DataFrame(rows), "q7_label_fraction")
    # Model comparisons: does the memory effect differ?
    rows, omni = [], []
    for cond in ["snippet", "full_dialogue"]:
        eff = {m: V(m, cond) - V(m, "no_memory") for m in FOLLOWUP_MODELS}
        for a, b in itertools.combinations(FOLLOWUP_MODELS, 2):
            d = eff[a] - eff[b]
            o = mean_ci(d, idx)
            rows.append({"memory": cond, "pair": f"{a} minus {b}", "est": o["est"], "ci_low": o["ci_low"], "ci_high": o["ci_high"], "item_p": exact_signflip_p(d)})
        for label, ms in [("all five", FOLLOWUP_MODELS), ("without Qwen", [m for m in FOLLOWUP_MODELS if m != "qwen-small"])]:
            M = np.column_stack([eff[m] for m in ms])
            obs = M.mean(axis=0).var()
            rng = np.random.default_rng(SEED)
            hits = 0
            for _ in range(20000):
                hits += rng.permuted(M, axis=1).mean(axis=0).var() >= obs - 1e-12
            omni.append({"memory": cond, "models": label, "spread_points": 100 * float(M.mean(axis=0).max() - M.mean(axis=0).min()), "perm_p": (hits + 1) / 20001})
    d = pd.DataFrame(rows)
    d["holm_p"] = d.groupby("memory").item_p.transform(lambda s: holm(s.to_numpy()))
    save(d, "q7_model_contrasts")
    save(pd.DataFrame(omni), "q7_equal_effects")
    # Main study against the benchmark, model by model.
    rows = []
    for m in FOLLOWUP_MODELS:
        e = compare(S(MAIN, m, SI), S(MAIN, m, NB))
        b = pairs[(pairs.model == m) & (pairs.comparison == "snippet vs no_memory")].iloc[0]
        fd = pairs[(pairs.model == m) & (pairs.comparison == "full_dialogue vs no_memory")].iloc[0]
        rows.append({"model": m, "mcq_effect": e["est"], "mcq_low": e["ci_low"], "mcq_high": e["ci_high"], "bench_snippet": b.est, "bs_low": b.ci_low, "bs_high": b.ci_high, "bench_dialogue": fd.est, "bd_low": fd.ci_low, "bd_high": fd.ci_high})
    save(pd.DataFrame(rows), "q7_mcq_vs_bench")
    # Published Llama-3.1-8B figures (Xiang et al. 2026), from report/literature/comparison_table.md.
    pub = [("no memory", "no_memory", 0.2992, 0.2992), ("full dialogue", "full_dialogue", 0.5017, 0.5017), ("memory (ours: snippet; theirs: memory systems)", "snippet", 0.5652, 0.6133)]
    r = pd.DataFrame(rate_rows).set_index(["model", "condition"])
    rows = []
    for name, c, lo, hi in pub:
        o = r.loc[("llama-8b", c)]
        rows.append({"measure": name, "published_low": lo, "published_high": hi, "ours": o.sycophancy, "ours_low": o.low, "ours_high": o.high, "published_in_our_ci": bool(o.low <= hi and o.high >= lo)})
    for name, a, lo, hi in [("rise, full dialogue", "full_dialogue vs no_memory", 0.2025, 0.2025), ("rise, memory", "snippet vs no_memory", 0.266, 0.314)]:
        o = pairs[(pairs.model == "llama-8b") & (pairs.comparison == a)].iloc[0]
        rows.append({"measure": name, "published_low": lo, "published_high": hi, "ours": o.est, "ours_low": o.ci_low, "ours_high": o.ci_high, "published_in_our_ci": bool(o.ci_low <= hi and o.ci_high >= lo)})
    save(pd.DataFrame(rows), "q7_published_llama")
    # Sensitivity and judge checks.
    rows = []
    clean = t[t.finish != "length"]
    for m in ["gemma-moe", "qwen-small"]:
        for c in ["snippet", "full_dialogue"]:
            o = diff(m, c, "no_memory", data=clean)
            rows.append({"model": m, "comparison": f"{c} vs no_memory, truncated replies dropped", "est": o["est"], "ci_low": o["ci_low"], "ci_high": o["ci_high"], "truncated_in_condition": int(((t.model == m) & (t.condition == c) & (t.finish == "length")).sum())})
    save(pd.DataFrame(rows), "q7_truncation")
    cross = t.groupby(["correct", "endorsed"]).size().reset_index(name="n")
    save(cross, "q7_judge_crosstab")
    byj = t.groupby(["judge_provider", "condition"]).endorsed.agg(["mean", "size"]).reset_index()
    save(byj, "q7_judge_host")
    RESULTS["q7"] = {"llama_hosts": t[t.model == "llama-8b"].provider.value_counts().to_dict(), "judge_hosts": t.judge_provider.value_counts().to_dict(),
                     "truncated": t[t.finish == "length"].groupby("alias").size().to_dict(), "unique_sources": int(t.source_id.nunique()), "pool_size": 300}


# ------------------------------------------------------------------ Q8 spend


def q8() -> None:
    rows = []
    for path in sorted(RUNS.rglob("trials.jsonl")):
        run = str(path.parent.relative_to(RUNS))
        recs = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        usage = sum(((r.get("usage") or {}).get("cost") or 0.0) for r in recs)
        top = sum((r.get("cost") or 0.0) for r in recs)
        # Bench rows carry answer + judge in `cost`; `usage.cost` holds the answer only. Other runs have no top-level cost.
        bench = any("judge_raw" in r or "judgment" in r for r in recs)
        cost = top if bench else usage
        group = "local (free)" if run.startswith("local-") else "smoke tests" if run.startswith("smoke") else "27 Oct rounds" if run.endswith("20261027") else "5 Nov follow-ups"
        upstream = sum(((r.get("usage") or {}).get("cost_details") or {}).get("upstream_inference_cost") or 0.0 for r in recs if (r.get("usage") or {}).get("cost") == 0)
        rows.append({"run": run, "group": group, "zero_billed_upstream": upstream, "attempt_rows": len(recs), "trials": len({r["trial_id"] for r in recs}), "error_rows": sum(1 for r in recs if r.get("error")), "cost_usd": cost, "usage_field_only": usage})
    t = save(pd.DataFrame(rows), "q8_spend")
    RESULTS["q8"] = {"by_group": t.groupby("group").cost_usd.sum().to_dict(), "total": float(t.cost_usd.sum()),
                     "usage_field_total": float(t.usage_field_only.sum()), "all_attempt_rows": int(t.attempt_rows.sum()), "all_trials": int(t.trials.sum()),
                     "new_trials": int(t[t.group.isin(["5 Nov follow-ups", "local (free)"])].trials.sum()), "zero_billed_upstream": float(t.zero_billed_upstream.sum())}


def audit() -> None:
    bad = {k: v for k, v in AUDIT.items() if v["score_mismatches"]}
    RESULTS["audit"] = {"runs_checked": len(AUDIT), "trials_rescored": sum(v["trials"] for v in AUDIT.values()), "score_mismatches": sum(v["score_mismatches"] for v in AUDIT.values()), "bad": bad}
    # Option order must match the main run wherever item and rep match.
    ref = None
    orders = {}
    mism = 0
    for run in RUN_NAMES:
        for r in {x["trial_id"]: x for x in read_rows(run)}.values():
            k = (r["case_id"], int(r["rep"]))
            if k in orders:
                mism += orders[k] != r["option_map"]
            elif r.get("case_kind", "factual") == "factual":
                orders[k] = r["option_map"]
    RESULTS["audit"]["option_order_mismatches"] = int(mism)
    OMAPS.extend(orders.items())
    # Prompts in identical-prompt replicates must be byte-identical.
    def prompts(run):
        return {(r["model_alias"], r["case_id"], int(r["rep"])): json.dumps(r["request"]["messages"]) for r in read_rows(run) if r["condition"] == SI and r.get("case_kind", "factual") == "factual"}

    m = prompts(MAIN)
    diffs = 0
    for run in SI_REPLICATES[1:]:
        diffs += sum(m[k] != v for k, v in prompts(run).items())
    RESULTS["audit"]["stored_prompt_differences_across_replicates"] = int(diffs)
    hosts = {}
    for run in RUN_NAMES:
        for mdl, g in DATA[run].groupby("alias"):
            for h, n in g.provider.fillna("local").value_counts().items():
                hosts.setdefault(mdl, {}).setdefault(h, 0)
                hosts[mdl][h] += int(n)
    RESULTS["audit"]["hosts"] = hosts


audit()
for step in (q1, q2, q3, q4, q5, q6, q7, q8):
    step()
    print(step.__name__, "done", flush=True)


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    return o


(HERE / "results.json").write_text(json.dumps(clean(RESULTS), indent=1), encoding="utf-8")
print("analysis written")
