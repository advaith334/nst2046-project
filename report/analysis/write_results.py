"""Builds report/analysis/stats_results.md from the tables, so no number is typed by hand."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import MODEL_NAMES as MN
from common import MODELS, OUT, TABLES

R = json.loads((OUT / "results.json").read_text())
BAYES = json.loads((OUT / "bayes.json").read_text())


def T(name):
    return pd.read_csv(TABLES / f"{name}.csv")


def pts(x, sign=True, d=0):
    x = 100 * x
    if round(x, d) == 0:
        return "0"
    return f"{x:+.{d}f}" if sign else f"{x:.{d}f}"


def rng(lo, hi, sign=True, d=0):
    return f"[{pts(lo, sign, d)}, {pts(hi, sign, d)}]"


def est(row, sign=True, d=0):
    return f"{pts(row['est'], sign, d)} {rng(row['ci_low'], row['ci_high'], sign, d)}"


def pv(p):
    if p >= 0.9995:
        return "1.00"
    if p >= 0.1:
        return f"{p:.2f}"
    if p >= 0.001:
        return f"{p:.3f}".rstrip("0") if p >= 0.01 else f"{p:.4f}".rstrip("0")
    if p >= 0.0001:
        return f"{p:.5f}".rstrip("0")
    return "<0.0001"


def peq(p):
    return "p < 0.0001" if p < 0.0001 else f"p = {pv(p)}"


def f2(x, d=2):
    return f"{x:.{d}f}"


pt = T("t05_holm_42_tests")
key = T("t06_key_effects_item_ci")
get = lambda m, c: pt[(pt.model == m) & (pt.comparison == c)].iloc[0]
SB, LS, SS, CB = ("stored_incorrect vs no_belief", "stored_incorrect_labelled vs stored_incorrect",
                  "stated_incorrect vs stored_incorrect", "stored_correct vs no_belief")
SN, LB, UB = "stated_incorrect vs no_belief", "stored_incorrect_labelled vs no_belief", "stored_unrelated vs no_belief"
N, S, L, G, Q, C = MODELS
LABELS = {SB: "Stored false vs no belief", SN: "Stated false vs no belief", LS: "Label vs stored false", LB: "Label vs no belief",
          CB: "Stored correct vs no belief", SS: "Stated vs stored", UB: "Unrelated vs no belief"}

nsb, ssb, llsn, lsb = get(N, SB), get(S, SB), get(L, SN), get(L, SB)
gee = R["gee"]
A, B2, CC, D, E_ = (gee["three_models_two_conditions"], gee["two_mistrals_two_conditions"], gee["three_models_all_conditions"],
                    gee["five_models_two_conditions"], gee["six_models_two_conditions"])
pw = T("t13_model_contrasts_stored_vs_baseline").set_index("contrast")
ors = T("t14_odds_ratios_stored_vs_baseline").set_index("model")
chan = T("t15_channel_by_model")
by = T("t28_bayes_stored_effect_by_model")
bc = T("t29_bayes_model_contrasts")
F1, F2, F3 = "shared spreads, prior sd 2.5", "shared spreads, prior sd 5", "per-model spreads, prior sd 2.5"
bcr = lambda c, f: bc[(bc.contrast == c) & (bc.fit == f)].iloc[0]
NSm, SLm, NLm = "mistral-nemo minus mistral-small", "mistral-small minus llama-8b", "mistral-nemo minus llama-8b"
mech = T("t17_mechanism_uncertainty").set_index("model")
bands = T("t18_mechanism_by_confidence_band")
band = lambda m, b: bands[(bands.model == m) & (bands.band.str.startswith(b))].iloc[0]
shift = T("t19_shift_without_answer_change")
sh = lambda m, mem, sub: shift[(shift.model == m) & (shift.memory.str.startswith(mem)) & (shift["subset"] == sub)].iloc[0]
null = T("t20_constant_boost_null")
nl = lambda m, b: null[(null.model == m) & (null.band.str.startswith(b))].iloc[0]
acc = T("t21_mechanism_by_baseline_accuracy")
lab = T("t22_label_effect")
lb = lambda m, x: lab[(lab.model == m) & (lab.measure.str.startswith(x))].iloc[0]
rd = T("t23_rounds_baseline_vs_effect")
rr = lambda m, x: rd[(rd.model == m) & (rd["round"].str.startswith(x))].iloc[0]
same = T("t24_nemo_same_uncertainty_by_itemset")
sm = lambda s, b: same[same.item_set.str.startswith(s) & same.band.str.startswith(b)].iloc[0]
d25 = T("t25_longtail_vs_round2_difference").set_index("model")
rep = T("t26_screened_vs_new_items")
rp = lambda m, c=SB: rep[(rep.model == m) & (rep.comparison == c)].iloc[0]
stv = T("t27_stated_vs_stored_probability").set_index("model")
sub = T("t12_nemo_subgroups").set_index("subset")
srep = T("t09_single_rep_estimates")
dec = T("t11_outcome_decomposition")
cov = T("t16_probability_coverage").set_index("model")
ment = T("t32_replies_mentioning_the_belief").set_index("model")
cut = R["cutoff_sensitivity"]
corr = T("t07_correct_rate_effects")
ml = T("t30_model_level_accuracy_vs_effect").set_index("model")
rates = T("fig_rates").set_index("model")
pairs = pd.read_csv(TABLES / "fig_mechanism_pairs_mistral-nemo.csv")
near0 = float((pairs.delta.abs() < 0.05).mean())
big = float((pairs.delta > 0.5).mean())
mid = 1 - near0 - big - float((pairs.delta < -0.05).mean())
checks = pd.read_csv(TABLES / "t04_readme_checks.csv")
reps = R["reps"]

o = []
w = o.append

w(f"""# Statistics results: stored beliefs and factual answers

Report analysis for NST2046, on existing data only: no new API calls and no change to any run log.

**Rebuild everything:** `bash report/analysis/run_all.sh` (about 3 minutes). Exact package versions are in that script.

**How to read the numbers**

- "Points" means percentage points of answers. +41 means the false option was chosen 41 points more often.
- Square brackets are 95% intervals from an **item bootstrap**: we resample the 48 items, not individual trials, {R['meta']['bootstrap_resamples']:,} times (BCa method).
- **Fixed in advance** means the analysis was in the code before the main run. The 42 paired comparisons qualify: they were committed 8 seconds before the first main-run trial. Nothing was formally pre-registered.
- **After seeing the data** means everything else, including all of sections 5, 7 and 8. Treat those as exploratory: they suggest, they do not confirm.

## Summary

