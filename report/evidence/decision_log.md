# Decision log

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026 from the session log and git history. **Advaith must check every row before submission, and the team must complete the blank rows.**

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
| 14 | 27 Oct 16:07 | Test evidence by removing it entirely as well as as-written. **Weaker evidence was not built** | Simple to test | `evidence_modes: [as_written, none]`. Feedback said "weaker or ambiguous" | AI assistant, within the approval above |
| 15 | 27 Oct 16:29 | Read the last "Answer:" line, not the first, and re-score earlier runs | Claude wrote "Answer: D", then corrected to B, and was counted as accepting the false belief | Session 16:29; `cal_num_digit_ones` | AI assistant, no separate approval; reported at 16:30 |
| 16 | 27 Oct 16:46 | **Move to long-tail facts, and add 2–3 small open models** | Frontier models stayed at ceiling; Llama's shifts looked like noise. The assistant offered this or "commit and write up" | `runs/calibration-20261027/`; session 16:30 | AI assistant proposed, Advaith approved (button, including the model names) |
| 17 | 27 Oct 16:46 | Add a $1 limit and an estimate before running this screen | Budget control. Part of the button text Advaith accepted | Session 16:46 | AI assistant proposed, Advaith approved (button) |
| 18 | 27 Oct 16:49 | Give Qwen3.5-9B 8000 tokens | Ran out mid-reasoning at 2000 | Small-model smoke test; `config/models.yaml` | AI assistant, no separate approval; reported at 16:50 |
| 19 | 27 Oct 16:50 | **Drop evidence passages for long-tail items.** This is a deviation from MS1 | So the answer depends on what the model knows. Removing evidence had shown little difference in round 2 | `longtail.yaml` header; the estimate at 16:50 says "no evidence". Approved at 16:51 (button). **It was not called a deviation until 5 Nov** | AI assistant proposed, Advaith approved (button) |
| 20 | 27 Oct 16:50 | **Logic items dropped.** Long-tail items are science, general knowledge and numerical only | **No reason is recorded.** Logic items in rounds 1–2 showed no clear memory effect, and long-tail facts are not logic problems, but the session never states this as the reason | No explicit decision in the session. The 17:43 main plan lists the categories. First flagged 5 Nov 12:56 | AI assistant, no separate approval. Advaith approved plans listing the categories; the session does not show he was asked about logic |

### Main study

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 21 | 27 Oct 17:39 | Expand to 48 items, all six conditions plus useful-memory checks, 2 reps | First clear effect (Nemo 19% → 60%). 40–60 items came from the feedback | `runs/longtail-20261027/`; session 17:35 | AI assistant proposed, Advaith approved (button) |
| 22 | 27 Oct 17:43 | **Reduce 12–16 models to 6:** Nemo, Mistral Small, Llama, Gemma 4, Qwen3.5-9B, Claude Sonnet 5.5 | Feedback asked for 4–6 contrasting models. Round 3 identified Nemo as susceptible | Session 17:43; `config/main.yaml` | Dr Filippov advised 4–6; AI assistant proposed the six, Advaith approved (button) |
| 23 | 27 Oct 17:43 | **Exclude Qwen3.5-397B from the main study** | Would add about $1.50, past the $2.73 credit left. "Matched Claude at ceiling": roughly true, but round 3 was 2% → 4% | Session 17:43; `runs/longtail-20261027/summary.csv` | AI assistant proposed, Advaith approved (button) |
| 24 | 27 Oct 17:43 | Keep Sonnet, not Haiku | The assistant offered Haiku as a $0.40 option with a weaker frontier contrast | Session 17:43 | AI assistant proposed both, Advaith chose Sonnet (button) |
| 25 | 27 Oct, by 17:45 | **No OpenAI model.** `gpt-terra` left the main set without comment | **No reason is recorded** | `config/models.yaml` in `c89f2c1` vs `9e374ef` | AI assistant, no separate approval |
| 26 | 27 Oct 14:25, carried through 17:43 | **No base model.** OpenRouter lists none, and a local server was never tried | Consequence of #3. Noted as a limitation, not chosen as a design | Catalogue check 14:25; first `config/models.yaml`; session 17:43 | Advaith chose OpenRouter only (#3). The assistant recorded the consequence. No one decided to attempt or abandon a local run: [TEAM TO COMPLETE] |
| 27 | 27 Oct 17:45 | Commit first so the run points to exact code, then run with a $1.95 cap | The record ties to a commit | Commit `9e374ef`; clean manifest | AI assistant proposed, Advaith approved (button) |
| 28 | 27 Oct 20:40 | Check the run; keep the Mac awake | Run looked stuck. Mac had slept 17:50–20:09 | "What is going on? Please make sure that the process is alive."; session 20:40 | Advaith asked; AI assistant acted |
| 29 | 27 Oct 21:31 | Retry 239 failed rows within the cap | Sleep and rate-limit errors | Session 21:31–21:42 | AI assistant, no separate approval. Within the cap Advaith set |

