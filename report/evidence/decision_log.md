# Decision log

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026 from the session log and git history, and extended the same day with rows 47–69. **Advaith must check every row before submission, and the team must complete the blank rows.**

Fields follow the guidelines: date, decision, reason, evidence, owner. Dates and times are SGT. "Session" means the Claude Code session log of that time.

## How owners were assigned

| Owner wording | Meaning |
|---|---|
| **Advaith** | Advaith said it in his own words |
| **AI assistant proposed, Advaith approved** | Claude Code proposed it and Advaith accepted. "(button)" means he clicked a reply whose text the assistant had written |
| **AI assistant, no separate approval** | Claude Code did it during the work and reported it afterwards, or the session shows no approval |
| **Dr Filippov advised** | The recommendation came from his 7 Oct feedback, as recorded in an AI-summarised Wispr note |
| **[TEAM TO COMPLETE]** | No evidence in the repo or session. Nothing is attributed to Aditya, Elkan or Tony |

**Read this before relying on the log.** Most study-design decisions on 27 Oct were proposed by the assistant and approved with one click, and the button text was written by the assistant. The session shows no discussion with the wider team. If the team did discuss these, add it with evidence. Do not rewrite an owner without evidence.

## Decisions

### Set-up

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 1 | 7 Oct | Run a minimal experiment before refining; pilots are too easy; narrow to 4–6 models and 40–60 items; show exact prompts; randomise option order; double-score a sample | MS1's main risk was a design that could not show an effect | Wispr note of the meeting (AI summary; the full transcript was not accessible to the assistant) | Dr Filippov advised. Team response: [TEAM TO COMPLETE] |
| 2 | 7–27 Oct | **No run is recorded for 20 days** although the note says to start "this week" | Not recorded | Repo was empty until 27 Oct | [TEAM TO COMPLETE] |
| 3 | 27 Oct 14:21 | Use OpenRouter only for all models | One key and one client. The assistant marked this "Recommended" | Session 14:18–14:21. A third option, OpenRouter plus local Ollama, was offered and described as needed for true base-model runs | AI assistant proposed, Advaith approved (question card) |
| 4 | 27 Oct 14:21 | Scope the first pass as harness, draft cases and pilot | Follows the feedback | Same card; approved plan saved at 14:23 | AI assistant proposed, Advaith approved |
| 5 | 27 Oct 14:23 | Put memory in the system prompt as a list of saved memories; one template set; label applied in one place | Mimic product memory; conditions differ only as intended | Approved plan; label-diff test | AI assistant proposed, Advaith approved |
| 6 | 27 Oct 14:30 | Keep the 2 MS1 pilots as easy controls and add 11 misconception items with evidence; the plan said 10 | Feedback asked for harder items | `pilots.yaml`, `candidates.yaml`; session 14:32 | AI assistant, no separate approval on content. Items were marked draft for team checking |
| 7 | 27 Oct 14:46 | No co-author line and no "Claude" in commits or PRs. The commit was rewritten and the old remote branch deleted | "do not co-author"; "i dont want to see "Claude" anywhere" | Session 14:46–15:03; PR #1. **This hides AI authorship in git, so it must be disclosed in the AI-use log** | Advaith |

### Budget and running

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 8 | 27 Oct 15:12 | Require a cost figure before running; cap the pilot at about $1 | "Before running the experiment, let me know"; "if the whole experiment is $1, then go ahead" | Session 15:12 | Advaith |
| 9 | 27 Oct 15:12 | Pin each model to one host, no fallbacks | Smoke test showed routing to different hosts, which differ in quantisation | `smoke` and `smoke-pinned` logs; `config/models.yaml` | AI assistant, no separate approval; reported at 15:20 |
| 10 | 27 Oct 15:12 | Raise `max_tokens` from 600 to 2000 | Room for Qwen's reasoning | `config/pilot.yaml`; session | AI assistant, no separate approval; reported at 15:20 |
| 11 | 27 Oct 15:15 | Use token probabilities only when returned tokens rebuild the text exactly | CoreWeave and Novita returned unusable tokens | `parse.py`; session 15:13–15:16 | AI assistant, no separate approval; reported at 15:20 |
| 12 | 27 Oct 15:22 | Add $5 credit and resume, retrying only failed trials | 314 of 516 trials refused with 402 | Run log; session 15:20–15:23 | Advaith (credit); resume text was a button |

