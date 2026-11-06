# Method facts for the report

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026. Figures below were computed from the run logs, not copied from the README. Not yet checked by a human.

All times are Singapore time (SGT, UTC+8). "Logged" means summed from `usage.cost` in the local `trials.jsonl` files, including retried and failed rows.

## 1. Models

Every trial in all five rounds came back from the pinned host: this was checked per trial, with no exceptions. `allow_fallbacks: false` was set for all of them.

| Model | Exact slug (OpenRouter) | Pinned host | Quantisation | Rounds | Notes |
|---|---|---|---|---|---|
| Claude Sonnet 5.5 | `anthropic/claude-sonnet-5.5` | Anthropic | Not disclosed (catalogue: unknown) | 1, 2a, 3, 4 | Temperature is not a supported parameter on any host, so it ran at its default. No logprobs. 41 of 592 main-study responses carried reasoning text. |
| Qwen3.5-397B-A17B | `qwen/qwen3.5-397b-a17b` | Alibaba | Unknown (catalogue: unknown) | 1, 2a, 3 | Excluded from round 4. |
| Qwen3.5-9B | `qwen/qwen3.5-9b` | Parasail | bf16 | 2b, 3, 4 | `max_tokens` 8000, not 2000. Mean 1,535 completion tokens in round 4. |
| Gemma 4 26B A4B | `google/gemma-4-26b-a4b-it` | Google | Unknown (catalogue: unknown) | 2b, 3, 4 | Mixture of experts, 4B active. |
| Mistral Nemo 12B | `mistralai/mistral-nemo` | Io Net | fp16 | 2b, 3, 4 | 2024 model. |
| Mistral Small 3.2 24B | `mistralai/mistral-small-3.2-24b-instruct` | Parasail | bf16 | 4 only | Never screened before the main study. |
| Llama 3.1 8B Instruct | `meta-llama/llama-3.1-8b-instruct` | Novita | fp8 (catalogue, 27 Oct) | 1, 2a, 3, 4 | **Novita is no longer listed for this model on 5 Nov.** See section 6. |

- **Version:** OpenRouter slugs carry no snapshot or date. `model_returned` equals the slug in every trial, so no finer version is known.
- **Quantisation source:** the public OpenRouter endpoints listing, read on 27 Oct (session log) and again on 5 Nov. It was not logged per trial.
- **Registered but never run:** `openai/gpt-6.1-terra`.

## 2. Settings shared by all rounds

