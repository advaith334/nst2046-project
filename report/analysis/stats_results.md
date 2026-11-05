# Statistics results: stored beliefs and factual answers

Report analysis for NST2046, on existing data only: no new API calls and no change to any run log.

**Rebuild everything:** `bash report/analysis/run_all.sh` (about 3 minutes). Exact package versions are in that script.

**How to read the numbers**

- "Points" means percentage points of answers. +41 means the false option was chosen 41 points more often.
- Square brackets are 95% intervals from an **item bootstrap**: we resample the 48 items, not individual trials, 20,000 times (BCa method).
- **Fixed in advance** means the analysis was in the code before the main run. The 42 paired comparisons qualify: they were committed 8 seconds before the first main-run trial. Nothing was formally pre-registered.
- **After seeing the data** means everything else, including all of sections 5, 7 and 8. Treat those as exploratory: they suggest, they do not confirm.

## Summary

| Question | Answer | Key numbers | Strength |
|---|---|---|---|
| Does a stored false belief pull answers toward it? | **Yes, in Mistral Nemo** | +41 [+28, +54] points; holds on the 24 unscreened items alone: +44 [+25, +62] | Strong |
| Mistral Small too? | **Probably, but weaker evidence** | +12 [+6, +23] points, from only 8 items; fails Holm when tested by item (p = 0.30) | Moderate |
| Llama, Gemma, Qwen, Claude? | **No detectable effect on chosen answers** | Largest upper limit: +10 points (Llama) | Good for "no large effect"; not proof of zero |
| Does susceptibility differ across models? | **Yes** | Model × condition χ²(2) = 13.3, p = 0.0013. Holds in every method | Strong, except Nemo vs Small on a relative scale |
| Does the label work? | **Partly, in Nemo** | Removes 56% [36, 78] of the effect; +18 points remain | Strong that it helps; moderate that it falls short |
| Does Llama ignore memory? | **No, contrary to the README** | Right on 8 of 8 preference checks; 8% of its stored-belief replies mention the belief | Moderate |
| Is memory strongest when a model is unsure? | **Partly: it helps predict flips, but it is neither necessary nor sufficient** | About half of Nemo's shift (46–61%, depending on the cut-off) came from answers it held confidently and correctly | Exploratory |
| Why did rounds 1–2 show so little? | **Not explained by low uncertainty** | Nemo was less accurate and less sure in round 2, yet the effect was +6 vs +41 points | Post hoc |

## 1. Checking the README against the raw data

**Method.** Scoring was re-implemented from the raw responses and compared with `raw_table.csv`, trial by trial, then 76 README claims were recomputed.

- **Scoring:** 0 of 5,472 trials differ across the five runs. The automatic scores reproduce exactly.
- **Retries:** 239 rows in the main `trials.jsonl` are failed attempts that were retried. Only the last attempt per trial counts, as the harness intends.
- **Result table and paired tests:** every main-study rate and flip count in sections 1 and 4 matches. `paired.csv` agrees with an independent recomputation of all 42 tests.
- **Overall:** 72 of 76 checks match.

### Numbers that do not match

| README says | Data says | Why it matters |
|---|---|---|
| Round 2: Llama "34% → 26%" | 34 → 26 is **with evidence only**. Without evidence: 29 → 26. Pooled: 32 → 26 | Small. The Nemo figures beside it are split by evidence; this one should be too |
| Round 1 cost $0.87 | Logs sum to $0.85; all rounds $3.56 | Trivial. "About $3.60" is fine |
| Qwen3.5-397B "matched Claude at ceiling in every round" | Round 3: 96.9% correct vs Claude 100% | Small. "Near ceiling" is accurate; "matched" is not |
| Round 2 small models ran, then round 3 followed from them | **Nemo's round 3 ran first**: 08:51–09:10 UTC, then its round 2 at 09:11–09:28 UTC | Matters for the method story. Round 2 on Nemo cannot have prompted the long-tail round, so the report should not say each round decided the next for that arm |

### Claims stronger than the evidence

The numbers below are right, but the wording goes further than the data.