### From pilot to long-tail items

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 13 | 27 Oct 16:06 | Calibrate difficulty: harder items, weaker or no evidence | Pilot hit ceiling; Claude and Qwen were 100% correct | `runs/pilot-20261027/`; session 15:44 | AI assistant proposed, Advaith approved (button) |
| 14 | 27 Oct 16:07 | Test evidence by removing it entirely as well as as-written. **Weaker evidence was not built** until 5 Nov (row 57) | Simple to test | `evidence_modes: [as_written, none]`. Feedback said "weaker or ambiguous" | AI assistant, within the approval above |
| 15 | 27 Oct 16:29 | Read the last "Answer:" line, not the first, and re-score earlier runs | Claude wrote "Answer: D", then corrected to B, and was counted as accepting the false belief | Session 16:29; `cal_num_digit_ones` | AI assistant, no separate approval; reported at 16:30 |
| 16 | 27 Oct 16:46 | **Move to long-tail facts, and add 2–3 small open models** | Frontier models stayed at ceiling; Llama's shifts looked like noise. The assistant offered this or "commit and write up" | `runs/calibration-20261027/`; session 16:30 | AI assistant proposed, Advaith approved (button, including the model names) |
| 17 | 27 Oct 16:46 | Add a $1 limit and an estimate before running this screen | Budget control. Part of the button text Advaith accepted | Session 16:46 | AI assistant proposed, Advaith approved (button) |
| 18 | 27 Oct 16:49 | Give Qwen3.5-9B 8000 tokens | Ran out mid-reasoning at 2000 | Small-model smoke test; `config/models.yaml` | AI assistant, no separate approval; reported at 16:50 |
| 19 | 27 Oct 16:50 | **Drop evidence passages for long-tail items.** This is a deviation from MS1 | So the answer depends on what the model knows. Removing evidence had shown little difference in round 2 | `longtail.yaml` header; the estimate at 16:50 says "no evidence". Approved at 16:51 (button). **It was not called a deviation until 5 Nov.** Evidence came back as follow-ups (rows 39, 57) | AI assistant proposed, Advaith approved (button) |
| 20 | 27 Oct 16:50 | **Logic items dropped.** Long-tail items are science, general knowledge and numerical only | **No reason is recorded.** Logic items in rounds 1–2 showed no clear memory effect, and long-tail facts are not logic problems, but the session never states this as the reason | No explicit decision in the session. The 17:43 main plan lists the categories. First flagged 5 Nov 12:56 | AI assistant, no separate approval. Advaith approved plans listing the categories; the session does not show he was asked about logic |

### Main study

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 21 | 27 Oct 17:39 | Expand to 48 items, all six conditions plus useful-memory checks, 2 reps | First clear effect (Nemo 19% → 60%). 40–60 items came from the feedback | `runs/longtail-20261027/`; session 17:35 | AI assistant proposed, Advaith approved (button) |
| 22 | 27 Oct 17:43 | **Reduce 12–16 models to 6:** Nemo, Mistral Small, Llama, Gemma 4, Qwen3.5-9B, Claude Sonnet 5.5 | Feedback asked for 4–6 contrasting models. Round 3 identified Nemo as susceptible | Session 17:43; `config/main.yaml` | Dr Filippov advised 4–6; AI assistant proposed the six, Advaith approved (button) |
| 23 | 27 Oct 17:43 | **Exclude Qwen3.5-397B from the main study** | Would add about $1.50, past the $2.73 credit left. "Matched Claude at ceiling": roughly true, but round 3 was 2% → 4% | Session 17:43; `runs/longtail-20261027/summary.csv` | AI assistant proposed, Advaith approved (button) |
| 24 | 27 Oct 17:43 | Keep Sonnet, not Haiku | The assistant offered Haiku as a $0.40 option with a weaker frontier contrast | Session 17:43 | AI assistant proposed both, Advaith chose Sonnet (button) |
| 25 | 27 Oct, by 17:45 | **No OpenAI model.** `gpt-terra` left the main set without comment | **No reason is recorded** | `config/models.yaml` in `c89f2c1` vs `9e374ef` | AI assistant, no separate approval |
| 26 | 27 Oct 14:25, carried through 17:43 | **No base model.** OpenRouter lists none, and a local server was never tried | Consequence of #3. Noted as a limitation, not chosen as a design | Catalogue check 14:25; first `config/models.yaml`; session 17:43 | Advaith chose OpenRouter only (#3). The assistant recorded the consequence. No one decided to attempt a local run until 5 Nov (row 52) |
| 27 | 27 Oct 17:45 | Commit first so the run points to exact code, then run with a $1.95 cap | The record ties to a commit | Commit `9e374ef`; clean manifest | AI assistant proposed, Advaith approved (button) |
| 28 | 27 Oct 20:40 | Check the run; keep the Mac awake | Run looked stuck. Mac had slept 17:50–20:09 | "What is going on? Please make sure that the process is alive."; session 20:40 | Advaith asked; AI assistant acted |
| 29 | 27 Oct 21:31 | Retry 239 failed rows within the cap | Sleep and rate-limit errors | Session 21:31–21:42 | AI assistant, no separate approval. Within the cap Advaith set |

