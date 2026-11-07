# Confirmatory results

Pre-registered in `report/preregistration.md`, locked at commit `04486fc` before any trial. Item SHA-256 `3f74b5a2…`. AI-drafted. Rebuild: `uv run --no-project --python 3.12 --with pandas==3.1.0 --with numpy==2.5.4 --with scipy==1.18.1 --with pyyaml==6.0.3 python report/analysis/confirm/confirm_analysis.py`. It needs the trial logs, which are not in git. The tables are in `tables/`.

**In short:** all five primary hypotheses pass. Harm appears in every open model. One secondary hypothesis fails in part (H7d), and one can't be settled (H8). Claude is incomplete.

## What ran

| Part | Planned | Done | Errors left | Unparseable | US$ |
|---|---|---|---|---|---|
| Default, 5 open models | 4,800 | 4,800 | 10 | 37 | 0.96 |
| Claude check | 240 | **167 (cap)** | 0 | 0 | 0.45 |
| "Notes:" | 1,440 | 1,440 | 0 | 0 | 0.04 |
| Caveat | 1,440 | 1,440 | 0 | 0 | 0.04 |
| Tutor | 720 | 720 | 0 | 0 | 0.04 |
| Patient | 720 | 720 | 0 | 0 | 0.01 |
| **Total** | 9,360 | **9,287** | 10 | 37 | **1.54** |

Changes from the plan are in the pre-registration's "Stopping and spend" section. The cap rose from US$1.25 to US$1.55 after 326 trials, on cost alone, with no outcome looked at. 149 attempts were retries of errors, which the plan allows once. Most were rate limits on Qwen3.5-9B.

## Hypotheses

Points, with 95% item-bootstrap intervals. Holm runs across the five primary tests, and separately across the eight secondary tests.

| ID | Claim | Estimate | Items up / down | Holm p | Verdict |
|---|---|---|---|---|---|
| H1 | Harm above zero, Nemo | +55 [+47, +63] | 81 / 0 | <0.001 | **Pass** |
| H2 | Harm above zero, Mistral Small | +35 [+28, +43] | 54 / 1 | <0.001 | **Pass** |
| H3 | Label reduces Nemo's harm | +15 [+10, +21] | 29 / 1 | <0.001 | **Pass** |
| H4 | Labelled memory stays above no belief, Nemo | +40 [+32, +48] | 62 / 2 | <0.001 | **Pass** |
| H5 | Benefit above zero, Nemo | +44 [+37, +52] | 70 / 1 | <0.001 | **Pass** |
| H6a | Harm differs from zero, Llama | +30 [+23, +38] | 56 / 6 | <0.001 | Yes, it does |
| H6b | Harm differs from zero, Gemma | +6 [+3, +11] | 10 / 0 | 0.006 | Yes, it does |
| H6c | Harm differs from zero, Qwen3.5-9B | +12 [+8, +19] | 18 / 0 | <0.001 | Yes, it does |
| H7a | Tutor frame reduces Nemo's harm (school) | +53 [+41, +68] | 40 / 2 | <0.001 | **Pass** |
| H7b | Tutor frame reduces Nemo's benefit (school) | +33 [+20, +48] | 33 / 7 | <0.001 | **Pass** |
| H7c | Patient frame reduces Nemo's harm (health) | +29 [+19, +40] | 27 / 3 | <0.001 | **Pass** |
| H7d | Patient frame reduces Nemo's benefit (health) | +7 [−1, +15] | 13 / 7 | 0.17 | **Fail** |
| H8 | Nemo's harm similar, school minus health | +15 [−1, +30] | n/a | 0.15 | **Not settled** |

- **H7 as written fails.** It said each frame cuts both harm and benefit, and the patient frame's cut to benefit was not detected.
- **H8 can't pass as written.** The plan set no margin for "similar". The interval allows anything from no gap to 30 points, so we can't say they're similar or different.

## By model

