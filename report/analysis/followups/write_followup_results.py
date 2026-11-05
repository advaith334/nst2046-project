"""Writes followup_results.md from the tables, so every number in it traces to a CSV."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
TABLES = HERE / "tables"
RES = json.loads((HERE / "results.json").read_text())
NEMO, SMALL, LLAMA, GEMMA, QWEN = "mistral-nemo", "mistral-small", "llama-8b", "gemma-moe", "qwen-small"
NAME = {NEMO: "Mistral Nemo", SMALL: "Mistral Small", LLAMA: "Llama 3.1 8B", GEMMA: "Gemma 4", QWEN: "Qwen3.5-9B"}


def T(n):
    return pd.read_csv(TABLES / f"{n}.csv")


def pt(v, d=0):
    r = round(100 * v, d)
    if r == 0:
        return "0"
    s = f"{abs(r):.{d}f}"
    return f"+{s}" if r > 0 else f"-{s}"


def ci(lo, hi, d=0):
    return f"[{pt(lo, d)}, {pt(hi, d)}]"


def pc(v, d=0):
    return f"{100 * v:.{d}f}%"


def pv(p):
    if pd.isna(p):
        return "n/a"
    if p < 0.0001:
        return "<0.0001"
    return f"{p:.2g}" if p < 0.01 else f"{p:.2f}"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


q1 = T("q1_dose_response")
q1a = q1[q1["items"] == "all 48"].set_index(["model", "evidence"])
c1 = T("q1_contrasts")
c1a = c1[c1["items"] == "all 48"].set_index(["model", "measure", "contrast"])
st = T("q1_weak_passage_strength").set_index(["items", "model"])
sa = T("q1_strong_all_models").set_index("model")
noise = T("q2_noise").set_index("model")
w = T("q2_wrappers_vs_base").set_index(["variant", "model", "arm"])
lw = T("q2_label_within_wording").set_index(["variant", "model"])
tr = T("q3_tradeoff").set_index(["variant", "model"])
fb = T("q3_frame_baselines").set_index(["frame", "model"])
us = T("q3_useful_checks")
gd = T("q3_gate_decisions")
af = T("q3_answer_first_draft").set_index(["model", "condition"])
sp = T("q3_tutor_sum_of_parts").set_index(["model", "reference"])
sb = T("q3_tutor_sum_of_parts_benefit").set_index("model")
q4 = T("q4_wrong_source").set_index("model")
q5 = T("q5_label_on_true").set_index("model")
r6 = T("q6_rates").set_index(["arm", "condition"])
e6 = T("q6_effects").set_index(["arm", "comparison"])
f6 = T("q6_label_fraction").set_index(["arm", "measure"])
b6 = T("q6_base_vs_instruct").set_index(["base_minus", "comparison", "measure"])
d6 = T("q6_arm_differences").set_index(["comparison", "condition"])
rep = T("q6_reproduction").set_index("condition")
lc = T("q6_logodds_clip")
pk = T("q6_peakedness").set_index("arm")
r7 = T("q7_rates").set_index(["model", "condition"])
p7 = T("q7_paired").set_index(["model", "comparison"])
l7 = T("q7_label_fraction").set_index("model")
c7 = T("q7_model_contrasts").set_index(["memory", "pair"])
o7 = T("q7_equal_effects").set_index(["memory", "models"])
m7 = T("q7_mcq_vs_bench").set_index("model")
pub = T("q7_published_llama").set_index("measure")
trunc = T("q7_truncation")
cross = T("q7_judge_crosstab").set_index(["correct", "endorsed"]).n
sp8 = T("q8_spend")
A = RES["audit"]
Q8 = RES["q8"]

# Guards: the prose below depends on these holding. If a rebuild changes them, stop and rewrite.
BI = "nemo-instruct-local"
assert b6.loc[(BI, "memory effect", "answers"), "ci_low"] < 0 < b6.loc[(BI, "memory effect", "answers"), "ci_high"]
assert b6.loc[(BI, "memory effect", "probabilities"), "ci_low"] < 0 < b6.loc[(BI, "memory effect", "probabilities"), "ci_high"]
assert q4.loc[NEMO, "change_low"] < 0 < q4.loc[NEMO, "change_high"] and q4.loc[SMALL, "change_low"] < 0 < q4.loc[SMALL, "change_high"]
assert sp.loc[(NEMO, "main run only"), "int_low"] < 0 < sp.loc[(NEMO, "main run only"), "int_high"]
assert sp.loc[(NEMO, "mean of 5 identical runs"), "int_low"] < 0 < sp.loc[(NEMO, "mean of 5 identical runs"), "int_high"]
assert sb.loc[NEMO, "int_high"] < 0 and sb.loc[NEMO, "lo_low"] < 0 < sb.loc[NEMO, "lo_high"]
assert noise.loc[NEMO, "p_sd_as_large"] > 0.05

L = []
add = L.append


def eff(m, lev):
    r = q1a.loc[(m, lev)]
    return f"{pt(r.effect)} {ci(r.effect_low, r.effect_high)}"


add(f"""# Follow-up results: evidence, wording, fixes, base model and benchmark

Statistics for the runs of 5 Nov 2026. No API calls were made, no run log was changed, and nothing in `src/`, `data/`, `config/`, `runs/` or the README was edited.

**Rebuild everything:** `bash report/analysis/followups/run_followups.sh` (under a minute). Every number here comes from `tables/`.

**All of this is post hoc.** None of these comparisons was pre-registered, and every run was designed after the main results were seen. Treat p-values as descriptive, including the Holm-adjusted ones. Holm only corrects within the family named beside it.

**How to read the numbers**

- "Points" means percentage points of answers. Square brackets are 95% intervals from an item bootstrap: 20,000 resamples of the items, BCa method, as in `stats_results.md`.
- Paired tests match on item and rep. Two p-values are given where it matters: exact McNemar on trials, and exact sign-flip on items. The item version is the honest one for claims about "items like these".
- **Comparisons that cross runs are marked.** On byte-identical prompts, whether Nemo picks the false option differs between runs on about {100 - 100 * noise.loc[NEMO, "trial_agreement_between_replicates"]:.0f}% of trials, so section 2 measures that noise and uses it as a bar.

## Summary

| Question | Answer | Key numbers | Strength |
|---|---|---|---|
| Does evidence shrink the memory effect? | **Yes, steeply, in Nemo** | None {eff(NEMO, "none")}, weak {eff(NEMO, "weak")}, stating {eff(NEMO, "strong")} points | Strong for Nemo; Small falls too but none vs weak is unresolved |
| How strong are the "weak" passages? | **Stronger than the name suggests** | Nemo no-memory accuracy {pc(st.loc[("all 48", NEMO), "acc_none"])} to {pc(st.loc[("all 48", NEMO), "acc_weak"])}, but its false answers fell from {pc(st.loc[("all 48", NEMO), "false_none"])} to {pc(st.loc[("all 48", NEMO), "false_weak"])} | Clear |
| Does wrapper wording matter? | **Yes, more than most fixes** | Nemo's stored rate runs from {pc(w.loc[("notes", NEMO, "stored"), "variant_rate"])} to {pc(w.loc[("bare_fact", NEMO, "stored"), "variant_rate"])} across wordings. Five identical runs span only {pc(noise.loc[NEMO, "rate_main-20261027"])}-{pc(noise.loc[NEMO, "rate_label_source"])} | Strong for the large shifts |
| Do any fixes remove harm and keep benefit? | **Not shown for Nemo** | Tutor: {pt(tr.loc[("tutor", NEMO), "si_change"])} false answers, but {pt(tr.loc[("tutor", NEMO), "sc_change"])} accuracy on true memory. No fix beats a proportional trade-off with an interval above zero | Good for the big moves; cross-run |
| Is the tutor frame more than its parts? | **Not on false answers. On lost benefit, in points only** | False answers: gap {pt(sp.loc[(NEMO, "main run only"), "interaction"])} {ci(sp.loc[(NEMO, "main run only"), "int_low"], sp.loc[(NEMO, "main run only"), "int_high"])}. Accuracy: {pt(sb.loc[NEMO, "interaction"])} {ci(sb.loc[NEMO, "int_low"], sb.loc[NEMO, "int_high"])}, not clear on log-odds | Exploratory, cross-run |
| Does a true memory resist a false passage? | **No detectable change** | Nemo {pc(q4.loc[NEMO, "passage_only_follow"])} to {pc(q4.loc[NEMO, "passage_plus_truth_follow"])}, Small {pc(q4.loc[SMALL, "passage_only_follow"])} to {pc(q4.loc[SMALL, "passage_plus_truth_follow"])} | Good for "no large protection" |
| Does the label hurt true memories? | **Yes in Nemo; no sign elsewhere** | Nemo {pt(q5.loc[NEMO, "label_change"])} {ci(q5.loc[NEMO, "lc_low"], q5.loc[NEMO, "lc_high"])}. Llama's rise cannot be separated from its host change | Moderate |
| Is the effect smaller in the base model? | **No: equal in points** | Base {pt(e6.loc[("nemo-base-local", "memory effect"), "ans_est"])}, instruct {pt(e6.loc[(BI, "memory effect"), "ans_est"])} on the same prompt, gap {pt(b6.loc[(BI, "memory effect", "answers"), "est"])} {ci(b6.loc[(BI, "memory effect", "answers"), "ci_low"], b6.loc[(BI, "memory effect", "answers"), "ci_high"])} | One pair only |
| Does the label work in base? | **Weakly** | Removes {pc(f6.loc[("nemo-base-local", "answers"), "fraction_removed"])} on answers, {pc(f6.loc[("nemo-base-local", "probabilities"), "fraction_removed"])} on probabilities, vs {pc(f6.loc[(BI, "answers"), "fraction_removed"])} and {pc(f6.loc[(BI, "probabilities"), "fraction_removed"])} | Exploratory |
| Is hosted Nemo reproduced locally? | **Yes** | All six rates within {max(abs(rep.local_minus_hosted_first)) * 100:.0f} points; item probabilities correlate {rep.item_r_probs.min():.2f}-{rep.item_r_probs.max():.2f} | Good |
| Are some models unaffected? | **Only in our multiple-choice setup** | MemSyco snippet effects: {", ".join(f"{k} {pt(m7.loc[m, 'bench_snippet'])}" for k, m in [("Nemo", NEMO), ("Small", SMALL), ("Llama", LLAMA), ("Gemma", GEMMA), ("Qwen", QWEN)])} points | Strong that the claim must narrow |
| Spend | **${Q8["total"]:.2f} in total** | ${Q8["by_group"]["5 Nov follow-ups"]:.2f} on 5 Nov; local runs free | Exact |