| Question | Answer | Key numbers | Strength |
|---|---|---|---|
| Does a stored false belief pull answers toward it? | **Yes, in Mistral Nemo** | {est(nsb)} points; holds on the 24 unscreened items alone: {pts(rp(N)['new_effect'])} {rng(rp(N)['new_low'], rp(N)['new_high'])} | Strong |
| Mistral Small too? | **Probably, but weaker evidence** | {est(ssb)} points, from only {int(ssb.items_up)} items; fails Holm when tested by item (p = {pv(ssb.p_holm_item)}) | Moderate |
| Llama, Gemma, Qwen, Claude? | **No detectable effect on chosen answers** | Largest upper limit: {pts(lsb.ci_high)} points (Llama) | Good for "no large effect"; not proof of zero |
| Does susceptibility differ across models? | **Yes** | Model × condition χ²({A['df']}) = {f2(A['chi2_bias_reduced'],1)}, p = {pv(A['p_bias_reduced'])}. Holds in every method | Strong, except Nemo vs Small on a relative scale |
| Does the label work? | **Partly, in Nemo** | Removes {pts(lb(N,'false')['est'],False)}% {rng(lb(N,'false')['ci_low'],lb(N,'false')['ci_high'],False)} of the effect; {pts(lb(N,'false')['residual_above_baseline'])} points remain | Strong that it helps; moderate that it falls short |
| Does Llama ignore memory? | **No, contrary to the README** | Right on {R['llama_preference']['right']} of {R['llama_preference']['trials']} preference checks; {pts(ment.loc[L,'stored_false_mentions'],False)}% of its stored-belief replies mention the belief | Moderate |
| Is memory strongest when a model is unsure? | **Partly: it helps predict flips, but it is neither necessary nor sufficient** | About half of Nemo's shift ({pts(cut[N]['0.99']['share_of_shift'],False)}–{pts(cut[N]['0.8']['share_of_shift'],False)}%, depending on the cut-off) came from answers it held confidently and correctly | Exploratory |
| Why did rounds 1–2 show so little? | **Not explained by low uncertainty** | Nemo was less accurate and less sure in round 2, yet the effect was {pts(d25.loc[N,'round2_effect'])} vs {pts(d25.loc[N,'longtail_effect'])} points | Post hoc |

## 1. Checking the README against the raw data

**Method.** Scoring was re-implemented from the raw responses and compared with `raw_table.csv`, trial by trial, then {R['checks']['total']} README claims were recomputed.

- **Scoring:** {R['n_scores_differ']} of {sum(x['trials'] for x in R['integrity']):,} trials differ across the five runs. The automatic scores reproduce exactly.
- **Retries:** {R['main_retry_rows']} rows in the main `trials.jsonl` are failed attempts that were retried. Only the last attempt per trial counts, as the harness intends.
- **Result table and paired tests:** every main-study rate and flip count in sections 1 and 4 matches. `paired.csv` agrees with an independent recomputation of all 42 tests.
- **Overall:** {R['checks']['total'] - R['checks']['mismatch']} of {R['checks']['total']} checks match.

### Numbers that do not match

| README says | Data says | Why it matters |
|---|---|---|
| Round 2: Llama "34% → 26%" | 34 → 26 is **with evidence only**. Without evidence: {pts(rr(L,'Round 2 harder items, no').baseline_false,False)} → {pts(rr(L,'Round 2 harder items, no').stored_false,False)}. Pooled: 32 → 26 | Small. The Nemo figures beside it are split by evidence; this one should be too |
| Round 1 cost $0.87 | Logs sum to ${[x for x in R['integrity'] if x['run']=='r1_pilot'][0]['cost_usd']:.2f}; all rounds ${R['total_cost']:.2f} | Trivial. "About $3.60" is fine |
| Qwen3.5-397B "matched Claude at ceiling in every round" | Round 3: {100*R['qwen_large_r3_correct']:.1f}% correct vs Claude {100*R['claude_r3_correct']:.0f}% | Small. "Near ceiling" is accurate; "matched" is not |
| Round 2 small models ran, then round 3 followed from them | **Nemo's round 3 ran first**: {R['chronology']['nemo_r3_start'][11:]}–{R['chronology']['nemo_r3_end'][11:]} UTC, then its round 2 at {R['chronology']['nemo_r2_start'][11:]}–{R['chronology']['nemo_r2_end'][11:]} UTC | Matters for the method story. Round 2 on Nemo cannot have prompted the long-tail round, so the report should not say each round decided the next for that arm |

### Claims stronger than the evidence

The numbers below are right, but the wording goes further than the data.

| README claim | What the data supports |
|---|---|
| "Two Mistral models are affected" | Nemo, clearly. Mistral Small's interval excludes zero, but its flips come from {int(ssb.items_up)} items and it fails Holm by item (section 2) |
| "A remembered belief pulls as hard as one the user states" | A non-significant test does not show equality. Nemo's difference is {est(get(N,SS))} points on chosen answers. On probabilities, **stored is stronger**: {est(stv.loc[N])} points, {int(stv.loc[N,'items_higher_stored'])} items vs {int(stv.loc[N,'items_higher_stated'])} (after seeing the data) |
| "The larger Mistral is less affected" | True in points. Not established on a relative scale (section 4) |
| Models are vulnerable where "unsure but not hopeless" | Only partly. Uncertainty does help predict flips, but about half of Nemo's shift comes from confident, correct answers, and Llama is as inaccurate as Nemo yet does not move (section 5) |
| Llama "may largely ignore the memory section" | **Contradicted.** It uses stored preferences and sometimes names the stored belief, then keeps its own answer (section 5) |
| Gemma 4 is "not affected" | True for final answers. Its first answer line does move a little, then it corrects itself (section 5). A small lead, not significant |
| "The label does not break useful memory" | {R['useful']['right']} of {R['useful']['trials'] - R['useful']['unreadable']} readable answers were right ({R['useful']['unreadable']} unreadable, so not quite "all"). There is no no-memory control arm, and the two correction items can be answered from the user's message alone, so these checks are weak evidence |
| "A correct stored belief cut Nemo's errors from 15% to 2%" | That is the false option only. All wrong answers fell from {100 - 100*R['nemo_correct']['no_belief']:.0f}% to {100 - 100*R['nemo_correct']['stored_correct']:.0f}% |
| Rounds 1–2 show no effect | Nemo's round 2 intervals reach {pts(rr(N,'Round 2 harder items, evidence').ci_high)} and {pts(rr(N,'Round 2 harder items, no').ci_high)} points. A moderate effect was not ruled out (section 7) |

One bug-like note: `summary.md` gives Mistral Small a mean false-option probability of {f2(R['ms_logged_only']['mean_p_stored_logged'])} under stored belief, but it chose that option {100*R['ms_recover']['rate_false_all_stored']:.0f}% of the time. The gap arises because only the logged half is averaged, and that half happens to under-represent false answers ({100*R['ms_recover']['rate_false_logged_subset_stored']:.0f}% vs {100*R['ms_recover']['rate_false_missing_subset_stored']:.0f}%). With all trials the probability is {f2(R['ms_logged_only']['mean_p_stored_all'])}, which agrees with behaviour.

## 2. Multiple comparisons: Holm across all 42 tests

*Fixed in advance.*

**Why two versions.** The README's McNemar test treats each of the 96 answers as independent, but the two reps of an item are not. So each test was run twice: on trials (exact McNemar), and on items (exact sign-flip test, where each of 48 items is one unit). The item version is the honest one for claims about "items like these".