### Analysis and reporting

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 30 | 27 Oct 17:41 | Add exact McNemar paired tests | To answer the label and stored-vs-stated questions directly | `report.py`; session 17:41 | AI assistant; part of the plan approved at 17:45 |
| 31 | 27 Oct 21:43 | **Use Bonferroni across 42 tests as a caveat.** Only Nemo's and Mistral Small's stored-belief results "hold" | 42 comparisons | Session 21:43; README section 5. Not pre-registered. Not implemented in code. 2 reps are treated as independent | AI assistant, no separate approval. Holm and item-level methods were commissioned on 5 Nov: results pending |
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
| 39 | 5 Nov 13:04 | Approve two more paid runs: evidence rerun and MemSyco-Bench, about $0.76, cap $1.25 | Evidence rerun addresses #19; the benchmark gives an external check | "Approve both runs" (button). Commit `c2d236f`. **Results not seen by this audit** | AI assistant proposed, Advaith approved (button). Update with outcome |
| 40 | 5 Nov 13:00 | Use six AI subagents for statistics, qualitative coding, item audit, literature, societal analysis and evidence trail | "spawn subagents and get a lot of work done" | Session 12:59–13:02 | Advaith set the direction; AI assistant chose the workstreams |

### Still open: team to complete

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 41 | [TEAM TO COMPLETE] | Which two members verify all 52 items, and when. None verified so far | MS1 promise | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |
| 42 | [TEAM TO COMPLETE] | Who double-scores which sample, and how kappa is reported | MS1 promise, feedback | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |
| 43 | [TEAM TO COMPLETE] | Whether the team reviewed and accepted the move to long-tail items and no evidence | Consequential change | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |
| 44 | [TEAM TO COMPLETE] | Whether to rebalance beliefs (43 assert, 5 deny), or report it as a limitation | MS1 said half and half | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |
| 45 | [TEAM TO COMPLETE] | Follow-up on the conflict-of-interest point about the Bensal/"Bansal" work, assigned to Advaith on 7 Oct | Feedback note | Passed to the literature agent on 5 Nov: result pending | [TEAM TO COMPLETE] |
| 46 | [TEAM TO COMPLETE] | Any decisions made in team meetings, messages or documents outside this session | Not visible to this audit | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |

### Frontier tests (branch `aditya/work`)

From Aditya's Claude Code session of 5 Nov, not Advaith's. Nothing has been run yet.

| # | Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|---|
| 47 | 5 Nov | Test whether frontier models' robustness is real or specific to test-shaped prompts | "my initial hypo is that the issue right now is that the models are benchmaxxed on the evals that we are running" | `frontier/README.md` | Aditya |
| 48 | 5 Nov | Build frontier tests F1 (headroom), F2 (test awareness), F3 (silent accommodation) and F4 (pressure). Not built: test-shaped vs natural multiple choice, and public vs paraphrased benchmark items | "build tests 1, 4 5 and 6" | Branch `aditya/work` | AI assistant proposed six tests; Aditya chose four |
| 49 | 5 Nov | Headroom items are computed (arithmetic, calendar, primes, letter counts), asked with reasoning off | Frontier models were at ceiling on long-tail facts; computed keys are certain | `frontier/scripts/build_headroom.py`; all 64 keys re-checked by independent code, 0 mismatches | AI assistant, no separate approval |
| 50 | 5 Nov | Fix the item-selection rule, primary scope, outcomes and a predictions table before running | The audits criticise choices made after seeing data | `frontier/README.md`, "Rules fixed in advance" | AI assistant proposed. Predictions: Aditya to fill in before running |
| 51 | 5 Nov | Keep the frontier tests in their own folder, model registry, prompts and tests, apart from the main study | "have it be the case so we can have a clear view of this" | `frontier/README.md`, "Where everything is"; main `config/`, `data/cases/` and prompts unchanged | Aditya |
| 52 | 5 Nov | Run every frontier test on nine models: Claude Opus 5.5, Claude Haiku 5.5, GPT-6.1 Terra and Gemini 4 Argon (reasoning off), plus the five open models with their exact main-study settings. Generation settings match the main study. Only the four frontier models decide F1's item selection. Claude Sonnet 5.5 and GPT-6.1 Sol dropped | "opus would be the frontier, then haiku terra, argon nemo and the 5 cheap open models"; results must "immediately be aligned with the remaining results" | `frontier/config/models.yaml`; `tests/test_frontier.py` checks the open models match `config/models.yaml` | Aditya chose the models; AI assistant proposed matching settings and the selection change. Set before any run |
| 53 | 5 Nov | Write up the unbuilt tests as specs: F5 (test-shaped vs natural prompts), F6 (public vs reworded benchmark items), F7 (frontier models on the main study's items). Not built | "for the missing tests you haven't built yet, just write the structure ... so there aren't gaps" | `frontier/planned/` | Aditya asked; AI assistant wrote the specs. Open choices: F6's benchmark (row 37 rejected SycophancyEval) and F7's reasoning setting |
| 54 | 5 Nov | Replace Claude Opus 5.5 with Claude Sonnet 5.5 in the frontier set, using the main study's exact Sonnet spec (reasoning at its default). Haiku, Terra and Argon keep reasoning off | "replace opus 5.5 with sonnet 5.5 with reasoning exactly like the tests" | `frontier/config/models.yaml`; a test checks Sonnet matches `config/models.yaml` | Aditya. Read by the AI assistant as "as in the main study"; Sonnet's F1 results are therefore not strictly comparable with the `-fast` models. Set before any run |
| 55 | 5 Nov | All four frontier models run with reasoning at the host's default (no reasoning-off setting). Haiku, Terra and Argon renamed `claude-haiku`, `gpt-terra-openai`, `gemini-argon`; Terra and Argon get 8,000 tokens in case they reason | "have all the frontier models have their reasoning on default" | `frontier/config/models.yaml`; a test checks no frontier model sets reasoning | Aditya. Token limit: AI assistant, following the main study's Qwen precedent. Reverses the reasoning-off part of rows 49 and 54. Set before any run |
| 56 | 5 Nov | Split F1–F4 into two separately run tracks with identical items, prompts and settings: A, frontier models (Claude Sonnet 5.5, Claude Haiku 5.5, GPT-6.1 Terra, Gemini 4 Argon); B, the main study's six models (`main` set) with their exact settings. Track A's screen picks the F1 items for both; each track is analysed against its own screen. Sonnet runs in both | "i want it to be a frontier model test and a test that uses the same models as the original tests" | `frontier/config/*_frontier.yaml`, `*_main.yaml`; a test checks each pair differs only in models | Aditya asked for the split; the AI assistant proposed the shared items and keeping Sonnet in both. Set before any run |
| 57 | 6 Nov | GPT-6.1 Terra runs without token probabilities (`logprobs: false`, a new per-model opt-out in `client.py`) | Smoke test: OpenAI returns "logprobs are not supported with reasoning models" | `frontier/runs/frontier-smoke` | AI assistant, from the smoke test. No main-study model changes |
| 58 | 6 Nov | Claude Sonnet gets 8,000 tokens in the frontier tests (2,000 in the main study) | Smoke test: it reasoned for all 2,000 tokens on `fh_primecount_7` and gave no answer (1 of 5; 0 of 592 in the main study). The README's step 0 rule, set before running, says to raise the limit | `frontier/runs/mainmodels-smoke` | AI assistant, applying the pre-set rule. Changes only replies that would be cut off |
| 59 | 6 Nov | Cut cost to about $9: track A is Claude Haiku 5.5 and GPT-6.1 Terra; Claude Sonnet runs once, in track B, and counts for both (shared items, prompts, settings, seed); Gemini 4 Argon dropped. F1 items are picked by Sonnet, Haiku and Terra across both screens | Aditya: "i dont have enough money to run the frontier tests at the prices you've estimated"; chose the ~$9 option of four offered | `frontier/config/models.yaml` (`frontier_models`, `selection`) | Aditya chose; AI assistant proposed the options. Before any stage B run; track B's screen was already running |
| 60 | 6 Nov | Keep Qwen3.5-9B at its main-study 8,000 tokens in track B, although it ran out of tokens on 67 of 192 screen answers (15 of 592 in the main study). This overrides the README's step 0 rule for Qwen, to keep track B identical to the main study | Aditya chose this over raising the limit to 16,000 and redoing its screen (~$0.50) | `frontier/runs/mainmodels-screen-20261106` | Aditya. Qwen's F1–F4 results will rest on fewer usable answers; report its unparseable rate beside them. Before any stage B run |

## Gaps in this log

- The session log covers Advaith's Claude Code session only, from 27 Oct onward.
- The assistant's own reasoning is not fully recorded, so the reasons above come from what it said to Advaith.
- Rows 20 and 25 have no recorded reason, and no reason has been supplied here.