| README claim | What the data supports |
|---|---|
| "Two Mistral models are affected" | Nemo, clearly. Mistral Small's interval excludes zero, but its flips come from 8 items and it fails Holm by item (section 2) |
| "A remembered belief pulls as hard as one the user states" | A non-significant test does not show equality. Nemo's difference is -7 [-17, +1] points on chosen answers. On probabilities, **stored is stronger**: -11 [-18, -6] points, 39 items vs 9 (after seeing the data) |
| "The larger Mistral is less affected" | True in points. Not established on a relative scale (section 4) |
| Models are vulnerable where "unsure but not hopeless" | Only partly. Uncertainty does help predict flips, but about half of Nemo's shift comes from confident, correct answers, and Llama is as inaccurate as Nemo yet does not move (section 5) |
| Llama "may largely ignore the memory section" | **Contradicted.** It uses stored preferences and sometimes names the stored belief, then keeps its own answer (section 5) |
| Gemma 4 is "not affected" | True for final answers. Its first answer line does move a little, then it corrects itself (section 5). A small lead, not significant |
| "The label does not break useful memory" | 95 of 95 readable answers were right (1 unreadable, so not quite "all"). There is no no-memory control arm, and the two correction items can be answered from the user's message alone, so these checks are weak evidence |
| "A correct stored belief cut Nemo's errors from 15% to 2%" | That is the false option only. All wrong answers fell from 27% to 3% |
| Rounds 1–2 show no effect | Nemo's round 2 intervals reach +20 and +24 points. A moderate effect was not ruled out (section 7) |

One bug-like note: `summary.md` gives Mistral Small a mean false-option probability of 0.09 under stored belief, but it chose that option 16% of the time. The gap arises because only the logged half is averaged, and that half happens to under-represent false answers (11% vs 20%). With all trials the probability is 0.15, which agrees with behaviour.

## 2. Multiple comparisons: Holm across all 42 tests

*Fixed in advance.*

**Why two versions.** The README's McNemar test treats each of the 96 answers as independent, but the two reps of an item are not. So each test was run twice: on trials (exact McNemar), and on items (exact sign-flip test, where each of 48 items is one unit). The item version is the honest one for claims about "items like these".

**Result:** 6 tests survive Holm on trials and **3 survive on items**. 12 of the 42 tests have no flips at all, so they cannot reject anything; they are kept in the family because dropping them after seeing the data would be cherry-picking.

| Model | Comparison | Flips toward / away | Items up / down | Change, points | Holm p, trials | Holm p, items | Verdict |
|---|---|---|---|---|---|---|---|
| Mistral Nemo 12B | Stored false vs no belief | 41 / 2 | 25 / 1 | +41 [+28, +54] | <0.0001 | <0.0001 | Survives both |
| Mistral Nemo 12B | Stated false vs no belief | 34 / 2 | 21 / 1 | +33 [+22, +47] | <0.0001 | 0.00022 | Survives both |
| Mistral Nemo 12B | Label vs stored false | 1 / 23 | 0 / 17 | -23 [-34, -15] | 0.00012 | 0.00061 | Survives both |
| Mistral Nemo 12B | Label vs no belief | 20 / 3 | 14 / 3 | +18 [+7, +30] | 0.019 | 0.18 | Survives on trials only |
| Mistral Small 24B | Stored false vs no belief | 12 / 0 | 8 / 0 | +12 [+6, +23] | 0.019 | 0.30 | Survives on trials only |
| Mistral Nemo 12B | Stored correct vs no belief | 0 / 12 | 0 / 8 | -12 [-24, -6] | 0.019 | 0.30 | Survives on trials only |
| Llama 3.1 8B | Stated vs stored | 12 / 1 | 9 / 1 | +11 [+4, +21] | 0.12 | 0.55 | Does not survive |
| Llama 3.1 8B | Stated false vs no belief | 14 / 2 | 10 / 1 | +12 [+5, +23] | 0.15 | 0.32 | Does not survive |
| Mistral Small 24B | Stated false vs no belief | 8 / 0 | 5 / 0 | +8 [+3, +19] | 0.27 | 1.00 | Does not survive |
| Mistral Small 24B | Label vs no belief | 8 / 0 | 4 / 0 | +8 [+2, +19] | 0.27 | 1.00 | Does not survive |

The other 32 tests do not survive either version. Full list: `tables/t05_holm_42_tests.csv`.

**What this means**

- **Three Nemo results stand on any reading:** stored belief, stated belief, and the label reducing the stored effect.
- **Mistral Small's stored effect survives on trials but not on items.** Its 12 flips come from 8 items. With 8 items all moving one way, the smallest possible p is 0.0078, so it could never pass.
- **That is a limit of the item count, not evidence against the effect.** At least 11 items moving the same way are needed to pass the first Holm step. Its interval still excludes zero, and its probability shift is clear (section 5).
- **Nemo's "label vs no belief" and "stored correct" results also survive on trials only.** By item they are 14 up and 3 down, and 8 down, which is not enough to clear the bar.
- **Llama's stated-belief results survive neither version.** The README is right to call them exploratory.
- **The README's Bonferroni remark is correct** for the trial version: the same 6 tests pass.