## What differs from the brief

| Brief or log says | Data says | Why it matters |
|---|---|---|
| 21 and 17 local answers are unparseable | All 38 are clear answers written with a comma, such as " C, Silicon". The harness pattern does not accept a comma | They are not random: {int(T("q6_unparseable").query("model == 'nemo-base-local' and condition == 'stated_incorrect'").unparseable.iloc[0])} of base's 21 are in the stated arm. Reading them changes no conclusion (section 6) |
| Llama moved to DeepInfra/Cloudflare | In label-correct all 96 trials were on **Cloudflare**. DeepInfra served only 14 of 384 evidence trials and {RES["q7"]["llama_hosts"].get("DeepInfra")} of 400 benchmark trials | The host caveat in section 5 is really Novita vs Cloudflare |
| `fixes-20261105/wrappers.md` shows useful-memory rates of 0.00 for the gate | That column is the false-option rate, which these checks do not have. Scored for correctness, gated Nemo got {int(us.query("run.str.contains('memory_gate') and model == @NEMO").right.sum())} of 16, against 16 of 16 in the main run | Nemo recommended salmon to a vegetarian after the gate withheld that memory (section 3) |
| Weak passages are a middle ground | On accuracy, roughly. On the false option, they already remove it for Nemo: {pc(st.loc[("all 48", NEMO), "false_none"])} to {pc(st.loc[("all 48", NEMO), "false_weak"])} | Many passages argue against the false option as well as leaning to the answer |
| Arithmetic items are "hard to weaken" | The 8 numerical items are where Nemo moves **most** under weak passages | Dropping them lowers the weak effect, the opposite of what that label predicts (section 1) |
| `role_only` compares cleanly with the main run | Its system prompt changes, so the main no-belief arm is not a true baseline, and no baseline was run | Its benefit figure leans on an assumption (section 3) |

**Checks that passed.** {A["trials_rescored"]:,} trials were re-scored independently, with {A["score_mismatches"]} disagreements with the logs. Option order matched the main run on every shared item and rep ({A["option_order_mismatches"]} mismatches). The stored-belief prompts in the five replicate runs are byte-identical to the main run. Every 5 Nov run logged a dirty git tree, so these logged requests, not the commit hash, are the record of what was sent.
""")

# ---- Section 1
rows = []
for m in [NEMO, SMALL]:
    for lev, nm in [("none", "No passage"), ("weak", "Weak"), ("strong", "Stating")]:
        r = q1a.loc[(m, lev)]
        rows.append([NAME[m], nm, pc(r.nb_accuracy), pc(r.nb_false), pc(r.si_false), pc(r.lb_false), f"{pt(r.effect)} {ci(r.effect_low, r.effect_high)}", f"{r.effect_toward:.0f} / {r.effect_away:.0f}", f"{pv(r.effect_holm_trial)} / {pv(r.effect_holm_item)}",
                     f"{pt(r.label_change)} {ci(r.label_low, r.label_high)}", f"{r.label_toward:.0f} / {r.label_away:.0f}", f"{pv(r.label_holm_trial)} / {pv(r.label_holm_item)}",
                     "n/a" if pd.isna(r.fraction_removed) else f"{pc(r.fraction_removed)} [{100 * r.fraction_low:.0f}, {100 * r.fraction_high:.0f}]"])
sens = []
for s, lab in [("all 48", "All 48"), ("drop lt_most_islands", "Drop `lt_most_islands`"), ("drop 8 numerical", "Drop 8 numerical"), ("drop islands + numerical", "Drop both (39 items)"), ("only 8 numerical", "Only the 8 numerical")]:
    g = q1[q1["items"] == s].set_index(["model", "evidence"])
    row = [lab]
    for m in [NEMO, SMALL]:
        for lev in ["none", "weak"]:
            r = g.loc[(m, lev)]
            row.append(f"{pt(r.effect)} {ci(r.effect_low, r.effect_high)}")
    row.append(pc(g.loc[(NEMO, "weak"), "nb_accuracy"]))
    sens.append(row)
c = lambda m, me, co: c1a.loc[(m, me, co)]  # noqa: E731
add(f"""## 1. Dose-response: does evidence shrink the memory effect?

*Post hoc. Each row's effect is within one run. Comparing levels crosses runs: "no passage" is the main run of 27 Oct, the others are 5 Nov.*

Figure: `report/figures/fig5_dose_response.png`.

{table(["Model", "Evidence", "Correct, no belief", "False, no belief", "False, stored", "False, labelled", "Memory effect, points", "Flips toward / away", "Holm p, trials / items", "Label change, points", "Flips toward / away", "Holm p, trials / items", "Share removed by label"], rows)}

Holm covers these 12 tests.

**What this means**

- **Nemo shows a clean dose-response.** The effect falls {pt(c(NEMO, "memory effect", "none minus weak").est).lstrip("+")} points {ci(c(NEMO, "memory effect", "none minus weak").ci_low, c(NEMO, "memory effect", "none minus weak").ci_high)} from no passage to weak (item p = {pv(c(NEMO, "memory effect", "none minus weak").item_p)}), then a further {pt(c(NEMO, "memory effect", "weak minus strong").est).lstrip("+")} {ci(c(NEMO, "memory effect", "weak minus strong").ci_low, c(NEMO, "memory effect", "weak minus strong").ci_high)} to a stating passage (p = {pv(c(NEMO, "memory effect", "weak minus strong").item_p)}).
- **A stating passage all but ends it.** Every one of the five models was 100% correct with no belief, and only 1 of Nemo's 96 stored answers flipped. In this design, memory beats what a model half-knows, not what is in front of it.
- **The effect survives weak evidence in Nemo.** It still passes Holm on trials and on items, so a weak passage does not protect it fully.
- **Small falls in the same direction, but less clearly.** The none-to-weak drop is {pt(c(SMALL, "memory effect", "none minus weak").est).lstrip("+")} points {ci(c(SMALL, "memory effect", "none minus weak").ci_low, c(SMALL, "memory effect", "none minus weak").ci_high)}, which cannot be told from zero. Its weak-level effect has an interval above zero but fails Holm (8 flips, from few items).
- **The label removes a similar share at both levels in Nemo:** {pc(q1a.loc[(NEMO, "none"), "fraction_removed"])} and {pc(q1a.loc[(NEMO, "weak"), "fraction_removed"])}, with wide intervals. At the stating level nothing is left to remove.
- **The fall is not a floor effect.** The measure is a rise from baseline, and a baseline near 0% leaves more room to rise, not less.

### How strong are the weak passages?

| Model | Correct: none, weak, stating | Weak minus none, points | Stating minus weak, points | Share of the accuracy gap closed by weak | False, no belief: none, weak | Items always right: none, weak, stating |
|---|---|---|---|---|---|---|
""" + "\n".join(f"| {NAME[m]} | {pc(s.acc_none)}, {pc(s.acc_weak)}, {pc(s.acc_strong)} | {pt(s.weak_gain)} {ci(s.weak_gain_low, s.weak_gain_high)} | {pt(s.strong_minus_weak)} {ci(s.smw_low, s.smw_high)} | {f"{pc(s.share_of_gap_closed)} [{100 * s.share_low:.0f}, {100 * s.share_high:.0f}]" if m == NEMO else "not meaningful: ceiling"} | {pc(s.false_none)}, {pc(s.false_weak, 0)} | {s.items_perfect_none:.0f}, {s.items_perfect_weak:.0f}, {s.items_perfect_strong:.0f} of 48 |" for m in [NEMO, SMALL] for s in [st.loc[("all 48", m)]]) + f"""

- **For Nemo they sit between the two, closer to "none" on accuracy.** They add about {pt(st.loc[("all 48", NEMO), "weak_gain"])} points, closing about {pc(st.loc[("all 48", NEMO), "share_of_gap_closed"])} of the gap, with a wide interval. The gain itself is not significant by item (p = {pv(st.loc[("all 48", NEMO), "weak_gain_p"])}).
- **But they are stronger than accuracy suggests.** Nemo's false option went from {pc(st.loc[("all 48", NEMO), "false_none"])} to {pc(st.loc[("all 48", NEMO), "false_weak"])} with no belief, while other wrong answers rose from {pc(q1a.loc[(NEMO, "none"), "nb_other"])} to {pc(q1a.loc[(NEMO, "weak"), "nb_other"])}. So several passages rule out the false option without pinning down the answer. One example says the "strong, light metal used in jet engines" melts far too low.
- **Small was already at {pc(st.loc[("all 48", SMALL), "acc_none"])}, so its accuracy cannot show passage strength.** Do not quote a strength figure for it.
- **Suggested description:** "passages that lean toward the answer and often against the false option", not simply "weak".

