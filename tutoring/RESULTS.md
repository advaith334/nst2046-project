# Tutoring simulation: results

AI-designed, AI-run and AI-judged. No person has checked a reply, and no student took part. Plan: `tutoring/README.md`, committed before the run. Tables: `tutoring/analysis/tables/`.

**In short:** three of five predictions failed and one of those reversed. In the tutor role a false note did not raise false answers. Without the role it did. Only models that knew the answer could tell a false note from a true one.

## Pre-registered tests (planned run, 500 tokens)

Points, with 95% item-bootstrap intervals. Holm across the five tests. Total spend for the planned run was US$2.27.

| ID | Prediction | Result | Holm p | Verdict |
|---|---|---|---|---|
| T1 | Nemo's harm above zero | +2 [-7, +10] | 1.00 | **Fail** |
| T2 | Nemo's benefit above zero | +5 [-7, +18] | 1.00 | **Fail** |
| T3 | Purpose sentence cuts Nemo's harm | +3 [-5, +13] | 1.00 | **Fail** |
| T4 | Haiku tells the student more than Nemo | +58 [+43, +70] | <0.001 | Pass |
| T5 | Nemo more false at turn 2 with a false note | -32 [-47, -15] | 0.004 | **Reversed** |

Second judge: same verdicts. Agreement: kappa 0.91 on the final answer, 0.92 on telling the student, 0.86 at turn 2.

**Q1, does the purpose sentence keep Nemo's benefit?** There was no benefit to keep, so the question falls away.

## The token-limit mistake

The 500-token limit cut off 28% of Nemo's, 32% of Llama's, 57% of Gemma's and 59% of Mistral Small's first replies. Claude's were not cut off. Gemma's results are not used. A post hoc rerun at 1,500 tokens (US$0.23) cut off 2 to 11% and gave the same verdicts.

## By tutor

Open models from the rerun, Claude models from the planned run. Sonnet ran on 20 items.

| Tutor | Correct, no note | Told wrong: false note / true note | With purpose sentence | Turn 2 false: no note / false note / purpose |
|---|---|---|---|---|
| Nemo | 57% | 13% / 7% | 68% / 42% | 70% / 43% / 30% |
| Llama | 70% | 22% / 13% | 45% / 25% | 40% / 35% / 30% |
| Mistral Small | 88% | 45% / 17% | 83% / 13% | 5% / 5% / 5% |
| Claude Haiku | 97% | 72% / 2% | 88% / 2% | 2% / 2% / 2% |
| Claude Sonnet | 100% | 65% / 0% | 70% / 0% | 0% / 0% / 0% |

## No tutor role (post hoc, US$0.05)

Same free-text task, "You are a helpful assistant", "Saved memories about this user", first turn only.

| Model | Harm with no role | Harm in the tutor role |
|---|---|---|
| Nemo | +15 [+3, +28] | 0 [-10, +10] |
| Llama | +13 [+2, +25] | 0 [-8, +8] |
| Mistral Small | +5 [-2, +13] | +3 [-2, +12] |

These compare separate runs. Nemo's multiple-choice harm on the same items was +63.

## How far this goes

- Single scripted exchanges on exam items, with no learning measured.
- The note repeats the question.
- Both judges are AI, and Haiku is also a tutor here.
- The reruns were decided after the first results were seen.