## 3. Item-level uncertainty

*Fixed in advance as contrasts; the item-level intervals were added after seeing the data.*

**How the two reps were handled.** They are not independent: each item gets the same two option orders in every condition, and an item that fools a model once tends to do so again. So they are never counted separately:

1. Differences are taken within item and rep, then averaged to one value per item.
2. Items are resampled whole, keeping both reps together. Effects are means over 48 items, not 96 answers.
3. All models use the same bootstrap draws, so between-model contrasts stay paired.

**How dependent are they?** Rep 1 and rep 2 correlate at about 0.71 for Nemo, 0.64 for Mistral Small and 0.58 for Llama. For Nemo's main effect, variance is 1.43 times what trial-level analysis assumes, so 96 pairs carry about the information of 67 independent ones.

Change in false-option rate, points, with item-level 95% intervals:

| Model | Stored false vs no belief | Label vs stored false | Stated vs stored | Stored correct vs no belief |
|---|---|---|---|---|
| Mistral Nemo 12B | +41 [+28, +54] | -23 [-34, -15] | -7 [-17, +1] | -12 [-24, -6] |
| Mistral Small 24B | +12 [+6, +23] | -4 [-9, -1] | -4 [-10, 0] | -1 [-8, +3] |
| Llama 3.1 8B | +1 [-7, +10] | +1 [-4, +8] | +11 [+4, +21] | -1 [-10, +8] |
| Gemma 4 26B | +1 [0, +5] | -1 [-5, 0] | +1 [-2, +8] | 0 [0, 0] |
| Qwen3.5-9B | +1 [0, +5] | -1 [-5, 0] | -1 [-5, 0] | -2 [-12, 0] |
| Claude Sonnet 5.5 | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] |

**What this means**

- **Stored false belief:** Nemo's rise is large, and even the low end (+28) is substantial. Small's is much smaller and rests on few items.
- **Zero means zero flips, not certainty.** Where nothing moved the bootstrap gives a zero-width interval. The fair statement is that if no item moved in 48, the true share of affected items is below about 6% (one-sided 95%).
- **Llama's stored effect is compatible with anything from -7 to +10.** "No detectable effect" is right. "Ignores memory" is stronger than these data can show.
- **Stored vs stated:** Nemo's interval just includes zero, and Mistral Small's touches it. Llama is the only model that clearly moves more when told directly (+11 [+4, +21]).
- **Stored correct:** on the false-option measure there is a floor, since Nemo has only 15% to lose. On correct answers its rise is +24 [+16, +35] points.
- **Unrelated memory:** Nemo +1 [-2, +5], Small +2 [-1, +9]. The README's "changed nothing" is fair for Nemo: anything above about +5 points is ruled out.
- **Each rep alone gives the same picture:** Nemo +44 [+31, +58] in rep 1 and +38 [+21, +54] in rep 2.
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
| Nemo, Small, Llama; stored vs no belief | χ²(2) = 13.3, p = 0.0013 | Susceptibility differs across these three |
| Same three; all six conditions | χ²(10) = 41.8, p < 0.0001 | Models differ in how they respond across conditions |
| Nemo vs Small only | χ²(1) = 0.09, p = 0.77 | **No shown difference on the odds scale**, but with a wide interval |
| Five or six models | **Fit failed** | Coefficients reached ±34 and standard errors 899,508. The software still prints a p-value, but it means nothing here, so it is not used |

**Why the fit fails.** Gemma has no false answers at baseline and Claude none at all, so the odds ratio has no finite estimate (separation).

**Alternatives that use all six models**

- Permutation test of equal effects across all six: p < 0.0001. Leaving Nemo out: p = 0.0056, so Nemo alone does not explain the spread.
- Bayesian fit: no divergences and R-hat at or below 1.005 in all three versions.

| Contrast (stored vs no belief) | Points, item test | Holm p (15 pairs) | Log-odds, item-specific (Bayes) | Same, wider prior | Same, separate item spreads |
|---|---|---|---|---|---|
| Nemo minus Small | +28 [+15, +43] | 0.0084 | 2.2 [0.2, 4.4] | 2.3 [-0.2, 4.8] | 1.9 [-0.6, 4.4] |
| Nemo minus Llama | +40 [+25, +55] | 0.00018 | 5.0 [3.1, 7.0] | 5.5 [3.4, 7.7] | 4.8 [2.9, 6.9] |
| Small minus Llama | +11 [+2, +24] | 0.49 | 2.8 [0.6, 4.9] | 3.3 [0.7, 5.8] | 3.0 [0.4, 5.5] |