**Result:** {R['n_survive_mcnemar']} tests survive Holm on trials and **{R['n_survive_item']} survive on items**. {R['n_no_discordant']} of the 42 tests have no flips at all, so they cannot reject anything; they are kept in the family because dropping them after seeing the data would be cherry-picking.
""")

w("| Model | Comparison | Flips toward / away | Items up / down | Change, points | Holm p, trials | Holm p, items | Verdict |\n|---|---|---|---|---|---|---|---|")
top = pt.sort_values("p_mcnemar").head(10)
for _, r in top.iterrows():
    v = "Survives both" if r.survives_item else "Survives on trials only" if r.survives_mcnemar else "Does not survive"
    w(f"| {MN[r.model]} | {LABELS[r.comparison]} | {r.toward} / {r.away} | {r.items_up} / {r.items_down} | {est(r)} | {pv(r.p_holm_mcnemar)} | {pv(r.p_holm_item)} | {v} |")
w(f"""
The other {R['n_tests'] - len(top)} tests do not survive either version. Full list: `tables/t05_holm_42_tests.csv`.

**What this means**

- **Three Nemo results stand on any reading:** stored belief, stated belief, and the label reducing the stored effect.
- **Mistral Small's stored effect survives on trials but not on items.** Its {int(ssb.toward)} flips come from {int(ssb.items_up)} items. With {int(ssb.items_up)} items all moving one way, the smallest possible p is {pv(ssb.p_item)}, so it could never pass.
- **That is a limit of the item count, not evidence against the effect.** At least {R['min_items_to_pass_holm']} items moving the same way are needed to pass the first Holm step. Its interval still excludes zero, and its probability shift is clear (section 5).
- **Nemo's "label vs no belief" and "stored correct" results also survive on trials only.** By item they are {int(get(N,LB).items_up)} up and {int(get(N,LB).items_down)} down, and {int(get(N,CB).items_down)} down, which is not enough to clear the bar.
- **Llama's stated-belief results survive neither version.** The README is right to call them exploratory.
- **The README's Bonferroni remark is correct** for the trial version: the same {R['n_survive_mcnemar']} tests pass.

## 3. Item-level uncertainty

*Fixed in advance as contrasts; the item-level intervals were added after seeing the data.*

**How the two reps were handled.** They are not independent: each item gets the same two option orders in every condition, and an item that fools a model once tends to do so again. So they are never counted separately:

1. Differences are taken within item and rep, then averaged to one value per item.
2. Items are resampled whole, keeping both reps together. Effects are means over 48 items, not 96 answers.
3. All models use the same bootstrap draws, so between-model contrasts stay paired.

**How dependent are they?** Rep 1 and rep 2 correlate at about {f2(reps[N]['mean_corr'])} for Nemo, {f2(reps[S]['mean_corr'])} for Mistral Small and {f2(reps[L]['mean_corr'])} for Llama. For Nemo's main effect, variance is {f2(nsb.design_effect)} times what trial-level analysis assumes, so 96 pairs carry about the information of {96/nsb.design_effect:.0f} independent ones.

Change in false-option rate, points, with item-level 95% intervals:
""")
w("| Model | Stored false vs no belief | Label vs stored false | Stated vs stored | Stored correct vs no belief |\n|---|---|---|---|---|")
for m in MODELS:
    w(f"| {MN[m]} | {est(get(m,SB))} | {est(get(m,LS))} | {est(get(m,SS))} | {est(get(m,CB))} |")
c_n = corr[(corr.model == N) & (corr.comparison == CB)].iloc[0]
u_n, u_s = get(N, UB), get(S, UB)
s1, s2 = srep[(srep.model == N) & (srep.comparison == SB)].iloc[0], srep[(srep.model == N) & (srep.comparison == SB)].iloc[1]
w(f"""
**What this means**

- **Stored false belief:** Nemo's rise is large, and even the low end ({pts(nsb.ci_low)}) is substantial. Small's is much smaller and rests on few items.
- **Zero means zero flips, not certainty.** Where nothing moved the bootstrap gives a zero-width interval. The fair statement is that if no item moved in 48, the true share of affected items is below about {100*R['zero_upper_95']:.0f}% (one-sided 95%).
- **Llama's stored effect is compatible with anything from {pts(lsb.ci_low)} to {pts(lsb.ci_high)}.** "No detectable effect" is right. "Ignores memory" is stronger than these data can show.
- **Stored vs stated:** Nemo's interval just includes zero, and Mistral Small's touches it. Llama is the only model that clearly moves more when told directly ({est(get(L,SS))}).
- **Stored correct:** on the false-option measure there is a floor, since Nemo has only {pts(R['nemo_rates']['no_belief'],False)}% to lose. On correct answers its rise is {est(c_n)} points.
- **Unrelated memory:** Nemo {est(u_n)}, Small {est(u_s)}. The README's "changed nothing" is fair for Nemo: anything above about {pts(u_n.ci_high)} points is ruled out.
- **Each rep alone gives the same picture:** Nemo {est(s1)} in rep 1 and {est(s2)} in rep 2.
- **Trial-level (Wilson) intervals are a little too narrow** for these effects, because they ignore item clustering.

## 4. Do models really differ?

*After seeing the data.*

**Method and why.** The outcome is binary and repeated within items, so plain logistic regression would overstate certainty. Three approaches were used because each covers a gap in the others:

| Method | Why used | Limit |
|---|---|---|
| Logistic GEE, clustered on item, small-sample corrected | Standard, assumption-light, gives population-average odds | Breaks on models with no false answers |
| Permutation and sign-flip tests on item effects | Cannot fail on sparse data, keeps all six models | Works in points, not odds |
| Bayesian hierarchical logistic model, all six models | Priors keep sparse models finite; separates item-level variation | Results for sparse models are mostly the prior |

**GEE results**

| Models and conditions | Test of model × condition | Meaning |
|---|---|---|
| Nemo, Small, Llama; stored vs no belief | χ²({A['df']}) = {f2(A['chi2_bias_reduced'],1)}, p = {pv(A['p_bias_reduced'])} | Susceptibility differs across these three |
| Same three; all six conditions | χ²({CC['df']}) = {f2(CC['chi2_bias_reduced'],1)}, {peq(CC['p_bias_reduced'])} | Models differ in how they respond across conditions |
| Nemo vs Small only | χ²({B2['df']}) = {f2(B2['chi2_bias_reduced'],2)}, p = {pv(B2['p_bias_reduced'])} | **No shown difference on the odds scale**, but with a wide interval |
| Five or six models | **Fit failed** | Coefficients reached ±{D['max_abs_coef']:.0f} and standard errors {D['max_se']:,.0f}. The software still prints a p-value, but it means nothing here, so it is not used |

**Why the fit fails.** Gemma has no false answers at baseline and Claude none at all, so the odds ratio has no finite estimate (separation).

**Alternatives that use all six models**