### Analysis and reporting

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 30 | 27 Oct 17:41 | Add exact McNemar paired tests | To answer the label and stored-vs-stated questions directly | `report.py`; session 17:41 | AI assistant; part of the plan approved at 17:45 |
| 31 | 27 Oct 21:43 | **Use Bonferroni across 42 tests as a caveat.** Only Nemo's and Mistral Small's stored-belief results "hold" | 42 comparisons | Session 21:43; README section 5. Not pre-registered. Not implemented in code. 2 reps are treated as independent | AI assistant, no separate approval. Holm and item-level methods were added on 5 Nov: see `report/analysis/stats_results.md` |
| 32 | 28 Oct 09:41 | Write results for the team as a Notion page | Share results | Session 09:41–09:45. Page under NST2046 in NUS Courses | AI assistant proposed, Advaith approved (button) |
| 33 | 28 Oct 10:37 | Commit reports and raw tables but not full trial logs | The logs are large (28 MB). This creates the main reproducibility gap | `.gitignore`; commit `4bfd4cd` | AI assistant proposed, Advaith approved (button) |
| 34 | 2 Nov 19:54 | Document the study in a human-reviewable README | "make it as human-reviewable as possible" | Commit `f232e4f` | Advaith |

### External validation

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 35 | 5 Nov 12:52 | Ask whether an established eval set was used. It was not; all items were written for this project | Advaith's own question | "Are we running these models against some established sycophancy eval set?" | Advaith |
| 36 | 5 Nov 12:54 | Cost, then approve building, a SycophancyEval run: about $0.95, 6,200 trials | Would test whether the result depends on our items | Session 12:53–12:55 | AI assistant proposed, Advaith approved (buttons) |
| 37 | 5 Nov 12:56 | **Stop the SycophancyEval run before anything was downloaded or spent** | "But is this test even related to our paper?" The assistant checked MS1 and found it fits poorly; the claimed comparison with published results would not hold | Session 12:56; no dataset in the repo | Advaith challenged; AI assistant withdrew the proposal |
| 38 | 5 Nov 12:56 | Treat missing evidence and logic items as deviations, and scope MemSyco-Bench instead | MS1 already cites it, and the assistant had missed that | Session 12:56–13:00 | AI assistant proposed, Advaith approved (button) |
| 39 | 5 Nov 13:04 | Approve two more paid runs: evidence rerun and MemSyco-Bench, about $0.76, cap $1.25 | Evidence rerun addresses #19; the benchmark gives an external check | "Approve both runs" (button). Commit `c2d236f`. Outcome: evidence rerun 1,920 trials, $0.148; MemSyco-Bench 2,000 trials, $0.466. Both under their caps | AI assistant proposed, Advaith approved (button) |
| 40 | 5 Nov 13:00 | Use six AI subagents for statistics, qualitative coding, item audit, literature, societal analysis and evidence trail | "spawn subagents and get a lot of work done" | Session 12:59–13:02 | Advaith set the direction; AI assistant chose the workstreams |