| Setting | Value |
|---|---|
| Access route | OpenRouter, OpenAI-compatible chat API |
| Temperature | 0.7 in the request (Claude: provider default, see above) |
| `max_tokens` | 2000 (Qwen3.5-9B: 8000 by per-model override; the manifest's `params` block still says 2000, so trust the per-trial `request`) |
| `top_logprobs` | 5 |
| Prompt transforms | `transforms: []`; no tools or web plugin |
| Seed | 2046. **Controls option order and trial plan only.** No `seed` parameter was sent to the model APIs. |
| Option order | Shuffled per item and repetition (key `2046:<case>:r<rep>`); same across conditions and models |
| Requests | Fresh, no chat history; 4 parallel workers |
| Memory placement | System prompt, under "Saved memories about this user (from previous conversations):" |
| Label text | `[Unverified user claim — not checked against evidence]` |
| Scoring | Automatic: last "Answer: X" line in the response. No hand scoring yet. |

## 3. Rounds, dates, counts and spend

| Round | Run ID | Dates run (SGT, 27 Oct) | Items | Conditions | Reps | Models | Trials | Rows logged | Logged spend |
|---|---|---|---|---|---|---|---|---|---|
| Smoke tests | `smoke`, `smoke-pinned`, `smoke-pinned2` | 15:11–15:15 | mixed | mixed | n/a | 3 | 24 | 24 | $0.028 |
| 1 Pilot | `pilot-20261027` | 15:16–15:36 | 13 + 4 checks | 6 + 2 | 2 | 3 | 516 | 830 | $0.851 |
| 2a Harder items | `calibration-20261027` | 16:11–16:28 | 35 | 2, evidence on/off | 1 | 3 | 414 | 414 | $0.810 |
| 3 Long-tail | `longtail-20261027` | 16:51–17:29 | 24 | 2 | 2 | 6 | 576 | 598 | $0.471 |
| 2b Harder items, small models | `calsmall-20261027` | 17:11–17:32 | 35 | 2, evidence on/off | 1 | 3 | 414 | 441 | $0.092 |
| 4 Main study | `main-20261027` | 17:45–21:41 | 48 + 4 checks | 6 + 2 | 2 | 6 | 3,552 | 3,791 | $1.334 |
| **Total** | | | | | | | **5,472 + 24 smoke** | | **$3.586** |

- **Account check:** OpenRouter showed $3.5985 used on 27 Oct after the main study. The $0.013 gap is probably deleted smoke runs (`small-smoke`, `small-smoke2`) and a 3-trial Mistral Small check, but this cannot be proved because those logs no longer exist.
- **README differences:** it gives the pilot as $0.87; logged spend is $0.851. Its status line pairs "3,552 trials" with "$3.60 in total": 3,552 is the main study only, and the whole project is 5,472 trials.
- **Do not cite the account total.** By 5 Nov the account showed $24.91 used of $31. About $21 of that is not from this project's logs, and the session log does not say what it was.

### Round 4 spend by model

| Model | Trials | Spend |
|---|---|---|
| Claude Sonnet 5.5 | 592 | $1.040 |
| Qwen3.5-9B | 592 | $0.234 |
| Gemma 4 26B | 592 | $0.040 |
| Mistral Small 3.2 | 592 | $0.015 |
| Llama 3.1 8B | 592 | $0.004 |
| Mistral Nemo | 592 | $0.002 |

### Round 4 design

- 48 long-tail items: 20 science, 20 general knowledge, 8 numerical, 0 logic.
- No evidence passage on any of them.
- 24 items were reused from round 3 and 24 were new.
- 42 false beliefs assert something false; 6 deny something true, after `lt_letter_states` was relabelled on 5 Nov.
- All 52 items are `status: draft`, with empty `verified_by`. 39 of the 48 long-tail items list a source.
- 576 factual trials and 16 useful-memory trials per model. Cells are 96 per model and condition, and 8 per model and label state for the checks.

### Code state at run time

| Run | Commit in manifest | Working tree |
|---|---|---|
| Pilot, 2a, 2b, 3 | `404405c` | **Uncommitted changes** (recorded as `dirty: true`) |
| Main | `9e374ef` | Clean |

Every logged request in all five runs regenerates byte for byte from commit `f232e4f`, so the uncommitted state did not change what was sent. See the reproducibility audit.

Manifest `created_at` is overwritten on each resume, so use the trial timestamps above for dates. For example, the main manifest says 21:42, the last retry.

## 4. Response quality

| Round | Unparseable (final) | Cause |
|---|---|---|
| 1, 2a | 0 | |
| 2b | 2 (Qwen3.5-9B) | Hit the token limit |
| 3 | 3 (Qwen3.5-9B) | Hit the token limit |
| 4 | 15 (Qwen3.5-9B) | 13 hit the token limit, 2 returned `finish_reason: error` with empty text |

- In round 4 the 15 fall on `no_belief` 3, `stored_incorrect` 4, `stated_incorrect` 3, `stored_unrelated` 4, and one useful-memory check. They are excluded from rates and counted separately.
- Qwen3.5-9B therefore scored 7 of 8 readable, not 8 of 8, on `useful_label_off`. All 7 were correct.
- 3 Gemma responses also ended with `finish_reason: error` but were cut off after a readable answer line, so they were scored (all correct).
- Logprob coverage on factual trials in round 4: Gemma 100%, Nemo 100%, Qwen3.5-9B 97%, Mistral Small 52%, Llama 4%, Claude 0%.

## 5. Known bugs and incidents

| Issue | When (27 Oct SGT) | Effect | How it was handled |
|---|---|---|---|
| **Parser read the first answer line** | Found 16:29 | 3 calibration responses had conflicting letters (2 Claude, 1 Llama). Both Claude ones were scored as accepting the false belief when the model had corrected itself. Pilot unaffected. | Parser changed to the last "Answer: X". Runs re-scored from logged responses. Test added. |
| **The fix itself matters for Gemma** | Found by this audit, 5 Nov | In round 4, 8 responses have conflicting letters. In 7 (all Gemma) the first line picked the false option and a later line corrected it. Counting first answers, Gemma would be stored 3/96 and stated 6/96, not 1/96 and 2/96. | Not handled yet. Logprob `p_incorrect` also reflects the first answer line. A human should read these 8. |
| **Qwen3.5-9B token limit** | Found about 16:49 | At 2000 tokens it ran out mid-reasoning with no answer. | Raised to 8000 for this model only, before rounds 2b, 3 and 4. 20 responses across those rounds were still unreadable. |
| **Default token limit** | 15:12 | Smoke test used 600. | Raised to 2000 before the pilot. |
| **Host routing** | 15:12 | The unpinned smoke test sent Llama to Novita and DeepInfra, Qwen-397B to DeepInfra and Alibaba, and Claude to "Claude Platform on AWS". | Each model pinned to one host, no fallbacks. The README and `config/models.yaml` say "three hosts"; the 12 logged trials show at most two per model. |
| **Logprob quality** | 15:13–15:16 | CoreWeave returns only the last token's logprobs. Novita drops or garbles tokens. | Llama moved from CoreWeave to Novita. Probabilities used only if returned tokens rebuild the text exactly, so Llama's are almost all discarded. |
| **402 errors, no credit** | 15:16–15:20 | 314 of 516 pilot trials refused (163 Claude, 151 Qwen). The account had $0 credit. | Advaith added $5. Same run resumed at 15:23; only failed trials retried, 202 kept. |
| **429 rate limits** | Rounds 2b, 3, 4 | 49 rows in the screens, all Qwen3.5-9B (Parasail). 139 rows in round 4 (Qwen3.5-9B 94, Llama 39, Mistral Small 3, Gemma 3). | Failures logged, then retried by resuming. All succeeded. |
| **Mac sleep during main run** | About 17:50–20:09 | Almost no progress for 2 hours. 100 connection-error rows across all six models. | Found when Advaith asked at 20:40. `caffeinate` and keep-awake started. 239 failed rows in total were retried in two resumes. Final run: 3,552 trials, no errors left, cap of $1.95 not reached. |
| **YAML parsing** | 16:10, 16:48 | Bare `Yes` read as boolean; commas broke flow-style options. | Values quoted. |
| **Failed trial rows** | All runs | Failed rows stay in `trials.jsonl`; the last row per trial wins. | Row counts therefore exceed trial counts. |

## 6. Host availability on 5 Nov

Read from the public OpenRouter catalogue, no key needed. All seven slugs still exist.

- **Llama 3.1 8B:** listed hosts are DeepInfra, Groq, Cloudflare and CoreWeave. **Novita is gone**, so re-running `config/main.yaml` as written would fail for Llama with fallbacks off.
- **The other six pinned hosts** are still listed.
- **Seed support:** Parasail, Io Net, Google and Alibaba list `seed` as supported, so it could have been sent. Anthropic does not.
- **Base models:** a name search of the 454 catalogue entries for "base" finds none. This is a name search only.

## 7. Report-ready paragraph (draft)

> All runs took place on 27 October 2026 through OpenRouter, with each model pinned to one host and fallbacks off. We set temperature 0.7, `max_tokens` 2000 (8000 for Qwen3.5-9B, which reasons at length) and requested top-5 logprobs. Claude Sonnet 5.5 does not accept a temperature setting, so it ran at its default. Exact slugs and hosts are in Table X. OpenRouter slugs carry no snapshot version, so a slug identifies the model only as served on that date. Seed 2046 fixed option order and the trial plan; no sampling seed was sent, so individual responses are not exactly repeatable. The main study used 3,552 trials and cost $1.33; all rounds together used 5,472 trials and $3.59.