- Permutation test of equal effects across all six: p < 0.0001. Leaving Nemo out: p = {pv(R['perm_excl_nemo']['p'])}, so Nemo alone does not explain the spread.
- Bayesian fit: no divergences and R-hat at or below {max(v['rhat_max'] for v in BAYES.values()):.3f} in all three versions.
""")
w("| Contrast (stored vs no belief) | Points, item test | Holm p (15 pairs) | Log-odds, item-specific (Bayes) | Same, wider prior | Same, separate item spreads |\n|---|---|---|---|---|---|")
for c, nm in [(NSm, "Nemo minus Small"), (NLm, "Nemo minus Llama"), (SLm, "Small minus Llama")]:
    p_ = pw.loc[c]
    cells = []
    for fit in (F1, F2, F3):
        x = bcr(c, fit)
        cells.append(f"{x.log_or_diff:.1f} [{x.low:.1f}, {x.high:.1f}]")
    w(f"| {nm} | {pts(p_.rd_diff)} {rng(p_.rd_low, p_.rd_high)} | {pv(p_.p_holm)} | {cells[0]} | {cells[1]} | {cells[2]} |")
w(f"""
Population-average odds ratios: Nemo {f2(ors.loc[N,'or'],1)} [{f2(ors.loc[N,'or_low'],1)}, {f2(ors.loc[N,'or_high'],1)}], Small {f2(ors.loc[S,'or'],1)} [{f2(ors.loc[S,'or_low'],1)}, {f2(ors.loc[S,'or_high'],1)}], Llama {f2(ors.loc[L,'or'],1)} [{f2(ors.loc[L,'or_low'],1)}, {f2(ors.loc[L,'or_high'],1)}]. Gemma, Qwen and Claude are not given here: with so few events the 0.5 correction would set the number, not the data.

**What this means**

- **Nemo really does produce more false answers than every other model**, by {pts(pw.loc[NSm,'rd_diff'],False)} to {pts(pw.loc['mistral-nemo minus claude-sonnet','rd_diff'],False)} points. All five contrasts survive Holm.
- **Nemo differs from Llama on every scale.** Small vs Llama is clear on odds in all three Bayesian versions. In points its interval excludes zero, but it does not survive Holm.
- **Whether Nemo's *underlying* pull exceeds Small's is unresolved.** In points the gap is clear. Relative to each model's low baseline, GEE sees no difference, and the Bayesian estimate is positive but its interval includes zero in two of three versions.
- **Why the scales disagree.** Small starts at {pts(rates.loc[S,'no_belief'],False)}% and Nemo at {pts(R['nemo_rates']['no_belief'],False)}%, so a similar multiplicative pull gives very different point rises. For harm, points are the relevant scale: they count wrong answers.
- **Differences among Llama, Gemma, Qwen and Claude cannot be separated.** No contrast survives, and their log-odds effects are mostly prior.
- **Llama responds differently to the two channels (exploratory).** How much more a stated belief moves a model than a stored one differs between Llama and Nemo ({est(chan.iloc[0])} points, uncorrected p = {pv(chan.iloc[0].p_item)}) and between Llama and Small ({est(chan.iloc[1])}, uncorrected p = {pv(chan.iloc[1].p_item)}). This is better evidence for the README's Llama lead than the single tests in section 2.
- **Scope:** these are six chosen models, so this says nothing about LLMs in general.

## 5. Mechanism: does uncertainty predict susceptibility?

*All after seeing the data. Exploratory.*

### Which models can test this

| Model | Baseline trials with probabilities | Top option above 99% | Usable? |
|---|---|---|---|
| Mistral Nemo | {int(cov.loc[N,'trials_with_probs'])} of 96 | {pts(cov.loc[N,'share_top_prob_over_099'],False)}% | **Yes**: real spread in confidence |
| Mistral Small | {int(cov.loc[S,'trials_with_probs'])} of 96 (after recovery) | {pts(cov.loc[S,'share_top_prob_over_099'],False)}% | **Partly**: little spread, only {int(band(S,'Unsure').pairs)} unsure pairs |
| Gemma 4 | {int(cov.loc[G,'trials_with_probs'])} of 96 | {pts(cov.loc[G,'share_top_prob_over_099'],False)}% | **No**: near-deterministic |
| Qwen3.5-9B | {int(cov.loc[Q,'trials_with_probs'])} of 96 | {pts(cov.loc[Q,'share_top_prob_over_099'],False)}% | **No**: measured *after* it has reasoned, typically for over 1,000 tokens, so it shows a settled answer, not prior uncertainty |
| Llama, Claude | Almost none | n/a | **No**: use baseline accuracy instead |

**Mistral Small recovery.** The harness logged probabilities for {R['ms_recover']['n_logged']} of {R['ms_recover']['n_trials']} trials, requiring the whole response to rebuild from tokens. The first 12 tokens are logged for every trial, so the other {R['ms_recover']['n_recovered']} were recomputed from those. Checks: on the {R['ms_recover']['n_logged']} trials with both, the largest difference is {R['ms_recover']['max_diff_when_both']:.0f}; the recovered letter matches the answer on {pts(R['ms_recover']['letter_match_rate'],False)}% of trials; and the logged head is an exact prefix of the response on {pts(R['ms_recover']['head_prefix_rate'],False)}% of recovered trials. Whether a trial was logged shows no link to condition (p = {pv(R['ms_recover']['chi2_p_condition'])}) or choice (p = {pv(R['ms_recover']['chi2_p_choice'])}). Using logged trials only gives the same direction (shift {pts(R['ms_logged_only']['mean_shift'])} points, ρ = {f2(R['ms_logged_only']['rho'])}) on just {R['ms_logged_only']['pairs']} pairs. Llama's token stream is visibly corrupted, so it was not recovered.

**Measure quality.** On Nemo, re-running identical prompts (rounds 3 and 4) gives r = {f2(R['retest']['p_inc_corr'],3)}, so probabilities are very stable for a fixed prompt. The two option orders agree far less (r = {f2(cov.loc[N,'rep_corr_false_prob'])}), so part of what looks like "confidence" depends on option order, not knowledge. This noise would weaken the correlations below.

### Does uncertainty predict the shift?

| Test | Nemo | Mistral Small | Meaning |
|---|---|---|---|
| Rank correlation, uncertainty vs shift | ρ = {f2(mech.loc[N,'rho_rho'])} [{f2(mech.loc[N,'rho_ci_low'])}, {f2(mech.loc[N,'rho_ci_high'])}] | ρ = {f2(mech.loc[S,'rho_rho'])} [{f2(mech.loc[S,'rho_ci_low'])}, {f2(mech.loc[S,'rho_ci_high'])}] | A real, moderate link |
| Same, uncertainty from one rep and shift from the other | ρ = {f2(mech.loc[N,'rho_crossrep'])} | ρ = {f2(mech.loc[S,'rho_crossrep'])} | Weaker once baseline noise is not shared |
| Same, shift measured against unrelated memory | ρ = {f2(mech.loc[N,'rho_vs_unrelated_baseline'])} | ρ = {f2(mech.loc[S,'rho_vs_unrelated_baseline'])} | Not mainly regression to the mean |
| Can uncertainty predict which answers flip? (AUC: 0.5 = chance) | {f2(mech.loc[N,'auc_uncertainty'])} [{f2(mech.loc[N,'auc_uncertainty_low'])}, {f2(mech.loc[N,'auc_uncertainty_high'])}] | {f2(mech.loc[S,'auc_uncertainty'])} [{f2(mech.loc[S,'auc_uncertainty_low'])}, {f2(mech.loc[S,'auc_uncertainty_high'])}] | Useful for Nemo, strong for Small |