### Sensitivity

Items identified from the data files, not from outcomes. "Numerical" is the item file's own category; those passages hand over a calculation. `lt_most_islands` is the item the audit flagged.

{table(["Items", "Nemo, none", "Nemo, weak", "Small, none", "Small, weak", "Nemo correct, weak"], sens)}

- **Dropping `lt_most_islands` changes nothing that matters.** Small's no-passage effect drops slightly, as the item audit found.
- **Dropping the numerical items cuts Nemo's weak effect about in half.** That is the reverse of what "hard to weaken" predicts: if those passages acted like stating ones, removing them would raise the effect.
- **On those 8 items alone, weak passages do not protect:** accuracy rises, yet Nemo's memory effect stays as high as with no passage. It rests on 8 items, so the interval is very wide. The likely reading is that a passage which needs arithmetic is weak in practice for this model, though these data cannot confirm why.
- **Three science items also rest on sums** (newborn bones, potato chromosomes, sound in seawater). Removing them as well gives the same picture: see `tables/q1_dose_response.csv`.

**Strong passages, all five models** (`tables/q1_strong_all_models.csv`). Stored belief moved nobody except Nemo's single flip. A belief stated by the user moved Nemo {pt(sa.loc[NEMO, "st_effect"])} {ci(sa.loc[NEMO, "st_low"], sa.loc[NEMO, "st_high"])} and Llama {pt(sa.loc[LLAMA, "st_effect"])} {ci(sa.loc[LLAMA, "st_low"], sa.loc[LLAMA, "st_high"])}, small rises that the stored belief did not produce.
""")

# ---- Section 2
n, s_ = noise.loc[NEMO], noise.loc[SMALL]
add(f"""## 2. Wrapper test: what is real, given run-to-run noise?

*Post hoc. All comparisons against `base` are same-day and paired by item and rep.*

### How big is the noise?

`base` repeats the main study's wording. In three label-wording runs the stored arm is also byte-identical, because only the label changed. That gives **five runs of one prompt**, a better noise estimate than base vs main alone.

| Model | Main (27 Oct) | base | label_short | label_source | label_check | Largest gap | Base minus main, stored | Base minus main, labelled |
|---|---|---|---|---|---|---|---|---|
| {NAME[NEMO]} | {pc(n["rate_main-20261027"], 1)} | {pc(n.rate_base, 1)} | {pc(n.rate_label_short, 1)} | {pc(n.rate_label_source, 1)} | {pc(n.rate_label_check, 1)} | {100 * n.gap_obs:.1f} pts | {pt(n.base_minus_main_si)} {ci(n.bm_low, n.bm_high)}, p = {pv(n.bm_mcnemar_p)} | {pt(n.base_minus_main_lb)} {ci(n.lbm_low, n.lbm_high)}, p = {pv(n.lbm_mcnemar_p)} |
| {NAME[SMALL]} | {pc(s_["rate_main-20261027"], 1)} | {pc(s_.rate_base, 1)} | {pc(s_.rate_label_short, 1)} | {pc(s_.rate_label_source, 1)} | {pc(s_.rate_label_check, 1)} | {100 * s_.gap_obs:.1f} pts | {pt(s_.base_minus_main_si)} {ci(s_.bm_low, s_.bm_high)}, p = {pv(s_.bm_mcnemar_p)} | {pt(s_.base_minus_main_lb)} {ci(s_.lbm_low, s_.lbm_high)}, p = {pv(s_.lbm_mcnemar_p)} |

- **The main run replicates.** Base vs main is not significant for either model.
- **The spread looks like ordinary sampling.** Simulating fresh draws from each trial's own pooled probability gives a run SD of {100 * n.sd_run_sim:.1f} points for Nemo; the observed SD is {100 * n.sd_run_obs:.1f} (p = {pv(n.p_sd_as_large)}). Small: {100 * s_.sd_run_sim:.1f} vs {100 * s_.sd_run_obs:.1f} (p = {pv(s_.p_sd_as_large)}). So nothing suggests host drift over the nine days.
- **The main run is the lowest of Nemo's five.** Same-day runs average {pt(n.same_day_minus_main, 1)} points above it {ci(n.sdm_low, n.sdm_high, 1)}. That is within noise, but it means comparisons with the main run slightly understate reductions.
- **Noise band used below: {100 * n.noise_band:.1f} points for Nemo, {100 * s_.noise_band:.1f} for Small.** This is the 95th percentile of the gap between two identical runs, and it equals the largest gap seen. A difference inside it could be a re-run.
""")

words = [("notes", "`Notes:` heading"), ("verified_profile", "`Verified profile facts`"), ("may_be_wrong", "`...may be out of date or wrong`"), ("bare_fact", "Bare fact, no \"User believes\""), ("said_once", "`User once said that...`"), ("label_short", "Label `[Unverified]`"), ("label_source", "Label `[Source: user statement only]`"), ("label_check", "Label `[Check this against your own knowledge...]`")]


def wcell(v, m, arm):
    k = (v, m, arm)
    if k not in w.index:
        return "same prompt as base"
    r = w.loc[k]
    return f"{pc(r.base_rate)} to {pc(r.variant_rate)}: {pt(r.est)} {ci(r.ci_low, r.ci_high)}, **{r.verdict}**"


rows = [[lab] + [wcell(v, m, a) for m in [NEMO, SMALL] for a in ["stored", "labelled"]] for v, lab in words]
rows2 = []
for v, lab in [("base", "Base")] + words:
    a, b = lw.loc[(v, NEMO)], lw.loc[(v, SMALL)]
    rows2.append([lab, f"{pt(a.label_change)} {ci(a.label_low, a.label_high)}, {a.toward:.0f} / {a.away:.0f}", f"{pc(a.fraction_removed)} [{100 * a.fraction_low:.0f}, {100 * a.fraction_high:.0f}]", f"{pt(b.label_change)} {ci(b.label_low, b.label_high)}, {b.toward:.0f} / {b.away:.0f}"])
add(f"""### Paired differences against `base`

False-option rate, points. **real** = passes Holm on items across these 26 tests and exceeds the noise band. **real on trials only** = passes Holm on trials and exceeds the band. **suggestive** = interval excludes zero but fails Holm. **within noise** = neither.

{table(["Wording", "Nemo, stored", "Nemo, labelled", "Small, stored", "Small, labelled"], rows)}

**What this means**

- **Wrapper text drives the result, as Dr Filippov warned.** Nemo's stored-belief rate ranges from {pc(w.loc[("notes", NEMO, "stored"), "variant_rate"])} to {pc(w.loc[("bare_fact", NEMO, "stored"), "variant_rate"])} with no change to the belief. Against the main no-belief baseline that is an effect of {pt(lw.loc[("notes", NEMO), "effect_vs_main_nb"])} to {pt(lw.loc[("bare_fact", NEMO), "effect_vs_main_nb"])} points. The headline +41 belongs to one wording.
- **Two wordings halve Nemo's effect:** the plain `Notes:` heading and the "may be out of date or wrong" caveat, with {w.loc[("notes", NEMO, "stored"), "toward"]:.0f} / {w.loc[("notes", NEMO, "stored"), "away"]:.0f} and {w.loc[("may_be_wrong", NEMO, "stored"), "toward"]:.0f} / {w.loc[("may_be_wrong", NEMO, "stored"), "away"]:.0f} flips. Both are real on every test. Neither reaches baseline ({pt(lw.loc[("notes", NEMO), "effect_vs_main_nb"])} and {pt(lw.loc[("may_be_wrong", NEMO), "effect_vs_main_nb"])} points above it, cross-run).
- **Removing "User believes" makes it worse.** The bare-fact wording is real for Small ({pt(w.loc[("bare_fact", SMALL, "stored"), "est"])}) and real on trials for Nemo ({pt(w.loc[("bare_fact", NEMO, "stored"), "est"])}). So "User believes that" is already acting as a partial hedge.
- **`said_once` also raises it,** real on trials for Nemo. This is odd, as "once said" sounds weaker than "believes". It suggests models are not simply weighing how firmly the belief is held.
- **`Verified profile facts` changes nothing detectable.** Claiming verification did not add pull, which is a useful null: Nemo {pt(w.loc[("verified_profile", NEMO, "stored"), "est"])} {ci(w.loc[("verified_profile", NEMO, "stored"), "ci_low"], w.loc[("verified_profile", NEMO, "stored"), "ci_high"])}.
- **Small mostly stays inside its noise band,** apart from the bare-fact rise. Its effect is small to begin with, so this has limited power.
- **Unknown cost.** The wrapper runs had no true-memory arm, so we do not know what `Notes:` or the caveat do to the benefit of correct memories. Given section 3, that should be tested before recommending either.

### Label wordings

Change from adding the label within each wording, flips toward / away, and share of the effect above baseline removed. The share uses the main run's no-belief arm, so it crosses runs.

{table(["Wording", "Nemo: label change", "Nemo: share removed", "Small: label change"], rows2)}