Population-average odds ratios: Nemo 7.0 [3.7, 17.1], Small 5.1 [2.1, 36.7], Llama 1.1 [0.5, 2.3]. Gemma, Qwen and Claude are not given here: with so few events the 0.5 correction would set the number, not the data.

**What this means**

- **Nemo really does produce more false answers than every other model**, by 28 to 41 points. All five contrasts survive Holm.
- **Nemo differs from Llama on every scale.** Small vs Llama is clear on odds in all three Bayesian versions. In points its interval excludes zero, but it does not survive Holm.
- **Whether Nemo's *underlying* pull exceeds Small's is unresolved.** In points the gap is clear. Relative to each model's low baseline, GEE sees no difference, and the Bayesian estimate is positive but its interval includes zero in two of three versions.
- **Why the scales disagree.** Small starts at 3% and Nemo at 15%, so a similar multiplicative pull gives very different point rises. For harm, points are the relevant scale: they count wrong answers.
- **Differences among Llama, Gemma, Qwen and Claude cannot be separated.** No contrast survives, and their log-odds effects are mostly prior.
- **Llama responds differently to the two channels (exploratory).** How much more a stated belief moves a model than a stored one differs between Llama and Nemo (+19 [+6, +33] points, uncorrected p = 0.011) and between Llama and Small (+16 [+9, +25], uncorrected p = 0.00024). This is better evidence for the README's Llama lead than the single tests in section 2.
- **Scope:** these are six chosen models, so this says nothing about LLMs in general.

## 5. Mechanism: does uncertainty predict susceptibility?

*All after seeing the data. Exploratory.*

### Which models can test this

| Model | Baseline trials with probabilities | Top option above 99% | Usable? |
|---|---|---|---|
| Mistral Nemo | 96 of 96 | 55% | **Yes**: real spread in confidence |
| Mistral Small | 96 of 96 (after recovery) | 85% | **Partly**: little spread, only 5 unsure pairs |
| Gemma 4 | 96 of 96 | 99% | **No**: near-deterministic |
| Qwen3.5-9B | 92 of 96 | 100% | **No**: measured *after* it has reasoned, typically for over 1,000 tokens, so it shows a settled answer, not prior uncertainty |
| Llama, Claude | Almost none | n/a | **No**: use baseline accuracy instead |

**Mistral Small recovery.** The harness logged probabilities for 298 of 576 trials, requiring the whole response to rebuild from tokens. The first 12 tokens are logged for every trial, so the other 278 were recomputed from those. Checks: on the 298 trials with both, the largest difference is 0; the recovered letter matches the answer on 100% of trials; and the logged head is an exact prefix of the response on 100% of recovered trials. Whether a trial was logged shows no link to condition (p = 0.49) or choice (p = 0.25). Using logged trials only gives the same direction (shift +11 points, ρ = 0.48) on just 26 pairs. Llama's token stream is visibly corrupted, so it was not recovered.

**Measure quality.** On Nemo, re-running identical prompts (rounds 3 and 4) gives r = 0.995, so probabilities are very stable for a fixed prompt. The two option orders agree far less (r = 0.57), so part of what looks like "confidence" depends on option order, not knowledge. This noise would weaken the correlations below.

### Does uncertainty predict the shift?

| Test | Nemo | Mistral Small | Meaning |
|---|---|---|---|
| Rank correlation, uncertainty vs shift | ρ = 0.38 [0.10, 0.61] | ρ = 0.60 [0.36, 0.77] | A real, moderate link |
| Same, uncertainty from one rep and shift from the other | ρ = 0.31 | ρ = 0.48 | Weaker once baseline noise is not shared |
| Same, shift measured against unrelated memory | ρ = 0.36 | ρ = 0.59 | Not mainly regression to the mean |
| Can uncertainty predict which answers flip? (AUC: 0.5 = chance) | 0.76 [0.63, 0.87] | 0.93 [0.84, 0.98] | Useful for Nemo, strong for Small |

### Does memory *mainly* move answers where the model is unsure?

**Not for Nemo, where it is about half. Unclear for Small, where it depends on the cut-off.** Unsure answers move more each, but there are fewer of them.