### Does memory *mainly* move answers where the model is unsure?

**Not for Nemo, where it is about half. Unclear for Small, where it depends on the cut-off.** Unsure answers move more each, but there are fewer of them.

| Baseline state | Model | Pairs | Mean shift, points | Flip rate | Flips | Share of total shift |
|---|---|---|---|---|---|---|""")
for m in (N, S):
    for b, nm in [("Confident and correct", "Confident and correct"), ("Unsure", "Unsure (top option under 90%)"), ("Confident and wrong", "Confident and wrong")]:
        r = band(m, b)
        fl = "n/a" if pd.isna(r.flip_rate) else f"{pts(r.flip_rate, False)}%"
        ci = "" if r.pairs < 5 else f" {rng(r.shift_ci_low, r.shift_ci_high)}"
        w(f"| {nm} | {MN[m]} | {int(r.pairs)} | {pts(r.mean_shift)}{ci} | {fl} | {int(r.flips)} of {int(r.at_risk_pairs)} | {pts(r.share_of_total_shift, False)}% |")
a_n, a_s = acc[acc.model == N], acc[acc.model == L]
ag = lambda d, g: d[d.baseline_accuracy_group == g].iloc[0]
w(f"""
- **Nemo:** an answer it held with over 90% confidence, and correctly, still flips {pts(band(N,'Confident and correct').flip_rate,False)}% of the time, against {pts(band(N,'Unsure').flip_rate,False)}% when unsure. {int(band(N,'Confident and correct').flips)} of its {int(mech.loc[N,'flips'])} flips started from confident, correct answers.
- **Mistral Small:** {int(band(S,'Confident and correct').flips)} of {int(mech.loc[S,'flips'])} flips started from answers above 90%, but only {cut[S]['0.99']['flips']} from answers above 99%.
- **The 90% line was chosen after seeing the data, and it matters.** Moving it from 80% to 99%, the confident-and-correct share of Nemo's shift goes from {pts(cut[N]['0.8']['share_of_shift'],False)}% to {pts(cut[N]['0.99']['share_of_shift'],False)}%, so "about half" is stable. Small's goes from {pts(cut[S]['0.8']['share_of_shift'],False)}% to {pts(cut[S]['0.99']['share_of_shift'],False)}%, so its {pts(band(S,'Confident and correct').share_of_total_shift,False)}% figure is not robust and should not be quoted alone.
- **Relative uncertainty does matter for Small.** Answers that flipped had a median top probability of {100*cut[S]['median_top_prob_flipped']:.1f}%, vs {100*cut[S]['median_top_prob_not_flipped']:.2f}% for those that did not. So its flips cluster at 90–99% rather than at 99.9% and above, which is why its AUC is high. Nemo: {100*cut[N]['median_top_prob_flipped']:.1f}% vs {100*cut[N]['median_top_prob_not_flipped']:.2f}%.
- **Movement tends to be all-or-nothing.** In Nemo, {pts(near0,False)}% of pairs moved under 5 points and {pts(big,False)}% rose more than 50; only {pts(mid,False)}% fell between. Memory seems to capture an item or not, rather than nudging all of them equally.
- **A simple sigmoid predicts more of a gradient than we see.** Adding one fixed log-odds boost to the false option on every item predicts {pts(nl(N,'Confident and correct').predicted_constant_boost)} points for confident items and {pts(nl(N,'Unsure').predicted_constant_boost)} for unsure ones. Nemo actually shows {pts(nl(N,'Confident and correct').observed)} and {pts(nl(N,'Unsure').observed)}. So there is no sign of extra sensitivity to uncertainty beyond what a sigmoid gives anyway; the log-odds shift is flat against uncertainty (ρ = {f2(mech.loc[N,'logit_shift_vs_unc_rho'])}).

### Baseline accuracy (includes Llama)

Items are grouped by whether the model was right twice, once or never at baseline. The effect is measured against the unrelated-memory arm, so different trials define the groups and the effect.

| Model | Right both times | Right once | Wrong both times |
|---|---|---|---|
| Mistral Nemo | {pts(ag(a_n,'right both times').effect_vs_unrelated)} [{pts(ag(a_n,'right both times').ci_low)}, {pts(ag(a_n,'right both times').ci_high)}], {int(ag(a_n,'right both times')['items'])} items | {pts(ag(a_n,'right once').effect_vs_unrelated)} [{pts(ag(a_n,'right once').ci_low)}, {pts(ag(a_n,'right once').ci_high)}], {int(ag(a_n,'right once')['items'])} items | {pts(ag(a_n,'wrong both times').effect_vs_unrelated)} [{pts(ag(a_n,'wrong both times').ci_low)}, {pts(ag(a_n,'wrong both times').ci_high)}], {int(ag(a_n,'wrong both times')['items'])} items |
| Llama 3.1 8B | {pts(ag(a_s,'right both times').effect_vs_unrelated)} [{pts(ag(a_s,'right both times').ci_low)}, {pts(ag(a_s,'right both times').ci_high)}], {int(ag(a_s,'right both times')['items'])} items | {pts(ag(a_s,'right once').effect_vs_unrelated)} [{pts(ag(a_s,'right once').ci_low)}, {pts(ag(a_s,'right once').ci_high)}], {int(ag(a_s,'right once')['items'])} items | {pts(ag(a_s,'wrong both times').effect_vs_unrelated)} [{pts(ag(a_s,'wrong both times').ci_low)}, {pts(ag(a_s,'wrong both times').ci_high)}], {int(ag(a_s,'wrong both times')['items'])} items |

- **Nemo moves about as much on items it reliably knows** as on ones it does not.
- **Llama is the key counterexample.** Its baseline accuracy ({pts(ml.loc[L,'baseline_correct'],False)}%) nearly equals Nemo's ({pts(ml.loc[N,'baseline_correct'],False)}%) and both have 10 items they get right only once, yet stored belief has no detectable effect, though the interval on those 10 items is wide. Low accuracy alone is therefore not enough. Note that accuracy is only a stand-in here: Llama's probabilities are unusable, so its uncertainty was not measured.
- **Between models there is no ordering by accuracy:** {pts(ml.loc[L,'baseline_correct'],False)}% → {pts(ml.loc[L,'stored_effect'])}, {pts(ml.loc[N,'baseline_correct'],False)}% → {pts(ml.loc[N,'stored_effect'])}, {pts(ml.loc[S,'baseline_correct'],False)}% → {pts(ml.loc[S,'stored_effect'])} points.

### Llama reads its memory