- **The original label removed the most for Nemo.** Against it, `label_check` leaves {pt(w.loc[("label_check", NEMO, "labelled"), "est"])} points more false answers (**real**) and `label_source` {pt(w.loc[("label_source", NEMO, "labelled"), "est"])} (real on trials). `label_short` is {pt(w.loc[("label_short", NEMO, "labelled"), "est"])} {ci(w.loc[("label_short", NEMO, "labelled"), "ci_low"], w.loc[("label_short", NEMO, "labelled"), "ci_high"])}, just above the band but failing Holm.
- **So a label's words matter.** An instruction to check the claim did worse than a statement that the claim is unverified: {pc(lw.loc[("label_check", NEMO), "fraction_removed"])} of the effect removed against {pc(lw.loc[("base", NEMO), "fraction_removed"])}. Findings about "the label" apply to this wording only.
- **The label stops adding anything once the block is already hedged.** Under `Notes:` and the caveat, it changes Nemo by {pt(lw.loc[("notes", NEMO), "label_change"])} and {pt(lw.loc[("may_be_wrong", NEMO), "label_change"])} points, much less than under base (gap {pt(lw.loc[("notes", NEMO), "label_change_vs_base"])} points for `Notes:`, p = {pv(lw.loc[("notes", NEMO), "lcb_p"])}, uncorrected). The stored and labelled arms converge near 25%. These seem to act on the same thing, so stacking hedges may not help.
- **Small:** no label wording differs from base.
""")

# ---- Section 3
order = ["tutor", "patient", "rule", "answer_first", "memory_gate", "role_only", "heading_only", "student_only", "label"]
show = {"tutor": "Tutor frame", "patient": "Patient frame", "rule": "Rule on memory block", "answer_first": "Answer first", "memory_gate": "Memory gate", "role_only": "Tutor role only", "heading_only": "Student heading only", "student_only": "\"Student believes\" only", "label": "Label (reference)"}
verdict = {"tutor": "Memory switched down both ways", "patient": "Same, with some harm left", "rule": "Harm within noise; some benefit lost", "answer_first": "Little harm removed, much benefit lost", "memory_gate": "Memory off, and fails useful checks",
           "role_only": "Small gain, cheap; no true baseline", "heading_only": "Small gain, cheap", "student_only": "Largest single part, cheap", "label": "Volume knob"}


def useful(v, m):
    run = {"tutor": "fixes-20261105/tutor", "rule": "fixes-20261105/rule", "answer_first": "fixes-20261105/answer_first", "memory_gate": "fixes-20261105/memory_gate"}.get(v)
    if not run:
        return "not run"
    g = us[(us.run == run) & (us.model == m)]
    return f"{g.right.sum():.0f} / {g.n.sum():.0f}"


rows = []
for v in order:
    r = tr.loc[(v, NEMO)]
    rows.append([show[v], f"{pc(r.si_false_main)} to {pc(r.si_false_variant)}", f"{pt(r.si_change)} {ci(r.si_low, r.si_high)}", "n/a" if v == "label" else f"{pv(r.si_holm_trial)} / {pv(r.si_holm_item)}",
                 f"{pc(r.sc_acc_main)} to {pc(r.sc_acc_variant)}", f"{pt(r.sc_change)} {ci(r.sc_low, r.sc_high)}", "n/a" if v == "label" else f"{pv(r.sc_holm_trial)} / {pv(r.sc_holm_item)}",
                 f"{pc(r.harm_share)}", f"{pc(r.benefit_share)}", f"{pt(r.selectivity)} {ci(r.sel_low, r.sel_high)}", useful(v, NEMO), verdict[v]])
rows_s = []
for v in order:
    r = tr.loc[(v, SMALL)]
    rows_s.append([show[v], f"{pc(r.si_false_main)} to {pc(r.si_false_variant)}", f"{pt(r.si_change)} {ci(r.si_low, r.si_high)}", "n/a" if v == "label" else f"{pv(r.si_holm_trial)} / {pv(r.si_holm_item)}",
                   f"{pc(r.sc_acc_main)} to {pc(r.sc_acc_variant)}", f"{pt(r.sc_change)} {ci(r.sc_low, r.sc_high)}", "n/a" if v == "label" else f"{pv(r.sc_holm_trial)} / {pv(r.sc_holm_item)}", useful(v, SMALL)])
g = gd[gd.kind == "factual"]
gn = gd[(gd.model == NEMO) & (gd.kind != "factual")]
add(f"""## 3. Fixes and frames: the two-sided trade-off

*Post hoc, and **every row compares across separate runs**: the main run is 27 Oct, these are 5 Nov. Item pairing keeps the items matched, but the run gap stays. Differences under about {100 * n.noise_band:.0f} points for Nemo or {100 * s_.noise_band:.0f} for Small could be noise.*

Figure: `report/figures/fig6_fix_tradeoff.png`. Across: points cut from the false-memory effect. Up: accuracy gain from a true memory over no memory. The dashed line joins "no fix" and "memory off". A fix on that line loses the same share of benefit as of harm.

**Nemo.** Main: stored false {pc(tr.loc[("tutor", NEMO), "si_false_main"])}, true memory {pc(tr.loc[("tutor", NEMO), "sc_acc_main"])} correct, effect {pt(tr.loc[("tutor", NEMO), "main_effect"])}, benefit {pt(tr.loc[("tutor", NEMO), "main_benefit"])}.

{table(["Variant", "False answers, false memory", "Change, points", "Holm p, trials / items", "Correct, true memory", "Change, points", "Holm p, trials / items", "Harm removed", "Benefit kept", "Selectivity", "Useful checks right", "Verdict"], rows)}

**Selectivity** = share of harm removed + share of benefit kept - 1, in points. Zero means a pure volume knob. Above zero means the fix sorts false memories from true ones. Holm covers the 32 tests on the 8 variants; the label row is for reference only.

**Baselines.** Tutor and patient use their own no-belief arm. Rule, answer first, gate, heading and student use the main arm, whose prompt is identical. Role has no valid baseline.

**Mistral Small.** Its true-memory benefit is only {pt(tr.loc[("tutor", SMALL), "main_benefit"])} points, as it starts at {pc(tr.loc[("tutor", SMALL), "nb_acc_used"] + 0.01 if False else st.loc[("all 48", SMALL), "acc_none"])}. So shares of benefit are not meaningful, and only changes are shown.

{table(["Variant", "False answers, false memory", "Change, points", "Holm p, trials / items", "Correct, true memory", "Change, points", "Holm p, trials / items", "Useful checks right"], rows_s)}

**What this means**

- **No fix is shown to sort false memories from true ones in Nemo.** Selectivity intervals all include zero, except answer first, which is significantly below it. Most points sit close to the dashed line.
- **The tutor frame works by turning memory down, not by judging it.** Inside the frame, false memory moves Nemo {pt(tr.loc[("tutor", NEMO), "effect_in_frame"])} {ci(tr.loc[("tutor", NEMO), "eif_low"], tr.loc[("tutor", NEMO), "eif_high"])} and true memory {pt(tr.loc[("tutor", NEMO), "benefit_kept"])} {ci(tr.loc[("tutor", NEMO), "benefit_low"], tr.loc[("tutor", NEMO), "benefit_high"])}. Both are near zero. The frame's own no-belief answers barely moved ({pc(fb.loc[("tutor", NEMO), "nb_false"])} false). The logged prompts hold the memory and replies cite it ("The student is indeed correct"), so this is not a broken prompt.
- **The patient frame repeats this, a little less cleanly.** Harm is cut, the benefit is gone, and a false-memory effect of {pt(tr.loc[("patient", NEMO), "effect_in_frame"])} {ci(tr.loc[("patient", NEMO), "eif_low"], tr.loc[("patient", NEMO), "eif_high"])} remains. So the result holds beyond tutors, but it is the same trade-off, not a win. The items are still general facts, not medical ones.
- **The memory gate is memory off.** It said FACT and withheld all {int(g.withheld.sum())} of {int(g.n.sum())} stored beliefs in both models, as its prompt instructs. True memories go too. It also withheld {int(gn.withheld.sum())} of {int(gn.n.sum())} of Nemo's useful memories, including the vegetarian one, and Nemo then got {int(gn.right.sum())} of {int(gn.n.sum())} right. A gate that fails the MS1 success test should not be counted as a fix.
- **Answer first is the worst of the group for Nemo.** It costs {pt(tr.loc[("answer_first", NEMO), "sc_change"]).lstrip("-")} points of benefit, and its cut in false answers cannot be told from zero. The drafts show the pattern: {af.loc[(NEMO, "stored_incorrect"), "draft_right_final_false"]:.0f} of {round(96 * af.loc[(NEMO, "stored_incorrect"), "draft_correct"]):.0f} right drafts still flipped to the false belief, while a true memory only lifted accuracy from {pc(af.loc[(NEMO, "stored_correct"), "draft_correct"])} in the draft to {pc(af.loc[(NEMO, "stored_correct"), "final_correct"])}, against {pc(tr.loc[("tutor", NEMO), "sc_acc_main"])} when shown up front. Answering first blocks the benefit more than the harm. It also failed the Pluto correction with the label off. For Small it looks better ({pt(tr.loc[("answer_first", SMALL), "si_change"])}, no accuracy loss), but that fails Holm.
- **The rule did not shift false answers beyond noise.** Nemo {pt(tr.loc[("rule", NEMO), "si_change"])} {ci(tr.loc[("rule", NEMO), "si_low"], tr.loc[("rule", NEMO), "si_high"])}, Small {pt(tr.loc[("rule", SMALL), "si_change"])} {ci(tr.loc[("rule", SMALL), "si_low"], tr.loc[("rule", SMALL), "si_high"])}, if anything the wrong way. Telling a model not to treat memory as evidence, in those words, did not clearly work.
- **The three single parts look cheap.** Each cuts Nemo by {pt(-tr.loc[("heading_only", NEMO), "si_change"]).lstrip("+")}-{pt(-tr.loc[("student_only", NEMO), "si_change"]).lstrip("+")} points against the main run with accuracy still {pc(tr.loc[("student_only", NEMO), "sc_acc_variant"])}-{pc(tr.loc[("role_only", NEMO), "sc_acc_variant"])}. Against the mean of the five identical runs the cuts are {pt(-tr.loc[("heading_only", NEMO), "si_change_vs_pool"]).lstrip("+")}-{pt(-tr.loc[("student_only", NEMO), "si_change_vs_pool"]).lstrip("+")} points, and only "Student believes" passes Holm (p = {pv(tr.loc[("student_only", NEMO), "si_pool_holm"])}). They are the most promising lead, but none passes Holm against the main run itself.
- **The label sits on the line too.** It removes {pc(tr.loc[("label", NEMO), "harm_share"])} of harm and keeps {pc(tr.loc[("label", NEMO), "benefit_share"])} of benefit (section 5).
- **Useful checks are easy.** Only 16 answers per model and variant, and Small's one miss on the metric check under rule, answer first and the gate could be chance. They catch a large failure such as the gate, but they cannot show a fix is safe.