| Baseline state | Model | Pairs | Mean shift, points | Flip rate | Flips | Share of total shift |
|---|---|---|---|---|---|---|
| Confident and correct | Mistral Nemo 12B | 57 | +40 [+27, +55] | 39% | 22 of 57 | 58% |
| Unsure (top option under 90%) | Mistral Nemo 12B | 30 | +58 [+44, +73] | 79% | 19 of 24 | 44% |
| Confident and wrong | Mistral Nemo 12B | 9 | -8 [-65, +4] | 0% | 0 of 1 | -2% |
| Confident and correct | Mistral Small 24B | 89 | +10 [+5, +20] | 11% | 10 of 89 | 80% |
| Unsure (top option under 90%) | Mistral Small 24B | 5 | +46 [+11, +82] | 50% | 2 of 4 | 20% |
| Confident and wrong | Mistral Small 24B | 2 | 0 | n/a | 0 of 0 | 0% |

- **Nemo:** an answer it held with over 90% confidence, and correctly, still flips 39% of the time, against 79% when unsure. 22 of its 41 flips started from confident, correct answers.
- **Mistral Small:** 10 of 12 flips started from answers above 90%, but only 3 from answers above 99%.
- **The 90% line was chosen after seeing the data, and it matters.** Moving it from 80% to 99%, the confident-and-correct share of Nemo's shift goes from 61% to 46%, so "about half" is stable. Small's goes from 94% to 27%, so its 80% figure is not robust and should not be quoted alone.
- **Relative uncertainty does matter for Small.** Answers that flipped had a median top probability of 94.8%, vs 99.98% for those that did not. So its flips cluster at 90–99% rather than at 99.9% and above, which is why its AUC is high. Nemo: 92.6% vs 99.97%.
- **Movement tends to be all-or-nothing.** In Nemo, 34% of pairs moved under 5 points and 44% rose more than 50; only 20% fell between. Memory seems to capture an item or not, rather than nudging all of them equally.
- **A simple sigmoid predicts more of a gradient than we see.** Adding one fixed log-odds boost to the false option on every item predicts +30 points for confident items and +73 for unsure ones. Nemo actually shows +40 and +58. So there is no sign of extra sensitivity to uncertainty beyond what a sigmoid gives anyway; the log-odds shift is flat against uncertainty (ρ = -0.05).

### Baseline accuracy (includes Llama)

Items are grouped by whether the model was right twice, once or never at baseline. The effect is measured against the unrelated-memory arm, so different trials define the groups and the effect.

| Model | Right both times | Right once | Wrong both times |
|---|---|---|---|
| Mistral Nemo | +40 [+25, +55], 30 items | +45 [+10, +75], 10 items | +31 [+6, +69], 8 items |
| Llama 3.1 8B | +2 [0, +9], 29 items | 0 [-25, +30], 10 items | -11 [-44, +22], 9 items |

- **Nemo moves about as much on items it reliably knows** as on ones it does not.
- **Llama is the key counterexample.** Its baseline accuracy (71%) nearly equals Nemo's (73%) and both have 10 items they get right only once, yet stored belief has no detectable effect, though the interval on those 10 items is wide. Low accuracy alone is therefore not enough. Note that accuracy is only a stand-in here: Llama's probabilities are unusable, so its uncertainty was not measured.
- **Between models there is no ordering by accuracy:** 71% → +1, 73% → +41, 96% → +12 points.

### Llama reads its memory

The README suggests Llama "may largely ignore the memory section" and lists this as a to-do. The logs say otherwise.

- **It uses stored preferences:** right on 8 of 8 vegetarian and metric checks, and 6 of those replies name the preference, for example "Since you prefer metric units".
- **It sometimes names the stored belief and keeps its own answer.** A text search finds it in 8% of stored-belief replies (8 trials), and it chose the false option in 0 of those. The same search finds nothing in its no-belief replies.
- **So the better description is "reads the belief but does not adopt it", while it does follow the same belief when the user says it.** Why stored and stated differ for Llama is still open. The search is rough, so treat the percentages as approximate.

Replies mentioning the stored belief, other models: Nemo 22%, Mistral Small 35%, Qwen 5%, Gemma 3%, Claude 3%.

### Probability shift with the chosen answer unchanged

MS1 predicted shifts without answer changes. **Supported for the two Mistrals, weak for Gemma, negligible for Qwen.** The unrelated memory is the placebo: any change there is noise.