The README suggests Llama "may largely ignore the memory section" and lists this as a to-do. The logs say otherwise.

- **It uses stored preferences:** right on {R['llama_preference']['right']} of {R['llama_preference']['trials']} vegetarian and metric checks, and {R['llama_preference']['cites_memory']} of those replies name the preference, for example "Since you prefer metric units".
- **It sometimes names the stored belief and keeps its own answer.** A text search finds it in {pts(ment.loc[L,'stored_false_mentions'],False)}% of stored-belief replies ({int(ment.loc[L,'stored_false_mention_trials'])} trials), and it chose the false option in {int(ment.loc[L,'false_chosen_when_mentioned'])} of those. The same search finds nothing in its no-belief replies.
- **So the better description is "reads the belief but does not adopt it", while it does follow the same belief when the user says it.** Why stored and stated differ for Llama is still open. The search is rough, so treat the percentages as approximate.

Replies mentioning the stored belief, other models: Nemo {pts(ment.loc[N,'stored_false_mentions'],False)}%, Mistral Small {pts(ment.loc[S,'stored_false_mentions'],False)}%, Qwen {pts(ment.loc[Q,'stored_false_mentions'],False)}%, Gemma {pts(ment.loc[G,'stored_false_mentions'],False)}%, Claude {pts(ment.loc[C,'stored_false_mentions'],False)}%.

### Probability shift with the chosen answer unchanged

MS1 predicted shifts without answer changes. **Supported for the two Mistrals, weak for Gemma, negligible for Qwen.** The unrelated memory is the placebo: any change there is noise.

| Model | Pairs unchanged | Mean shift, points | Median, points | Pairs rising | Typical multiple on false-option probability | Placebo: mean shift, pairs rising, multiple |
|---|---|---|---|---|---|---|""")
for m in (N, S, G, Q):
    r, pl = sh(m, "stored false", "chosen answer unchanged"), sh(m, "unrelated", "chosen answer unchanged")
    dd = 3 if m == Q else 1
    w(f"| {MN[m]} | {int(r.pairs)} | {pts(r.mean_shift, True, dd)} {rng(r.ci_low, r.ci_high, True, dd)} | {pts(r.median_shift, True, dd)} | {pts(r.share_up, False)}% | {r.geo_mean_ratio:.1f}× | {pts(pl.mean_shift, True, dd)}, {pts(pl.share_up, False)}%, {pl.geo_mean_ratio:.1f}× |")
gf = R["gemma_first"]
w(f"""
- **Mistrals:** over 90% of unchanged pairs moved toward the false option, and the false-option probability typically multiplied about {sh(N,'stored false','chosen answer unchanged').geo_mean_ratio:.0f}-fold in Nemo and {sh(S,'stored false','chosen answer unchanged').geo_mean_ratio:.0f}-fold in Small, from a very low start. The absolute move is small (medians near zero).
- **Placebo matters here.** Even an unrelated memory nudged this probability up in about {pts(sh(S,'unrelated','chosen answer unchanged').share_up,False)}–{pts(sh(N,'unrelated','chosen answer unchanged').share_up,False)}% of pairs, so "it rose" alone proves little. The size is what separates them: {sh(N,'unrelated','chosen answer unchanged').geo_mean_ratio:.1f}× and {sh(S,'unrelated','chosen answer unchanged').geo_mean_ratio:.1f}× for placebo.
- **Caution:** "answer unchanged" is decided after the memory is shown. Some of Nemo's high-probability trials stayed unchanged by the luck of sampling, which inflates its mean. The median is the safer figure.
- **Gemma:** the mean comes from a few items. Most pairs do not move, and the median is zero.
- **Qwen:** a tiny shift (about {sh(Q,'stored false','chosen answer unchanged').geo_mean_ratio:.1f} times on a near-zero probability), read after reasoning, so little can be concluded.

**A new lead on Gemma.** The harness scores the last "Answer:" line, but probabilities refer to the first. Gemma chose the false option on its first line in {pts(gf['stored_incorrect'],False)}% of stored and {pts(gf['stated_incorrect'],False)}% of stated trials, and in 0% with no belief. It then corrected itself in {R['gemma_corrections']['stored_incorrect']} and {R['gemma_corrections']['stated_incorrect']} of those trials, and never changed answer in the no-belief, unrelated or stored-correct conditions. Reading the replies confirms this is real: one opens by accepting the belief, then says "Wait, I must correct". It rests on {R['gemma_first_effect']['items_up']}–{R['gemma_first_effect_stated']['items_up']} items and is not significant (p = {pv(R['gemma_first_effect']['p_item'])} and {pv(R['gemma_first_effect_stated']['p_item'])}), so it is a lead only. It also shows that scoring only the last answer can hide a model's first response.

## 6. How much does the label remove?

*The label comparison was fixed in advance; the fraction removed was added after seeing the data.*

**Fraction removed** = (stored − label) ÷ (stored − no belief).

| Model | Measure | No belief | Stored | Label | Fraction removed | Still above baseline, points |
|---|---|---|---|---|---|---|""")
for m, x, nm in [(N, "false", "False answers chosen"), (N, "prob", "Probability on false option"), (S, "false", "False answers chosen"), (S, "prob", "Probability on false option")]:
    r = lb(m, x)
    w(f"| {MN[m]} | {nm} | {pts(r.baseline,False)}% | {pts(r.stored,False)}% | {pts(r.labelled,False)}% | **{pts(r.est,False)}%** {rng(r.ci_low,r.ci_high,False)} | {pts(r.residual_above_baseline)} {rng(r.residual_low,r.residual_high)} |")
nf, sf, nc = lb(N, "false"), lb(S, "false"), lb(N, "correct")
pool = lab[lab.model == "both Mistrals pooled"].iloc[0]
il = R["nemo_label_items"]
w(f"""
- **Nemo:** the label removes about {pts(nf.est,False)}% of the effect, plausibly anywhere from about a third to three-quarters. A second method (Fieller) agrees: [{pts(nf.fieller_low,False)}, {pts(nf.fieller_high,False)}]. The probability measure is tighter and gives the same answer.
- **It restores correct answers too:** {pts(nc.est,False)}% {rng(nc.ci_low,nc.ci_high,False)} of Nemo's lost correct answers come back, so answers are not just moving to other wrong options.
- **It is not a fix:** Nemo stays {pts(nf.residual_above_baseline)} points above baseline {rng(nf.residual_low,nf.residual_high)}.
- **Item view:** of the {il['moved_items']} items where stored belief raised Nemo's false answers, the label helped on {il['moved_items_label_helped']}, made no difference on {il['moved_items_label_no_change']}, and never made things worse. {il['moved_items_fully_back']} returned fully to baseline.
- **Mistral Small is uncertain:** {pts(sf.est,False)}% with a very wide interval ({rng(sf.fieller_low,sf.fieller_high,False)} by Fieller). The direct test is {int(get(S,LS).toward)} vs {int(get(S,LS).away)} flips, p = {pv(get(S,LS).p_mcnemar)}, and does not reach significance. Do not claim the label works on Small; say the estimate points that way.
- **Nemo and Small cannot be told apart here:** the gap in fraction removed is [{pts(R['label_diff_mistrals']['low'])}, {pts(R['label_diff_mistrals']['high'])}] points. Both pooled: {pts(pool.est,False)}% {rng(pool.ci_low,pool.ci_high,False)}.
- **Same result on unscreened items:** {pts(R['label_new_items']['est'],False)}% {rng(R['label_new_items']['ci_low'],R['label_new_items']['ci_high'],False)} on the 24 new items, vs {pts(R['label_screened_items']['est'],False)}% on the screened 24.
- **Llama, Gemma, Qwen and Claude have no stored effect to remove**, so the label cannot be assessed on them.