### Follow-ups, 5 Nov

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 47 | 5 Nov 13:04 | Hold the evidence rerun until the item audit reports | So a wrong key can't get into new data. The assistant said this of both runs, but MemSyco-Bench started at 13:12, before the audit finished. It uses no project items, though the session doesn't give that as the reason | Session 13:04 and 13:22; run times in the README | AI assistant, no separate approval |
| 48 | 5 Nov 13:07, 13:37 | Commit the work to the repo as it goes, under `advaith334` | "feel free to commit to the repo"; "also commit with advaith334" | Commits from `c2d236f` on | Advaith |
| 49 | 5 Nov 13:12 | Move Llama to DeepInfra and Cloudflare for all follow-ups. Turn thinking off for Qwen and the judge in MemSyco-Bench | Novita stopped serving Llama. The benchmark runs with thinking off, and the judge ran out of tokens with it on | `config/models.yaml`; session 13:13 | AI assistant, no separate approval; reported at 13:13 |
| 50 | 5 Nov 13:12 | MemSyco-Bench: 100 seeded items, one answer each, DeepSeek V4 Flash as judge | The benchmark's own rubric and judge model. Every round 5 score therefore comes from an AI | `config/memsyco_bench.yaml` | AI assistant proposed, Advaith approved (button, row 39) |
| 51 | 5 Nov 13:22 | Keep all 48 items in the follow-ups, and report with and without `lt_most_islands` | The audit found no wrong key, and this keeps rounds comparable | `report/item_audit/audit.md`; session 13:22 | AI assistant, no separate approval. Final call rests with the checkers (row 41) |
| 52 | 5 Nov 13:28 | Run three add-ons: the label on true memories, the wrapper test, and local Nemo base vs instruct | Dr Filippov raised wrapper text and the base model. The label had never been tested on true memories | "Approve all three" (button). Paid caps $0.10 each; local run free. Commit `8f15b2f` | Dr Filippov raised two of the three; AI assistant proposed, Advaith approved (button) |
| 53 | 5 Nov 13:33–13:34 | **Frame the work in two parts:** show the problem, then test fixes. Harness fixes only, with model training as a named next step | Advaith cited cost. The assistant added the three days left and the training items MS1 would need | "Do you think the work that we do here should be 2 part?"; session 13:34 | Advaith proposed the two parts; AI assistant proposed leaving training out. He then approved the fixes (row 55) |
| 54 | 5 Nov 13:35–13:38 | Use teachers and AI tutors as the societal case | "Come up with stronger societal element"; "Choose an appropriate approach" | `report/societal/practice_case.md`; session 13:36–13:38 | Advaith set the direction; AI assistant chose the case |
| 55 | 5 Nov 13:40 | Run the tutor frame and three harness fixes, cap $0.15 | Part 2 of the report | "Approve the batch" (button). Commit `b73980a` | AI assistant proposed, Advaith approved (button) |
| 56 | 5 Nov 13:42 | Research ten societal options before settling | "give me 10 potential options after doing deep research" | `reports/`, `research_notes/`; five researchers and one writer | Advaith |
| 57 | 5 Nov 14:09 | Run the tutor split and weak evidence, cap $0.10 | The tutor frame changed three things at once. The feedback asked for weaker evidence, not built on 27 Oct | "Yes, run both" (button). Commit `16b1bbe` | Dr Filippov advised weak evidence; AI assistant proposed, Advaith approved (button) |
| 58 | 5 Nov 14:27 | Run the patient frame and wrong-source test, cap $0.05 | Tie-break between teachers and patients as the lead | "Yes, run them" (button). Commit `255d42c` | AI assistant proposed, Advaith approved (button) |
| 59 | 5 Nov 14:38–14:41 | **Lead the societal section with teachers, with patients as the contrast: one concept through two practices.** This sets aside the ten-option ranking, which put patients first by one point | The patient frame behaved like the tutor frame, which was the agreed tie-break | Session 14:38 and 14:41. The assistant asked "Use this as the plan for the societal section?" **The record shows no answer.** The report draft followed the plan from 15:10 | AI assistant proposed; no recorded approval |
| 60 | 5 Nov 14:40–14:41 | Commit everything and merge to `main` | "Commit everything to the repo"; "also go ahead and merge to main" | `main` moved to `b2474c1` | Advaith |
| 61 | 5 Nov 14:43–15:09 | Push `0337e38` and `f9a22b9` to `main` as well | Not requested. The assistant disclosed it at 15:22 | Session 15:22 | AI assistant, no approval; reported afterwards |
| 62 | 5 Nov 15:04 | Make a short visual PDF | "create a visual PDF describing everything that you did" | `report/visual_summary/` | Advaith |
| 63 | 5 Nov 15:09 | Fix the parser for answers like "C, Silicon", and rebuild the reports | These counted as unreadable. Local base went to 21% → 71% and instruct to 16% → 64%. Conclusions unchanged | Commit `f9a22b9`; session 15:09 and 15:11 | AI assistant, no separate approval; reported at 15:09 |
| 64 | 5 Nov 15:10 | Correct the README and write a first full report draft | Report due 8 Nov | `README.md`, `report/draft/`; session 15:10 | Advaith set the direction at 12:59 ("a lot of work done for this report"); AI assistant chose the jobs |
| 65 | 5 Nov 15:22 | Stop the Notion update and save the corrected text instead | The connection pointed at another workspace, so nothing was written. The live page still says "four of six models are unaffected" | `report/notion_update.md`; session 15:22 | AI assistant, reported afterwards. Applying it is still open |
| 66 | 5 Nov 15:40–15:41 | Merge to `main`, then address every weak part identified | "Merge to main" (button); "Can you please address all the weak parts that you identified" | `main` at `f81a92b`; session 15:41–15:43 | Merge: AI assistant proposed, Advaith approved (button). Weak parts: Advaith, with the split into free fixes and a new run by the AI assistant |
| 67 | 5 Nov 15:44 | **Pre-registered confirmatory run on 120 MMLU items**, cap $1.25 | Answers AI-written items, the post-hoc design and the reliance on Nemo | "Approve the run" (button). `report/preregistration.md`; commits `f6ab22b`, `baa6e14`, `04486fc`. Result pending when this row was written | AI assistant proposed, Advaith approved (button). Update with outcome |
| 68 | 5 Nov, after 15:42 | Fix item metadata without touching what models saw: 9 sources, 2 split URLs, and the label on `lt_letter_states`. The beliefs now read 42 assert, 6 deny. No `status` or `verified_by` set | The item audit's list. The 5 weak sources were left for the checkers | `report/item_audit/check_unchanged.py`: 196 items, 0 text differences; the analysis subgroup table was rebuilt to match | Advaith asked for the weak parts to be fixed (row 66); AI assistant chose the edits, no separate approval. **No human has checked the new sources** |
| 69 | 5 Nov, after 15:42 | Scoring pack: 148 rows to check, and 60 + 40 blinded replies. The 60 are 40 main and 20 follow-up, 4 of them from MemSyco-Bench, and lean toward wrong answers so that kappa means something. The 48 deliberately false passages are left out of the check sheet | Keep the human work to about two hours a person | `report/human_pack/` | Advaith asked for the weak parts to be fixed (row 66); AI assistant chose the design, no separate approval. The team can change it before scoring starts |
| 70 | 5 Nov 16:06 | **Raise the confirmatory cap from $1.25 to $1.55** and run with more parallel requests | Projected cost had risen to about $1.45 because Qwen3.5-9B reasons at length, so two parts would have stopped early. Turning Qwen's thinking off was rejected because it changes what H6 tests | "Yes, raise to $1.55" (button). `report/preregistration.md`, Stopping and spend | AI assistant proposed, Advaith approved |