### Is the tutor frame more than the sum of its parts?

**On false answers: no evidence that it is.** The result flips sign depending on the reference, and both intervals span zero.

| Model | Reference | Tutor cut, points | Sum of three parts, points | Gap, points | p | Gap, log-odds |
|---|---|---|---|---|---|---|
""" + "\n".join(f"| {NAME[m]} | {ref} | {pt(x.combined)} {ci(x.combined_low, x.combined_high)} | {pt(x.sum_parts)} {ci(x.sum_low, x.sum_high)} | {pt(x.interaction)} {ci(x.int_low, x.int_high)} | {pv(x.int_p)} | {x.logodds_interaction:+.2f} [{x.lo_low:+.2f}, {x.lo_high:+.2f}] |" for (m, ref), x in sp.iterrows()) + f"""

- **Why the reference matters.** The gap uses the main run twice over, so its noise counts double. The main run is the low one of five, which shrinks each part and inflates the gap. Against the mean of five identical runs, Nemo's gap is {pt(sp.loc[(NEMO, "mean of 5 identical runs"), "interaction"])} points. That is the better estimate.
- **Additive is a fair summary for false answers,** with room for a gap of about ±15 points either way.

**On true-memory accuracy: in points yes, on log-odds no.** Each part costs almost nothing, but together they cost {pt(sb.loc[NEMO, "combined"])} {ci(sb.loc[NEMO, "combined_low"], sb.loc[NEMO, "combined_high"])} against {pt(sb.loc[NEMO, "sum_parts"])} {ci(sb.loc[NEMO, "sum_low"], sb.loc[NEMO, "sum_high"])} summed: a gap of {pt(sb.loc[NEMO, "interaction"])} {ci(sb.loc[NEMO, "int_low"], sb.loc[NEMO, "int_high"])}, p = {pv(sb.loc[NEMO, "int_p"])}. The patient frame shows the same against the tutor parts: {pt(sb.loc[NEMO, "patient_interaction"])} {ci(sb.loc[NEMO, "pint_low"], sb.loc[NEMO, "pint_high"])}, p = {pv(sb.loc[NEMO, "pint_p"])}.

- **A ceiling could explain it.** The main run is at {pc(sb.loc[NEMO, "main_acc"])}, where small pulls barely show in points and then add up fast. On log-odds the gap is {sb.loc[NEMO, "logodds_interaction"]:+.2f} [{sb.loc[NEMO, "lo_low"]:+.2f}, {sb.loc[NEMO, "lo_high"]:+.2f}], which spans zero and is very wide.
- **Reading:** a whole, consistent frame may change how a model treats memory in a way no single phrase does, but these data do not establish that. It is exploratory, crosses runs, and has no replicate of the true-memory arm.
- **Mistral Small** shows no clear gap on either side.
""")

# ---- Section 4
a, b = q4.loc[NEMO], q4.loc[SMALL]
add(f"""## 4. Wrong source: did a true memory change following of the false passage?

*Post hoc. Paired within one run. The passage is deliberately false: "An older reference states that ...". `accepted_incorrect` here means the model followed it.*

| Model | Followed passage, no memory | Followed, true memory | Change, points | Flips toward / away | p, trials / items | Correct, no memory to true memory |
|---|---|---|---|---|---|---|
| {NAME[NEMO]} | {pc(a.passage_only_follow)} {ci(a.po_low, a.po_high).replace("+", "")} | {pc(a.passage_plus_truth_follow)} {ci(a.pt_low, a.pt_high).replace("+", "")} | {pt(a.follow_change)} {ci(a.change_low, a.change_high)} | {a.toward:.0f} / {a.away:.0f} | {pv(a.mcnemar_p)} / {pv(a.item_p)} | {pc(a.acc_passage_only)} to {pc(a.acc_with_truth)} |
| {NAME[SMALL]} | {pc(b.passage_only_follow)} {ci(b.po_low, b.po_high).replace("+", "")} | {pc(b.passage_plus_truth_follow)} {ci(b.pt_low, b.pt_high).replace("+", "")} | {pt(b.follow_change)} {ci(b.change_low, b.change_high)} | {b.toward:.0f} / {b.away:.0f} | {pv(b.mcnemar_p)} / {pv(b.item_p)} | {pc(b.acc_passage_only)} to {pc(b.acc_with_truth)} |

- **No: true memory made no detectable difference in either model.** This is a null, not proof of zero. The intervals rule out protection above about {abs(100 * a.change_low):.0f} points for Nemo and {abs(100 * b.change_low):.0f} for Small.
- **The false passage is powerful.** It lifts Nemo's false answers by {pt(a.passage_rise)} {ci(a.pr_low, a.pr_high)} over no passage (cross-run), though it is framed as an *older* source.
- **The asymmetry is the finding.** On its own, a true memory takes Nemo to {pc(a.main_sc_acc)} correct. Against a false passage, it stays at {pc(a.acc_with_truth)}. With section 1, the passage wins in both directions: a true passage beats a false memory, and a false passage beats a true memory.
- **So what is in front of the model outranks what it remembers,** in this design. That cuts both ways for practice: a corrected source helps, and a stale one is not rescued by the record.
- **Societal note, with care.** The case of a right patient and a wrong record is the one where stored knowledge gave no protection, but these are general facts, not medical items.
""")

# ---- Section 5
rows = []
for m in [NEMO, SMALL, LLAMA, GEMMA, QWEN]:
    r = q5.loc[m]
    rows.append([NAME[m], f"{pc(r.acc_no_belief)}", f"{pc(r.acc_true_memory)}", f"{pc(r.acc_true_labelled)}", f"{pt(r.label_change)} {ci(r.lc_low, r.lc_high)}", f"{r.toward:.0f} / {r.away:.0f}", f"{pv(r.holm_trial_label)} / {pv(r.holm_item_label)}", f"{pt(r.labelled_vs_nb)} {ci(r.ln_low, r.ln_high)}", f"{pc(r.false_true_memory)} to {pc(r.false_true_labelled)}"])
add(f"""## 5. The label on true memories

*Post hoc and **cross-run**: the labelled arm is 5 Nov, the other two are the main run. Holm covers 10 tests.*

{table(["Model", "Correct, no belief", "Correct, true memory", "Correct, true + label", "Label change, points", "Flips up / down", "Holm p, trials / items", "True + label vs no belief, points", "False: true memory to true + label"], rows)}

- **The label has a real cost in Nemo.** It loses {pt(q5.loc[NEMO, "label_change"]).lstrip("-")} points of accuracy on true memories, {q5.loc[NEMO, "away"]:.0f} flips down and none up, surviving Holm on both versions. Nemo keeps about {pc(q5.loc[NEMO, "benefit_kept"])} [{100 * q5.loc[NEMO, "bk_low"]:.0f}, {100 * q5.loc[NEMO, "bk_high"]:.0f}] of its benefit from true memory. The estimate is about twice the {100 * n.noise_band:.0f}-point noise band measured on false answers, but the near end of its interval ({pt(q5.loc[NEMO, "lc_high"])}) is inside that band, so the size is uncertain.
- **So the MS1 success claim needs narrowing.** The useful-memory checks showed no cost because they are too easy. On harder items, the label removes about {pc(tr.loc[("label", NEMO), "harm_share"])} of the harm and about {100 * (1 - q5.loc[NEMO, "benefit_kept"]):.0f}% of the benefit. It acts more like a volume knob than a filter (section 3), and the two shares have wide, overlapping intervals.
- **Mistral Small: no change at all,** zero flips, but it has almost no benefit to lose.
- **Gemma and Qwen: at ceiling,** so the label has nothing to reduce. This is not evidence of no cost.
- **Llama: an apparent gain of {pt(q5.loc[LLAMA, "label_change"])} {ci(q5.loc[LLAMA, "lc_low"], q5.loc[LLAMA, "lc_high"])} that should not be read as a label effect.** It fails Holm, and it is confounded.