## 7. Why did rounds 1–2 show so little?

*Post hoc. The rounds differ in items, design and reps, so this compares unlike things.*
""")
w("| Model | Round | Items | Baseline correct | Baseline false | Stored false | Effect, points | Share of non-false answers captured |\n|---|---|---|---|---|---|---|---|")
for m in (N, L):
    for nm in ["Round 1", "Round 2 harder items, evidence", "Round 2 harder items, no", "Round 3", "Round 4 main, new", "Round 4 main, all"]:
        r = rr(m, nm)
        if pd.isna(r["items"]):
            w(f"| {MN[m]} | {r['round']} | Not run | | | | | |")
            continue
        w(f"| {MN[m]} | {r['round']} | {int(r['items'])} | {pts(r.baseline_correct,False)}% | {pts(r.baseline_false,False)}% | {pts(r.stored_false,False)}% | {pts(r.effect)} {rng(r.ci_low,r.ci_high)} | {pts(r.conversion,False)}% |")
e_, n_ = rr(N, "Round 2 harder items, evidence"), rr(N, "Round 2 harder items, no")
a4 = rr(N, "Round 4 main, all")
w(f"""
Rounds 2 and 3 share no items. Rounds 1 and 2 share 11; rounds 3 and 4 share 24.

**What the numbers show**

- **Ceiling explains round 1 for Claude and Qwen3.5-397B only.** Llama was at {pts(rr(L,'Round 1').baseline_correct,False)}% correct and did not move. Nemo was not in round 1, so round 1 says nothing about it.
- **Baseline accuracy does not explain Nemo's rounds.** It was *less* accurate in round 2 ({pts(n_.baseline_correct,False)}–{pts(e_.baseline_correct,False)}%) than in the main study ({pts(a4.baseline_correct,False)}%), and *less* sure ({pts(e_.share_unsure,False)}–{pts(n_.share_unsure,False)}% unsure vs {pts(a4.share_unsure,False)}%). On the README's "unsure but not hopeless" reading, round 2 should have offered at least as much room to move. It moved less.
- **The gap is large:** the long-tail effect exceeds round 2's by {pts(d25.loc[N,'difference'])} points {rng(d25.loc[N,'ci_low'],d25.loc[N,'ci_high'])}.
- **It survives a floor correction.** In round 2 the false option already took {pts(n_.baseline_false,False)}–{pts(e_.baseline_false,False)}% of Nemo's answers, leaving less room. But of the remaining answers, memory captured {pts(e_.conversion,False)}–{pts(n_.conversion,False)}%, vs {pts(a4.conversion,False)}% in the main study.
- **At equal confidence, long-tail items still move more.** Confident and correct: {pts(sm('Long','Confident and correct').flip_rate,False)}% flip ({int(sm('Long','Confident and correct').flips)} of {int(sm('Long','Confident and correct').at_risk)}) vs {pts(sm('Round','Confident and correct').flip_rate,False)}% in round 2 ({int(sm('Round','Confident and correct').flips)} of {int(sm('Round','Confident and correct').at_risk)}). Unsure: {pts(sm('Long','Unsure').flip_rate,False)}% ({int(sm('Long','Unsure').flips)} of {int(sm('Long','Unsure').at_risk)}) vs {pts(sm('Round','Unsure').flip_rate,False)}% ({int(sm('Round','Unsure').flips)} of {int(sm('Round','Unsure').at_risk)}). So item type seems to matter beyond uncertainty.
- **Removing evidence is not the reason:** without evidence, round 2 reached only {pts(n_.effect)} points.
- **Round 2 was weak, not null:** intervals reach {pts(e_.ci_high)} and {pts(n_.ci_high)} points, and Nemo's probability shifts were {pts(e_.mean_prob_shift)} {rng(e_.prob_shift_low,e_.prob_shift_high)} and {pts(n_.mean_prob_shift)} {rng(n_.prob_shift_low,n_.prob_shift_high)}.
- **Llama shows no detectable effect in any round**, so its null holds across item types.

**A possible explanation (untested).** Round 2 items are misconceptions and logic or numerical puzzles, the kind of thing training text often discusses and corrects. A long-tail item has no such correction, so a stated "fact" may have less to compete with. Topic familiarity, rather than momentary uncertainty, would then be the moderator. These data cannot show this.

## 8. Selection bias and internal replication

*After seeing the data, but this is the check that matters most for trusting the main result.*

**Where selection entered**

- **Item type:** long-tail items were chosen because Nemo moved on them, after two item sets showed little.
- **Forking paths:** three item sets, two evidence modes and six models were tried before the main run. A search like that can find an effect by chance, which is why the replication below matters.
- **Model:** Nemo is in the main study because it moved.
- **Reuse:** 24 of the 48 main items are the round 3 items.
- **Not item-level cherry-picking:** all {R['n_screened']} round 3 items were kept for the main study, so none was dropped for failing to move.

**The 24 screened items are not fresh evidence.** They used identical prompts and option orders in rounds 3 and 4, so round 4 re-measures them (same answer {pts(R['retest']['same_answer'],False)}% of the time, item effects ρ = {f2(R['r3_r4']['rho_choice'])}). Their effect barely regressed: {pts(R['r3_r4']['effect_r3'])} to {pts(R['r3_r4']['effect_r4_same_items'])} points.

**Internal replication: Nemo on the 24 new items**

| Items | Baseline correct | Baseline false | Effect, points | Items up / down | Item p |
|---|---|---|---|---|---|
| 24 screened | {pts(rp(N)['screened_ref_correct'],False)}% | {pts(rp(N)['screened_ref_rate'],False)}% | {pts(rp(N)['screened_effect'])} {rng(rp(N)['screened_low'],rp(N)['screened_high'])} | {int(rp(N)['screened_items_up'])} / {int(rp(N)['screened_items_down'])} | {pv(rp(N)['screened_p_item'])} |
| 24 new | {pts(rp(N)['new_ref_correct'],False)}% | {pts(rp(N)['new_ref_rate'],False)}% | **{pts(rp(N)['new_effect'])} {rng(rp(N)['new_low'],rp(N)['new_high'])}** | {int(rp(N)['new_items_up'])} / {int(rp(N)['new_items_down'])} | {pv(rp(N)['new_p_item'])} |