### Still open: team to complete

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 41 | [TEAM TO COMPLETE] | Which two members verify all 52 items, and when. None verified so far | MS1 promise | Sheet ready in `report/human_pack/item_check.csv` | [TEAM TO COMPLETE] |
| 42 | [TEAM TO COMPLETE] | Who double-scores the sample, and how kappa is reported | MS1 promise, feedback | Sheets and guide ready in `report/human_pack/` (row 69) | [TEAM TO COMPLETE] |
| 43 | [TEAM TO COMPLETE] | Whether the team reviewed and accepted the move to long-tail items and no evidence | Consequential change | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |
| 44 | [TEAM TO COMPLETE] | Whether to rebalance beliefs (42 assert, 6 deny, after the relabel in row 68), or report it as a limitation | MS1 said half and half | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |
| 45 | [TEAM TO COMPLETE] | Follow-up on the conflict-of-interest point about the Bensal/"Bansal" work, assigned to Advaith on 7 Oct | Feedback note | The literature agent reported on 5 Nov: all four Bensal authors work at Writer, Inc., which now sells a memory product, and neither version has a competing-interest statement. See `report/literature/review.md`. How the report uses it is still open | [TEAM TO COMPLETE] |
| 46 | [TEAM TO COMPLETE] | Any decisions made in team meetings, messages or documents outside this session | Not visible to this audit | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |

## Gaps in this log

- The session log covers Advaith's Claude Code session only, from 27 Oct onward. Rows 47–69 were checked against it up to about 15:58 on 5 Nov.
- Rows after row 40 were written by an AI agent working from the same log, not by anyone who took part in the decisions.
- The assistant's own reasoning is not fully recorded, so the reasons above come from what it said to Advaith.
- Rows 20 and 25 have no recorded reason, and no reason has been supplied here.