**Llama host caveat.** The main run used Novita. All 96 labelled trials ran on Cloudflare, because Novita stopped serving this model. No run has the same prompt on both hosts, so the label and the host cannot be separated. The config lists both as fp8, but a label making a model *more* accurate than unlabelled true memory ({pc(q5.loc[LLAMA, "acc_true_labelled"])} vs {pc(q5.loc[LLAMA, "acc_true_memory"])}) could as easily be a host difference as a label effect. Report the Llama row with this note, or leave it out.
""")

# ---- Section 6
arms = [("nemo-base-local", "Local base, plain text"), (BI, "Local instruct, plain text"), ("nemo-instruct-local-chat", "Local instruct, chat"), ("hosted", "Hosted instruct, main run")]
rows = []
for arm, lab in arms:
    x = e6.loc[(arm, "memory effect")]
    l = e6.loc[(arm, "label vs stored")]
    tm = e6.loc[(arm, "true memory")]
    rows.append([lab, pc(r6.loc[(arm, "no_belief"), "false_rate"]), pc(r6.loc[(arm, "stored_incorrect"), "false_rate"]), pc(r6.loc[(arm, "stored_incorrect_labelled"), "false_rate"]),
                 f"{pt(x.ans_est)} {ci(x.ans_low, x.ans_high)}", f"{x.toward:.0f} / {x.away:.0f}", f"{pt(x.prob_est)} {ci(x.prob_low, x.prob_high)}", f"{x.logodds_est:+.1f}", f"{pt(l.ans_est)} {ci(l.ans_low, l.ans_high)}", f"{pt(l.prob_est)} {ci(l.prob_low, l.prob_high)}", f"{pc(f6.loc[(arm, 'answers'), 'fraction_removed'])}, {pc(f6.loc[(arm, 'probabilities'), 'fraction_removed'])}"])
ba, bp, bl = b6.loc[(BI, "memory effect", "answers")], b6.loc[(BI, "memory effect", "probabilities")], b6.loc[(BI, "memory effect", "log-odds of probability")]
lba, lbp = b6.loc[(BI, "label vs stored", "answers")], b6.loc[(BI, "label vs stored", "probabilities")]
CH = "nemo-instruct-local-chat"
lca, lcp = b6.loc[(CH, "label vs stored", "answers")], b6.loc[(CH, "label vs stored", "probabilities")]
base_nb = e6.loc[("nemo-base-local", "unrelated memory")]
rr = RES["q6_repro_effect"]
add(f"""## 6. Base vs instruct: does instruction tuning cause this?

*Post hoc and exploratory. One pair of models. Base and instruct on the plain-text prompt is the fair comparison, as both see the same transcript ending in "Answer:". The chat arm is instruct in its natural form.*

Figure: `report/figures/fig7_base_vs_instruct.png`.

{table(["Arm", "False, no belief", "False, stored", "False, labelled", "Memory effect, answers", "Flips", "Memory effect, probability", "Same, log-odds", "Label vs stored, answers", "Label vs stored, probability", "Share removed: answers, probability"], rows)}

### Is the effect larger, smaller or equal in base?

| Scale | Base | Instruct, same prompt | Base minus instruct | Item p | Reading |
|---|---|---|---|---|---|
| Answers, points | {pt(ba.base)} | {pt(ba.other)} | {pt(ba.est)} {ci(ba.ci_low, ba.ci_high)} | {pv(ba.item_p)} | Equal, within about ±14 points |
| Token probability, points | {pt(bp.base)} | {pt(bp.other)} | {pt(bp.est)} {ci(bp.ci_low, bp.ci_high)} | {pv(bp.item_p)} | Equal, within about ±11 points |
| Log-odds of that probability | {bl.base:+.1f} | {bl.other:+.1f} | {bl.est:+.1f} [{bl.ci_low:+.1f}, {bl.ci_high:+.1f}] | {pv(bl.item_p)} | Smaller in base |

- **Equal in points, and never larger or smaller by a detectable margin.** That is an interval result, not proof of equality, but gaps above about 14 points are ruled out on answers. Base against chat and hosted instruct gives the same picture: {pt(b6.loc[(CH, "memory effect", "answers"), "est"])} {ci(b6.loc[(CH, "memory effect", "answers"), "ci_low"], b6.loc[(CH, "memory effect", "answers"), "ci_high"])} and {pt(b6.loc[("hosted", "memory effect", "answers"), "est"])} {ci(b6.loc[("hosted", "memory effect", "answers"), "ci_low"], b6.loc[("hosted", "memory effect", "answers"), "ci_high"])}.
- **The log-odds gap mostly reflects how sure each model starts.** Base has a median no-belief probability of {pc(pk.loc["nemo-base-local", "median_answer_prob_no_belief"])} on the right answer, instruct {pc(pk.loc[BI, "median_answer_prob_no_belief"])}, and instruct's false-option probability starts far lower ({pk.loc[BI, "median_false_prob_no_belief"]:.3f} vs {pk.loc["nemo-base-local", "median_false_prob_no_belief"]:.2f}). The same rise in points is then a bigger log-odds move. It also depends on the clip at very small probabilities: the gap goes from {lc.base_minus_instruct.iloc[0]:+.1f} to {lc.base_minus_instruct.iloc[2]:+.1f} as the clip moves from 0.01% to 1%. So it does not show that tuning adds pull.
- **The pattern is the same as in instruct.** In base an unrelated memory does nothing ({pt(base_nb.ans_est)} {ci(base_nb.ans_low, base_nb.ans_high)}) and a true memory removes false answers ({pt(e6.loc[("nemo-base-local", "true memory"), "ans_est"])}). So it is the content that moves it, in both directions.

### Does the label work in base?

**Weakly, and less well than in instruct.**

- **On answers it barely reaches significance.** Base {pt(e6.loc[("nemo-base-local", "label vs stored"), "ans_est"])} {ci(e6.loc[("nemo-base-local", "label vs stored"), "ans_low"], e6.loc[("nemo-base-local", "label vs stored"), "ans_high"])}, {e6.loc[("nemo-base-local", "label vs stored"), "toward"]:.0f} / {e6.loc[("nemo-base-local", "label vs stored"), "away"]:.0f} flips, McNemar p = {pv(e6.loc[("nemo-base-local", "label vs stored"), "mcnemar_p"])}, item p = {pv(e6.loc[("nemo-base-local", "label vs stored"), "item_p"])}.
- **On probabilities the drop is clear but small:** {pt(e6.loc[("nemo-base-local", "label vs stored"), "prob_est"])} {ci(e6.loc[("nemo-base-local", "label vs stored"), "prob_low"], e6.loc[("nemo-base-local", "label vs stored"), "prob_high"])}.
- **The label works better in instruct.** On probabilities the gap against base is {pt(lbp.est)} {ci(lbp.ci_low, lbp.ci_high)} (p = {pv(lbp.item_p)}) on the same prompt, and {pt(lcp.est)} {ci(lcp.ci_low, lcp.ci_high)} (p = {pv(lcp.item_p)}) for chat. On answers: {pt(lba.est)} {ci(lba.ci_low, lba.ci_high)} (p = {pv(lba.item_p)}) and {pt(lca.est)} {ci(lca.ci_low, lca.ci_high)} (p = {pv(lca.item_p)}). None of these is corrected for multiplicity.
- **Reading:** the tendency to follow memory does not need tuning, but responding to a caution label may partly come from it. This is a lead, not a finding.

### Is hosted Nemo reproduced by the local chat arm?

**Yes.** The quantised local model matches the hosted one closely. Hosted is scored on the first answer line here, since local replies stop at 16 tokens; for Nemo this gives the same rates as the final line.

{table(["Condition", "Local chat", "Hosted", "Local minus hosted, points", "Flips", "Holm p, items", "Mean probability: local, hosted", "Item correlation: answers, probabilities"], [[c_, pc(x.local_chat), pc(x.hosted_first_line), f"{pt(x.local_minus_hosted_first)} {ci(x.ci_low, x.ci_high)}", f"{x.toward:.0f} / {x.away:.0f}", pv(x.holm_item), f"{x.p_local:.2f}, {x.p_hosted:.2f}", f"{x.item_r_answers:.2f}, {x.item_r_probs:.2f}"] for c_, x in rep.iterrows()])}

- **No condition differs after Holm.** The largest gap, {pt(rep.loc["stored_incorrect", "local_minus_hosted_first"], 1)} on the stored arm, equals the {100 * n.noise_band:.1f}-point noise band for identical hosted runs.
- **The effect:** local {pt(rr["effect_local"])}, hosted {pt(rr["effect_hosted_first"])}, gap {pt(rr["est"])} {ci(rr["ci_low"], rr["ci_high"])}. Against the mean of the five hosted runs, the stored rate differs by only {pt(RES["q6_repro_vs_pool"]["est"], 1)} points {ci(RES["q6_repro_vs_pool"]["ci_low"], RES["q6_repro_vs_pool"]["ci_high"], 1)}.
- **So quantisation and the move to a local server did not create or remove the effect.** That makes the local pair a fair stand-in for the hosted model.

### What this means for MS1

The MS1 document is not in this repo, so the claim is taken as worded in the brief.

**Stated plainly: this pair does not support the claim that instruction tuning on preference data causes the effect.** The base model, with no instruction tuning, shows the effect at full size, so tuning is not needed to produce it here. The effect appears to come from pre-training, or from how a text model continues a prompt that contains the claim.