- **It replicated.** The unscreened items show the effect alone, no smaller than the screened ones. Difference: {pts(rp(N)['diff'])} points {rng(rp(N)['diff_low'],rp(N)['diff_high'])}, p = {pv(rp(N)['p_perm'])}. Probability shifts agree: {pts(R['nemo_prob_shift']['screened'])} vs {pts(R['nemo_prob_shift']['new'])}.
- **The stated-belief and label effects replicate too** ({pts(rp(N,SN)['new_effect'])} and {pts(rp(N,LS)['new_effect'])} points on new items).
- **The new items are easier for Nemo** ({pts(rp(N)['new_ref_correct'],False)}% vs {pts(rp(N)['screened_ref_correct'],False)}% correct), yet the effect holds. This is a further point against uncertainty as the main driver.
- **What replication does not fix.** The same team wrote the new items, in the same style, after seeing round 3. So this rules out luck among the 24 items, not selection of the item *type*. The defensible claim is "on long-tail facts", not "on factual questions": round 2's items gave {pts(d25.loc[N,'round2_effect'])} points.
- **Mistral Small was never screened**, so all 48 items are out of sample for it, and that protects its result from item-level selection. But it is split: {pts(rp(S)['screened_effect'])} on the first 24 and {pts(rp(S)['new_effect'])} on the new 24 (difference p = {pv(rp(S)['p_perm'])}), with neither half significant alone.

## 9. Robustness

| Check | Result | Meaning |
|---|---|---|
| Drop any one item | Nemo's effect stays {pts(R['nemo_loo']['min'])} to {pts(R['nemo_loo']['max'])} | No single item drives it |
| Concentration | Top 5 items give {pts(R['nemo_top5_share'],False)}% of the effect, top 10 give {pts(R['nemo_top10_share'],False)}% | Broad, as the README says |
| By category | Science {pts(sub.loc['category: science','effect'])}, general {pts(sub.loc['category: general','effect'])}, numerical {pts(sub.loc['category: numerical','effect'])} | Similar across topics |
| Belief direction | Asserts false ({int(sub.loc['belief asserts something false','items'])} items) {pts(sub.loc['belief asserts something false','effect'])}; denies true ({int(sub.loc['belief denies something true','items'])} items) {pts(sub.loc['belief denies something true','effect'])} | Too few denial items to compare |
| Drop the {R['n_convention_items']} item noted as depending on a counting convention | {pts(sub.loc['items without a counting/convention note','effect'])} | Not driven by that item. No item is verified yet |
| Where Nemo's false answers come from | Correct answers fall {pts(abs(dec[(dec.model==N)&(dec.outcome=='correct')].est.iloc[0]),False)} points, other wrong answers {pts(abs(dec[(dec.model==N)&(dec.outcome=='other wrong')].est.iloc[0]),False)} | Mostly right answers turning wrong, which is the harmful case |
| Qwen's 7 unreadable stored/no-belief answers, worst case both ways | Effect between {pts(R['qwen_bounds']['all unreadable stored=not false, base=false'])} and {pts(R['qwen_bounds']['all unreadable stored=false, base=not false'])} | Dropping them cannot hide a large effect |
| Same items moved in both Mistrals? | {R['item_overlap']['both']} of Small's {R['item_overlap']['small_up']} items also moved in Nemo (p = {pv(R['item_overlap']['fisher_p'])}) | No shown overlap; what makes an item movable may be model-specific |

## 10. Figures

All in `report/figures/`. Colours pass an all-pairs colour-vision check, and each model also has its own marker shape.

- **Figure 1, `fig1_effects_by_model.png`.** Effect of each condition on the false-option rate, by model, with 95% item-level intervals. Filled markers pass Holm across all 42 tests by item. *Only Nemo's stored-belief and label effects (panels a, b) are filled; its stated-vs-no-belief effect also passes but is not one of these panels.*
- **Figure 2, `fig2_uncertainty_vs_shift.png`.** Each point is one item and rep. Across: baseline confidence. Up: change in probability on the false option. The dashed line marks 90%. *Exploratory.* Over half of the flips sit left of the line. Shares in the panels depend on that 90% line: at 99% they are {pts(cut[N]['0.99']['share_of_shift'],False)}% for Nemo and {pts(cut[S]['0.99']['share_of_shift'],False)}% for Small. The left side also holds a few confident-but-wrong pairs, which the panel text does not count.
- **Figure 3, `fig3_label_effect.png`.** (a) False-option rates with and without the label. (b) Share of the effect removed. Intervals are item-level; panels share no axis.
- **Figure 4, `fig4_rounds_and_replication.png`.** (a) *Post hoc:* baseline accuracy against effect for each independent item set; R2 labels share items, and one Llama point is nudged 0.6 across so it stays visible. (b) Effect on screened vs new items. Mistral Small was not in round 3, so "screened" is only a label for it.

## 11. Limits and the next test

**Limits of this analysis**

- **Items are unverified drafts**, and nothing is hand-scored. Wrong answer keys would change these numbers.
- **Intervals generalise to items like these**, written by this team, not to all factual questions, and not to all LLMs.
- **Probabilities describe the first answer line** and are not the same as sampling at temperature 0.7.
- **Sections 5, 7 and 8 were designed after seeing the data.** Their p-values are descriptive.
- **Reps add little.** Evidence is limited by the number of items, so the README's plan to "add repetitions" for Small and Llama would not help much. **More items would.** At Small's current rate, about {int(np.ceil(R['min_items_to_pass_holm'] / (ssb.items_up / 48)))} items would be needed before it could pass the Holm test by item.

**Most informative next test.** Pre-register a fresh item set that crosses item type (long-tail vs misconception) with baseline confidence, on Nemo, Small and Llama. That tests the post hoc story in section 7 directly. Separately, replace the README's to-do on why Llama "ignores" memory with the real question: why does it use stored preferences and follow stated beliefs, yet not adopt stored beliefs? Comparing Llama's replies on the same items across those conditions is a cheap start.

## Suggested wording for the report

- "A stored false belief raised Mistral Nemo's false answers by {pts(nsb.est,False)} points ({pts(nsb.ci_low,False)}–{pts(nsb.ci_high,False)}, item-level 95% CI), and the effect replicated on 24 items not used in screening ({pts(rp(N)['new_effect'],False)} points)."
- "Mistral Small showed a smaller rise ({pts(ssb.est,False)} points, {pts(ssb.ci_low,False)}–{pts(ssb.ci_high,False)}), which did not survive correction when items, not trials, were the unit of analysis."
- "Llama, Gemma, Qwen and Claude showed no detectable effect on chosen answers."
- "An 'unverified' label removed about {pts(nf.est,False)}% of Nemo's effect ({pts(nf.ci_low,False)}–{pts(nf.ci_high,False)}), leaving it {pts(nf.residual_above_baseline,False)} points above baseline."
- "In exploratory analyses, uncertainty was only a partial explanation: about half of Nemo's shift came from answers it held confidently and correctly, and Llama, equally inaccurate, did not move."
""")
(OUT / "stats_results.md").write_text("\n".join(o), encoding="utf-8")
print("written", sum(len(x) for x in o))