| Model | Pairs unchanged | Mean shift, points | Median, points | Pairs rising | Typical multiple on false-option probability | Placebo: mean shift, pairs rising, multiple |
|---|---|---|---|---|---|---|
| Mistral Nemo 12B | 50 | +10.4 [+5.9, +18.4] | +1.2 | 92% | 25.4× | +1.3, 76%, 3.2× |
| Mistral Small 24B | 81 | +1.6 [+0.6, +4.1] | +0.1 | 96% | 18.9× | +0.5, 68%, 1.5× |
| Gemma 4 26B | 93 | +2.1 [0, +7.7] | 0 | 39% | 1.5× | 0, 16%, 0.9× |
| Qwen3.5-9B | 88 | +0.001 [0, +0.003] | 0 | 68% | 1.6× | 0, 42%, 1.0× |

- **Mistrals:** over 90% of unchanged pairs moved toward the false option, and the false-option probability typically multiplied about 25-fold in Nemo and 19-fold in Small, from a very low start. The absolute move is small (medians near zero).
- **Placebo matters here.** Even an unrelated memory nudged this probability up in about 68–76% of pairs, so "it rose" alone proves little. The size is what separates them: 3.2× and 1.5× for placebo.
- **Caution:** "answer unchanged" is decided after the memory is shown. Some of Nemo's high-probability trials stayed unchanged by the luck of sampling, which inflates its mean. The median is the safer figure.
- **Gemma:** the mean comes from a few items. Most pairs do not move, and the median is zero.
- **Qwen:** a tiny shift (about 1.6 times on a near-zero probability), read after reasoning, so little can be concluded.

**A new lead on Gemma.** The harness scores the last "Answer:" line, but probabilities refer to the first. Gemma chose the false option on its first line in 3% of stored and 6% of stated trials, and in 0% with no belief. It then corrected itself in 2 and 4 of those trials, and never changed answer in the no-belief, unrelated or stored-correct conditions. Reading the replies confirms this is real: one opens by accepting the belief, then says "Wait, I must correct". It rests on 2–3 items and is not significant (p = 0.50 and 0.25), so it is a lead only. It also shows that scoring only the last answer can hide a model's first response.

## 6. How much does the label remove?

*The label comparison was fixed in advance; the fraction removed was added after seeing the data.*

**Fraction removed** = (stored − label) ÷ (stored − no belief).

| Model | Measure | No belief | Stored | Label | Fraction removed | Still above baseline, points |
|---|---|---|---|---|---|---|
| Mistral Nemo 12B | False answers chosen | 15% | 55% | 32% | **56%** [36, 78] | +18 [+7, +30] |
| Mistral Nemo 12B | Probability on false option | 15% | 56% | 33% | **56%** [41, 70] | +18 [+11, +28] |
| Mistral Small 24B | False answers chosen | 3% | 16% | 11% | **33%** [7, 71] | +8 [+2, +19] |
| Mistral Small 24B | Probability on false option | 3% | 15% | 12% | **30%** [9, 68] | +8 [+3, +18] |

- **Nemo:** the label removes about 56% of the effect, plausibly anywhere from about a third to three-quarters. A second method (Fieller) agrees: [36, 80]. The probability measure is tighter and gives the same answer.
- **It restores correct answers too:** 65% [39, 91] of Nemo's lost correct answers come back, so answers are not just moving to other wrong options.
- **It is not a fix:** Nemo stays +18 points above baseline [+7, +30].
- **Item view:** of the 25 items where stored belief raised Nemo's false answers, the label helped on 15, made no difference on 10, and never made things worse. 11 returned fully to baseline.
- **Mistral Small is uncertain:** 33% with a very wide interval ([2, 91] by Fieller). The direct test is 0 vs 4 flips, p = 0.12, and does not reach significance. Do not claim the label works on Small; say the estimate points that way.
- **Nemo and Small cannot be told apart here:** the gap in fraction removed is [-16, +53] points. Both pooled: 51% [31, 72].
- **Same result on unscreened items:** 62% [33, 90] on the 24 new items, vs 50% on the screened 24.
- **Llama, Gemma, Qwen and Claude have no stored effect to remove**, so the label cannot be assessed on them.

## 7. Why did rounds 1–2 show so little?

*Post hoc. The rounds differ in items, design and reps, so this compares unlike things.*