What this does **not** show:

- **It does not show tuning plays no part anywhere.** It is one model pair, and other models or other tuning could differ.
- **It does not test preference data as such.** We compare base with instruct. We have no record here of how Nemo Instruct was tuned, so "preference data" is not separately isolated.
- **It does not show the same mechanism in both.** A base model continuing a transcript may simply be primed by text in its context. An instruct model may reach the same answer for social reasons. Equal size does not mean an equal cause.
- **Tuning does seem to change something:** the response to the label, and how sure the model is.

The report should drop or reword the causal claim to: "in one base and instruct pair, instruction tuning was not necessary for the effect."

### Limits

- **One pair**, from one family.
- **Quantised:** both Q4_K_M, from different GGUF builders. Local chat matching hosted reduces this worry for instruct only; base has no hosted comparison.
- **Completion prompt.** Base never sees a chat template. The system text is pasted into a plain transcript ending in "Answer:", which is not how anyone uses a base model. It also forces an immediate letter.
- **Unparseable answers.** 21 in base and 17 in instruct, all comma-style answers the harness pattern does not read. They are uneven across conditions (10 of base's 21 are stated-belief trials). Reading them leaves the base effect at {pt(e6.loc[("nemo-base-local", "memory effect"), "ans_rescued"])} and instruct at {pt(e6.loc[(BI, "memory effect"), "ans_rescued"])}; the gap is {pt(b6.loc[(BI, "memory effect", "answers, comma read"), "est"])} {ci(b6.loc[(BI, "memory effect", "answers, comma read"), "ci_low"], b6.loc[(BI, "memory effect", "answers, comma read"), "ci_high"])}. No conclusion changes. Probabilities use all 576 trials, so they are unaffected.
- **Short replies:** local replies stop at 16 tokens, so a model cannot correct itself as hosted replies can.
- **Probabilities describe the first answer position** and are not the same as sampling at temperature 0.7.
""")

# ---- Section 7
conds = [("no_memory", "No memory"), ("full_dialogue", "Full dialogue"), ("snippet", "Snippet"), ("snippet_labelled", "Snippet + label")]
ms = [NEMO, SMALL, LLAMA, GEMMA, QWEN]
rows = [[NAME[m]] + [f"{pc(r7.loc[(m, c), 'sycophancy'])} [{100 * r7.loc[(m, c), 'low']:.0f}, {100 * r7.loc[(m, c), 'high']:.0f}]" for c, _ in conds] + [" / ".join(f"{100 * r7.loc[(m, c), 'accuracy']:.0f}" for c, _ in conds)] for m in ms]


def pair(m, cc):
    r = p7.loc[(m, cc)]
    return f"{pt(r.est)} {ci(r.ci_low, r.ci_high)}, {r.toward:.0f} / {r.away:.0f}"


rows2 = [[NAME[m], pair(m, "full_dialogue vs no_memory"), pair(m, "snippet vs no_memory"), pair(m, "snippet_labelled vs snippet"), pv(p7.loc[(m, "snippet_labelled vs snippet"), "holm_p"]), f"{pc(l7.loc[m, 'fraction_removed'])} [{100 * l7.loc[m, 'low']:.0f}, {100 * l7.loc[m, 'high']:.0f}]", pair(m, "snippet_labelled vs no_memory")] for m in ms]
rows3 = [[NAME[m], f"{pt(x.mcq_effect)} {ci(x.mcq_low, x.mcq_high)}", f"{pt(x.bench_snippet)} {ci(x.bs_low, x.bs_high)}", f"{pt(x.bench_dialogue)} {ci(x.bd_low, x.bd_high)}"] for m in ms for x in [m7.loc[m]]]


def pubrow(k, lab):
    x = pub.loc[k]
    p_ = f"{100 * x.published_low:.1f}" if x.published_low == x.published_high else f"{100 * x.published_low:.1f}-{100 * x.published_high:.1f}"
    return [lab, p_, f"{100 * x.ours:.0f} [{100 * x.ours_low:.0f}, {100 * x.ours_high:.0f}]", "Yes" if x.published_in_our_ci else "No, just outside"]


sn = o7.loc[("snippet", "without Qwen")]
add(f"""## 7. MemSyco-Bench: an external check

*Post hoc. 100 items sampled by seed from the benchmark's 300 Objective Fact Judgment items; one answer per item, model and condition. Free text, judged by an AI model. `sycophancy` = the judge says the answer endorses the misconception the memory favours. Intervals are item-bootstrap; they agree with the harness's Wilson intervals to within a point.*

### Rates

{table(["Model", "No memory", "Full dialogue", "Snippet", "Snippet + label", "Correct: no memory / dialogue / snippet / label"], rows)}

### Effects

Points, with flips toward / away. Holm is on trials across all 25 tests here.

{table(["Model", "Full dialogue vs none", "Snippet vs none", "Label vs snippet", "Holm p, label", "Share removed by label", "Label vs none"], rows2)}

**What this means**

- **Every model moved, by large amounts.** Memory raised endorsement by {pt(min(p7.loc[(m, "snippet vs no_memory"), "est"] for m in ms))} to {pt(max(p7.loc[(m, "snippet vs no_memory"), "est"] for m in ms))} points with a snippet, and {pt(min(p7.loc[(m, "full_dialogue vs no_memory"), "est"] for m in ms))} to {pt(max(p7.loc[(m, "full_dialogue vs no_memory"), "est"] for m in ms))} with full dialogue. All 10 tests pass Holm.
- **Models barely differ on full dialogue** (equal-effects permutation p = {pv(o7.loc[("full_dialogue", "all five"), "perm_p"])}, spread {o7.loc[("full_dialogue", "all five"), "spread_points"]:.0f} points). No pair survives Holm.
- **Qwen stands out on the snippet:** {pc(r7.loc[(QWEN, "snippet"), "sycophancy"])}, {pt(p7.loc[(QWEN, "snippet vs no_memory"), "est"])} points, with {p7.loc[(QWEN, "snippet vs no_memory"), "toward"]:.0f} flips toward and none away. It exceeds each other model by {pt(-c7.loc[("snippet", "mistral-nemo minus qwen-small"), "est"]).lstrip("+")}-{pt(-c7.loc[("snippet", "llama-8b minus qwen-small"), "est"]).lstrip("+")} points (all Holm p < 0.001). Without Qwen the other four cannot be separated (p = {pv(sn.perm_p)}). Its thinking was off here, which matters (limits below).
- **The snippet moves answers as much as the long dialogue** in Nemo, Small and Gemma, with differences of {pt(p7.loc[(NEMO, "full_dialogue vs snippet"), "est"])}, {pt(p7.loc[(SMALL, "full_dialogue vs snippet"), "est"])} and {pt(p7.loc[(GEMMA, "full_dialogue vs snippet"), "est"])} points, all non-significant. That supports our one-line memory design.
- **The label helps in every model:** {pt(max(p7.loc[(m, "snippet_labelled vs snippet"), "est"] for m in ms))} to {pt(min(p7.loc[(m, "snippet_labelled vs snippet"), "est"] for m in ms))} points, and accuracy rises by {pt(min(p7.loc[(m, "snippet_labelled vs snippet"), "acc_change"] for m in ms))} to {pt(max(p7.loc[(m, "snippet_labelled vs snippet"), "acc_change"] for m in ms))}. Nemo's reduction alone misses Holm (p = {pv(p7.loc[(NEMO, "snippet_labelled vs snippet"), "holm_p"])}, 9 / 22 flips). It is not a full fix: four of five stay above no memory, and only Llama returns near it.
- **Unlike section 5, the label raises accuracy here.** There is no true memory arm, so this benchmark cannot show the label's cost.
- **Baseline is not zero.** With no memory, {pc(r7.loc[(QWEN, "no_memory"), "sycophancy"])}-{pc(r7.loc[(NEMO, "no_memory"), "sycophancy"])} of answers still endorse the misconception, as these items come from TruthfulQA.

### Against the published Llama-3.1-8B figures

Xiang et al. (2026) report these on all 300 items; ours are 100 of the same items, so the two are not independent. Our "snippet" is our own condition; their memory figures come from real memory systems.

{table(["Measure", "Published", "Ours [95% CI]", "Published value inside our interval?"], [pubrow("no memory", "No memory, %"), pubrow("full dialogue", "Full dialogue, %"), pubrow("memory (ours: snippet; theirs: memory systems)", "With memory, %"), pubrow("rise, full dialogue", "Rise, full dialogue, points"), pubrow("rise, memory", "Rise, memory, points")])}

- **Our run agrees with the paper in direction and rough size.** Each rate is compatible with it, though the "with memory" row only just overlaps and compares unlike conditions. The one miss is the full-dialogue rise, ours {pt(pub.loc["rise, full dialogue", "ours"])} vs +20, sitting just outside our interval's edge at {100 * pub.loc["rise, full dialogue", "ours_low"]:.0f}. With one test of five and a subsample, that is not a meaningful disagreement.
- **This supports the harness setup.** It also shows Llama, our "no effect" model, moves about as much here as published.

### How this changes "some models are unaffected"

{table(["Model", "Our multiple choice: stored vs none", "MemSyco: snippet vs none", "MemSyco: dialogue vs none"], rows3)}

- **The claim does not hold as a general one.** Llama, Gemma and Qwen showed about +1 point on our items and {pt(p7.loc[(LLAMA, "snippet vs no_memory"), "est"])}, {pt(p7.loc[(GEMMA, "snippet vs no_memory"), "est"])} and {pt(p7.loc[(QWEN, "snippet vs no_memory"), "est"])} here.
- **Correct wording:** "Llama, Gemma and Qwen showed no detectable effect on our long-tail multiple-choice items. All three showed large effects on free-text misconception items in MemSyco-Bench."
- **The model ranking reverses in part.** Nemo is highest on our items, and Qwen on the snippet here. So susceptibility depends on the task as well as the model.
- **Claude is not covered.** It was not in this run, so nothing here changes its 0%.

### Limits

- **AI judge.** Every score comes from one model, DeepSeek V4 Flash, with no human check. It sees the memory text in every condition, including no memory, and is not told the condition, but it may still be primed to find endorsement. Its output is coherent, with only {cross.loc[(1, 1)]} of 2,000 answers marked both correct and endorsing, but coherent is not the same as right.
- **Preference, not belief.** The memory says the user "prefers the familiar framing", and adds that this does not assert the claim. Our main study stores a belief. These are related constructs, not one measure.
- **Qwen thinking off,** as the benchmark runs it. Our main run had it on, with long reasoning. So Qwen's gap between tasks may be partly thinking, not the task. These data cannot separate the two.
- **Other differences at once:** free text vs multiple choice, temperature 0.2 vs 0.7, misconceptions vs long-tail facts. Any of these could explain the contrast with our items.
- **Truncated replies:** {sum(RES["q7"]["truncated"].values())} hit the 800-token limit ({", ".join(f"{k} {v}" for k, v in RES["q7"]["truncated"].items())}). Dropping them changes nothing (`tables/q7_truncation.csv`).
- **Llama's host:** mostly Cloudflare ({RES["q7"]["llama_hosts"].get("Cloudflare")} of 400).
""")

# ---- Section 8
g = Q8["by_group"]
add(f"""## 8. Spend

*From logged costs, every attempt included, failed ones too.*

| Group | Cost | Trials |
|---|---|---|
| 27 Oct rounds (pilot to main) | ${g["27 Oct rounds"]:.2f} | {sp8[sp8.group == "27 Oct rounds"].trials.sum():,} |
| 5 Nov follow-ups | ${g["5 Nov follow-ups"]:.2f} | {sp8[sp8.group == "5 Nov follow-ups"].trials.sum():,} |
| Smoke tests | ${g["smoke tests"]:.2f} | {sp8[sp8.group == "smoke tests"].trials.sum():,} |
| Local base and instruct | $0.00 | {sp8[sp8.group == "local (free)"].trials.sum():,} |
| **Total** | **${Q8["total"]:.2f}** | **{Q8["all_trials"]:,}** ({Q8["all_attempt_rows"]:,} logged attempts) |

- **MemSyco-Bench was the largest item on 5 Nov:** ${sp8[sp8.run == "memsyco-bench-20261105"].cost_usd.iloc[0]:.3f}.
- **A trap in the logs.** Benchmark rows hold the judge's cost only in the top-level `cost` field. Summing `usage.cost` alone gives ${Q8["usage_field_total"]:.2f}, which is ${Q8["total"] - Q8["usage_field_total"]:.2f} too low.
- **The fix runs are complete.** The gate and answer-first runs add their extra call's cost into the logged usage, so nothing is hidden there.
- **The README's "about $3.60" is the 27 Oct figure** and needs updating.
- **Unbilled calls.** Trials the router logged at $0 had an upstream cost of ${Q8["zero_billed_upstream"]:.4f}, which is not included.
- **By run:** `tables/q8_spend.csv`.

## Figures

All in `report/figures/`, 300 dpi, using the same colour-vision-checked palette as figures 1-4. Each series also has its own marker. All three are post hoc.

- **Figure 5, `fig5_dose_response.png`.** False-option rate by evidence level, with item-level 95% intervals. Text above each stack gives the memory effect in points. Tick labels give no-belief accuracy. The no-passage level comes from a different run than the other two.
- **Figure 6, `fig6_fix_tradeoff.png`.** Harm removed against benefit kept, in points, with item-level 95% intervals. **Every point crosses runs.** Stars mark the main run ("no fix") and removing memory entirely. In panel b Label and Heading sit on the same point. Benefit for Small is limited by its ceiling, and its axes differ from panel a.
- **Figure 7, `fig7_base_vs_instruct.png`.** (a) Rise from a stored false belief. (b) Share of it the label removes. Filled markers are answers; hollow are token probabilities. One model pair; the base interval in panel b touches zero.

## Limits across all sections

- **Nothing here was pre-registered.** These are many tests on data we had seen, with Holm applied only inside each family.
- **Items are still unverified drafts,** and nothing is hand-scored.
- **Intervals generalise to items like these,** by this team, and two to five chosen models.
- **Comparisons with the main run cross nine days.** Section 2 finds no sign of drift, but that is a check on one prompt.
- **Same items, repeated.** All follow-ups reuse the 48 items, so nothing here is fresh evidence on item selection.

## Most informative next test

Rerun `Notes:`, the "may be wrong" caveat and "Student believes" **with a true-memory arm**, on the same day as a baseline. Those are the only moves that cut harm a lot or cheaply, and we do not know what the first two cost. It is a cheap run, and it would settle whether any wording is selective rather than a volume knob.

## Suggested wording for the report

- "The memory effect shrank with evidence: Nemo's rise in false answers was {pt(q1a.loc[(NEMO, "none"), "effect"]).lstrip("+")} points with no passage (95% CI {pt(q1a.loc[(NEMO, "none"), "effect_low"]).lstrip("+")}-{pt(q1a.loc[(NEMO, "none"), "effect_high"]).lstrip("+")}), {pt(q1a.loc[(NEMO, "weak"), "effect"]).lstrip("+")} with a passage leaning toward the answer ({pt(q1a.loc[(NEMO, "weak"), "effect_low"]).lstrip("+")}-{pt(q1a.loc[(NEMO, "weak"), "effect_high"]).lstrip("+")}), and {pt(q1a.loc[(NEMO, "strong"), "effect"]).lstrip("+")} with a passage stating it (0-{pt(q1a.loc[(NEMO, "strong"), "effect_high"]).lstrip("+")}). These comparisons were post hoc."
- "The 'weak' passages raised Nemo's no-memory accuracy only from {pc(st.loc[("all 48", NEMO), "acc_none"])} to {pc(st.loc[("all 48", NEMO), "acc_weak"])}, but removed its false answers at baseline, so they often argued against the false option as well."
- "Wording around the memory changed Nemo's false-answer rate from {pc(w.loc[("notes", NEMO, "stored"), "variant_rate"])} to {pc(w.loc[("bare_fact", NEMO, "stored"), "variant_rate"])} with the belief unchanged. Five runs of the same prompt differed by at most {100 * n.gap_obs:.0f} points, so the reported effect size is specific to our wording."
- "No fix was shown to separate false memories from true ones. The tutor frame cut Nemo's false answers by {pt(-tr.loc[("tutor", NEMO), "si_change"]).lstrip("+")} points ({pt(-tr.loc[("tutor", NEMO), "si_high"]).lstrip("+")}-{pt(-tr.loc[("tutor", NEMO), "si_low"]).lstrip("+")}) and its accuracy on true memories by {pt(-tr.loc[("tutor", NEMO), "sc_change"]).lstrip("+")} ({pt(-tr.loc[("tutor", NEMO), "sc_high"]).lstrip("+")}-{pt(-tr.loc[("tutor", NEMO), "sc_low"]).lstrip("+")}). All such comparisons cross separate runs."
- "The 'unverified' label cost Nemo {pt(-q5.loc[NEMO, "label_change"]).lstrip("+")} points of accuracy on true memories ({pt(-q5.loc[NEMO, "lc_high"]).lstrip("+")}-{pt(-q5.loc[NEMO, "lc_low"]).lstrip("+")}), about half the benefit, in line with the share of harm it removed. The label behaves more like a volume control than a filter. The useful-memory checks were too easy to show this."
- "A true memory did not reduce following of a false passage (Nemo {pc(q4.loc[NEMO, "passage_only_follow"])} to {pc(q4.loc[NEMO, "passage_plus_truth_follow"])}, difference {pt(q4.loc[NEMO, "follow_change"])}, CI {pt(q4.loc[NEMO, "change_low"])} to {pt(q4.loc[NEMO, "change_high"])})."
- "In one base and instruct pair, instruction tuning was not necessary for the effect: base Nemo rose {pt(ba.base).lstrip("+")} points and instruct {pt(ba.other).lstrip("+")} on the same prompt (difference {pt(ba.est)}, CI {pt(ba.ci_low)} to {pt(ba.ci_high)}). This is one quantised pair on a plain-text prompt, and it does not exclude a role for tuning elsewhere. The label worked less well in base."
- "Models that showed no detectable effect on our multiple-choice items were strongly affected on a sample of MemSyco-Bench ({pt(p7.loc[(LLAMA, "snippet vs no_memory"), "est"]).lstrip("+")}-{pt(p7.loc[(QWEN, "snippet vs no_memory"), "est"]).lstrip("+")} points), though that benchmark differs in memory type, answer format and scoring, and is judged by an AI model. 'Unaffected' therefore holds only for our task."
""")

(HERE / "followup_results.md").write_text("\n".join(L), encoding="utf-8")
print("results written")