| Model | Correct, no memory | False, no memory | False, false memory | False, labelled | Correct, true memory | Harm | Label cut | Benefit |
|---|---|---|---|---|---|---|---|---|
| Nemo | 50% | 15% | 70% | 55% | 94% | +55 | +15 | +44 |
| Mistral Small | 75% | 8% | 43% | 28% | 98% | +35 | +15 | +23 |
| Llama | 55% | 17% | 46% | 34% | 81% | +30 | +14 | +26 |
| Qwen3.5-9B | 90% | 4% | 17% | 9% | 98% | +12 | +9 | +7 |
| Gemma | 89% | 5% | 12% | 8% | 95% | +6 | +4 | +6 |
| Claude, incomplete | 93% | 3% | 3% | n/a | n/a | +2 [0, +8], 60 items | n/a | n/a |

Claude's rates use all 167 trials. Its effect uses the 60 items with both arms.

## Open questions

**Q1: do "Notes:" and the caveat keep Nemo's benefit?** Not fully. Both cut harm and benefit.

| Wording | Model | Harm, was → now | Harm cut | Benefit, was → now | Benefit cut |
|---|---|---|---|---|---|
| "Notes:" | Nemo | +55 → +43 | +13 [+6, +19] | +44 → +37 | +8 [+1, +15] |
| Caveat | Nemo | +55 → +30 | +25 [+17, +33] | +44 → +33 | +11 [+4, +18] |
| "Notes:" | Small | +35 → +31 | +4 [−1, +10] | +23 → +20 | +2 [−3, +8] |
| Caveat | Small | +35 → +25 | +10 [+5, +15] | +23 → +21 | +1 [−3, +6] |

**Q2: does Claude's harm differ from zero?** Not detected: +2 [0, +8], one item moved, on 60 complete items. That is incomplete evidence. Claude scored 93% on these items with no memory, so its resistance here no longer rests on items a Claude model wrote.

## Exploratory, not pre-registered

- **Selectivity.** Share of harm left against share of benefit left, on the same items. Only the first row's interval clearly favours keeping benefit, and this contradicts the long-tail patient run, where benefit vanished.

  | Fix | Model | Harm left | Benefit left | Gap [95%] |
  |---|---|---|---|---|
  | Patient frame | Nemo | 39% | 81% | +42 [+14, +70] |
  | Patient frame | Small | 38% | 48% | +10 [−26, +55] |
  | Caveat | Nemo | 55% | 75% | +20 [0, +40] |
  | Caveat | Small | 73% | 94% | +22 [−2, +48] |
  | Tutor frame | Nemo | 15% | 38% | +23 [−7, +55] |
  | Tutor frame | Small | 17% | 21% | +4 [−56, +51] |
  | "Notes:" | Nemo | 77% | 83% | +6 [−11, +23] |

- **The tutor frame lowers accuracy overall.** On school items Nemo's false answers with no memory rise from 18% to 26%, and accuracy with a true memory falls from 94% to 55%. Part of its "harm cut" is a worse baseline.
- **The patient frame does not.** On health items Nemo's no-memory accuracy stays at 58–59%. With a true memory it goes from 94% to 87%, and false answers with a false memory go from 61% to 33%.
- **Knowledge.** On items each model got right both times with no memory, a false memory still drew false answers from Nemo 46%, Llama 32% and Small 31%, against Qwen 8% and Gemma 5%. On the few items Gemma and Qwen were unsure of, they followed it 50% and 77% of the time (16 and 15 items). Items were picked on the baseline, so some of this is regression to the mean.
- **The label is weaker here.** It removes 28% of Nemo's harm, against 56% in the main study. This run has no labelled true memory, so its cost is unknown.
- **Domain.** Qwen's harm is all in health items (0 school, +24 health). Gemma leans the same way (+2, +11). Small numbers of items moved.

## How far this goes

- **Not comparable with the main study.** The belief sentence here is `the answer to "<question>" is <option>`, which repeats the question. That may strengthen the effect, so differences from the main study are descriptive only.
- **MMLU keys are taken as given.** No key has been checked, and no sensitivity analysis has been needed yet.
- **Same limits as before.** Synthetic single turns, multiple choice, English, no users, and rates that don't describe any product.