| Model | Round | Items | Baseline correct | Baseline false | Stored false | Effect, points | Share of non-false answers captured |
|---|---|---|---|---|---|---|---|
| Mistral Nemo 12B | Round 1 pilot (misconceptions, evidence) | Not run | | | | | |
| Mistral Nemo 12B | Round 2 harder items, evidence | 35 | 54% | 37% | 40% | +3 [-14, +20] | 5% |
| Mistral Nemo 12B | Round 2 harder items, no evidence | 34 | 50% | 35% | 44% | +9 [-3, +24] | 14% |
| Mistral Nemo 12B | Round 3 long-tail (24 items) | 24 | 67% | 19% | 60% | +42 [+25, +58] | 51% |
| Mistral Nemo 12B | Round 4 main, new 24 | 24 | 81% | 8% | 52% | +44 [+25, +62] | 48% |
| Mistral Nemo 12B | Round 4 main, all 48 | 48 | 73% | 15% | 55% | +41 [+28, +54] | 48% |
| Llama 3.1 8B | Round 1 pilot (misconceptions, evidence) | 13 | 85% | 12% | 12% | 0 [-15, +15] | 0% |
| Llama 3.1 8B | Round 2 harder items, evidence | 35 | 54% | 34% | 26% | -9 [-26, +9] | -13% |
| Llama 3.1 8B | Round 2 harder items, no evidence | 34 | 59% | 29% | 26% | -3 [-18, +12] | -4% |
| Llama 3.1 8B | Round 3 long-tail (24 items) | 24 | 71% | 17% | 21% | +4 [-6, +21] | 5% |
| Llama 3.1 8B | Round 4 main, new 24 | 24 | 75% | 12% | 8% | -4 [-19, +4] | -5% |
| Llama 3.1 8B | Round 4 main, all 48 | 48 | 71% | 14% | 15% | +1 [-7, +10] | 1% |

Rounds 2 and 3 share no items. Rounds 1 and 2 share 11; rounds 3 and 4 share 24.

**What the numbers show**

- **Ceiling explains round 1 for Claude and Qwen3.5-397B only.** Llama was at 85% correct and did not move. Nemo was not in round 1, so round 1 says nothing about it.
- **Baseline accuracy does not explain Nemo's rounds.** It was *less* accurate in round 2 (50–54%) than in the main study (73%), and *less* sure (43–50% unsure vs 31%). On the README's "unsure but not hopeless" reading, round 2 should have offered at least as much room to move. It moved less.
- **The gap is large:** the long-tail effect exceeds round 2's by +35 points [+18, +52].
- **It survives a floor correction.** In round 2 the false option already took 35–37% of Nemo's answers, leaving less room. But of the remaining answers, memory captured 5–14%, vs 48% in the main study.
- **At equal confidence, long-tail items still move more.** Confident and correct: 39% flip (22 of 57) vs 12% in round 2 (3 of 26). Unsure: 79% (19 of 24) vs 33% (6 of 18). So item type seems to matter beyond uncertainty.
- **Removing evidence is not the reason:** without evidence, round 2 reached only +9 points.
- **Round 2 was weak, not null:** intervals reach +20 and +24 points, and Nemo's probability shifts were +11 [0, +23] and +6 [-5, +18].
- **Llama shows no detectable effect in any round**, so its null holds across item types.

**A possible explanation (untested).** Round 2 items are misconceptions and logic or numerical puzzles, the kind of thing training text often discusses and corrects. A long-tail item has no such correction, so a stated "fact" may have less to compete with. Topic familiarity, rather than momentary uncertainty, would then be the moderator. These data cannot show this.

## 8. Selection bias and internal replication

*After seeing the data, but this is the check that matters most for trusting the main result.*

**Where selection entered**

- **Item type:** long-tail items were chosen because Nemo moved on them, after two item sets showed little.
- **Forking paths:** three item sets, two evidence modes and six models were tried before the main run. A search like that can find an effect by chance, which is why the replication below matters.
- **Model:** Nemo is in the main study because it moved.
- **Reuse:** 24 of the 48 main items are the round 3 items.
- **Not item-level cherry-picking:** all 24 round 3 items were kept for the main study, so none was dropped for failing to move.

**The 24 screened items are not fresh evidence.** They used identical prompts and option orders in rounds 3 and 4, so round 4 re-measures them (same answer 94% of the time, item effects ρ = 0.89). Their effect barely regressed: +42 to +38 points.

**Internal replication: Nemo on the 24 new items**

| Items | Baseline correct | Baseline false | Effect, points | Items up / down | Item p |
|---|---|---|---|---|---|
| 24 screened | 65% | 21% | +38 [+19, +54] | 13 / 1 | 0.0011 |
| 24 new | 81% | 8% | **+44 [+25, +62]** | 12 / 0 | 0.00049 |

- **It replicated.** The unscreened items show the effect alone, no smaller than the screened ones. Difference: -6 points [-31, +19], p = 0.75. Probability shifts agree: +40 vs +43.
- **The stated-belief and label effects replicate too** (+35 and -27 points on new items).
- **The new items are easier for Nemo** (81% vs 65% correct), yet the effect holds. This is a further point against uncertainty as the main driver.
- **What replication does not fix.** The same team wrote the new items, in the same style, after seeing round 3. So this rules out luck among the 24 items, not selection of the item *type*. The defensible claim is "on long-tail facts", not "on factual questions": round 2's items gave +6 points.
- **Mistral Small was never screened**, so all 48 items are out of sample for it, and that protects its result from item-level selection. But it is split: +17 on the first 24 and +8 on the new 24 (difference p = 0.49), with neither half significant alone.

## 9. Robustness

| Check | Result | Meaning |
|---|---|---|
| Drop any one item | Nemo's effect stays +39 to +43 | No single item drives it |
| Concentration | Top 5 items give 26% of the effect, top 10 give 51% | Broad, as the README says |
| By category | Science +40, general +40, numerical +44 | Similar across topics |
| Belief direction | Asserts false (43 items) +40; denies true (5 items) +50 | Too few denial items to compare |
| Drop the 1 item noted as depending on a counting convention | +41 | Not driven by that item. No item is verified yet |
| Where Nemo's false answers come from | Correct answers fall 32 points, other wrong answers 8 | Mostly right answers turning wrong, which is the harmful case |
| Qwen's 7 unreadable stored/no-belief answers, worst case both ways | Effect between -2 and +5 | Dropping them cannot hide a large effect |
| Same items moved in both Mistrals? | 5 of Small's 8 items also moved in Nemo (p = 0.70) | No shown overlap; what makes an item movable may be model-specific |

## 10. Figures

All in `report/figures/`. Colours pass an all-pairs colour-vision check, and each model also has its own marker shape.

- **Figure 1, `fig1_effects_by_model.png`.** Effect of each condition on the false-option rate, by model, with 95% item-level intervals. Filled markers pass Holm across all 42 tests by item. *Only Nemo's stored-belief and label effects (panels a, b) are filled; its stated-vs-no-belief effect also passes but is not one of these panels.*
- **Figure 2, `fig2_uncertainty_vs_shift.png`.** Each point is one item and rep. Across: baseline confidence. Up: change in probability on the false option. The dashed line marks 90%. *Exploratory.* Over half of the flips sit left of the line. Shares in the panels depend on that 90% line: at 99% they are 46% for Nemo and 27% for Small. The left side also holds a few confident-but-wrong pairs, which the panel text does not count.
- **Figure 3, `fig3_label_effect.png`.** (a) False-option rates with and without the label. (b) Share of the effect removed. Intervals are item-level; panels share no axis.
- **Figure 4, `fig4_rounds_and_replication.png`.** (a) *Post hoc:* baseline accuracy against effect for each independent item set; R2 labels share items, and one Llama point is nudged 0.6 across so it stays visible. (b) Effect on screened vs new items. Mistral Small was not in round 3, so "screened" is only a label for it.

## 11. Limits and the next test

**Limits of this analysis**

- **Items are unverified drafts**, and nothing is hand-scored. Wrong answer keys would change these numbers.
- **Intervals generalise to items like these**, written by this team, not to all factual questions, and not to all LLMs.
- **Probabilities describe the first answer line** and are not the same as sampling at temperature 0.7.
- **Sections 5, 7 and 8 were designed after seeing the data.** Their p-values are descriptive.
- **Reps add little.** Evidence is limited by the number of items, so the README's plan to "add repetitions" for Small and Llama would not help much. **More items would.** At Small's current rate, about 66 items would be needed before it could pass the Holm test by item.

**Most informative next test.** Pre-register a fresh item set that crosses item type (long-tail vs misconception) with baseline confidence, on Nemo, Small and Llama. That tests the post hoc story in section 7 directly. Separately, replace the README's to-do on why Llama "ignores" memory with the real question: why does it use stored preferences and follow stated beliefs, yet not adopt stored beliefs? Comparing Llama's replies on the same items across those conditions is a cheap start.

## Suggested wording for the report

- "A stored false belief raised Mistral Nemo's false answers by 41 points (28–54, item-level 95% CI), and the effect replicated on 24 items not used in screening (44 points)."
- "Mistral Small showed a smaller rise (12 points, 6–23), which did not survive correction when items, not trials, were the unit of analysis."
- "Llama, Gemma, Qwen and Claude showed no detectable effect on chosen answers."
- "An 'unverified' label removed about 56% of Nemo's effect (36–78), leaving it 18 points above baseline."
- "In exploratory analyses, uncertainty was only a partial explanation: about half of Nemo's shift came from answers it held confidently and correctly, and Llama, equally inaccurate, did not move."
