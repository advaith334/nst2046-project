# MS1 plan vs what was delivered

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026 from the MS1 report, Dr Filippov's feedback note, the session log and the run files. Needs a human check.

"Who approved" uses the same rule as the decision log. "(button)" means Advaith clicked a reply written by the AI assistant. No row shows team sign-off, because the record contains none: add it with evidence if it happened.

## The deviations that matter most

| Priority | Deviation | Why it matters |
|---|---|---|
| 1 | No evidence passages in the main study | MS1 defines factual sycophancy as agreement with a false belief "despite the available evidence". Without evidence, the main study tests memory against what the model already knows |
| 2 | No human item verification or scoring | MS1 promised two members for both. Nothing has been done |
| 3 | No logic items, and a new "general" category | The main study is not the planned case mix |
| 4 | No base model | MS1 and the feedback both named this contrast |
| 5 | Beliefs not balanced | 43 assert, 5 deny; MS1 said half and half |

## Full table

### Models

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| 12–16 models | 6 in the main study, 7 across all rounds | Dr Filippov advised 4–6 contrasting models on 7 Oct | Dr Filippov advised; AI assistant proposed the six; Advaith approved (button) |
| Base and instruction-tuned models | Instruction-tuned only | OpenRouter lists no base model. Choosing OpenRouter only (Ollama was offered) made this follow. A local server was never tried | Advaith chose OpenRouter only (AI recommended). Nobody decided to drop the base model: it is listed as a limitation |
| Candidates: Qwen, GLM, Kimi, Llama, Gemma; OpenAI, Anthropic, Google APIs | Qwen, Llama, Gemma, Anthropic, **plus Mistral, which MS1 never named**. No GLM, Kimi or OpenAI | Mistral came in as small open models for round 2b. Nemo then produced the main result. `gpt-terra` left the set with no recorded reason | AI assistant proposed; Advaith approved (button). Removal of GPT: no separate approval |
| Same generation settings where supported | Same except Claude (temperature unsupported) and Qwen3.5-9B (8000 tokens) | Claude ignores temperature; Qwen ran out of tokens | AI assistant, no separate approval; disclosed in README |
| Qwen3.5-397B not specifically planned; used in rounds 1–3 | Dropped from main study | Would exceed remaining credit; near ceiling | AI assistant proposed; Advaith approved (button) |

### Test set

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| 12 shared cases | 48 in the main study; 85 factual items across all rounds | Feedback advised 40–60 | Dr Filippov advised; AI assistant proposed 48; Advaith approved (button) |
| 4 each: numerical, logical, scientific | 20 science, 20 general knowledge, 8 numerical, **0 logic** | **No reason recorded.** Logic items were tried in rounds 1–2 and showed no clear memory effect, then dropped when items changed to long-tail facts | No explicit decision. First flagged by the AI assistant on 5 Nov |
| Each case has supporting evidence; memory supplied "alongside the question and evidence" | **None of the 48 main items has evidence** | Rounds 1–2 hit ceiling, and removing evidence made little difference. Feedback said "weaker or ambiguous" evidence, not none, and weak evidence was not built as a distinct arm | AI assistant proposed; Advaith approved (button, 27 Oct). Not called a deviation until 5 Nov. Evidence rerun approved 5 Nov, result pending |
| Half true, half false statements | 43 assert something false, 5 deny something true | Not addressed when items were expanded; flagged in the README | No decision recorded. Rebalancing is on the README to-do list |
| Two members check every case; science verified against reliable sources | **Not done.** All 52 items are `draft`; 9 long-tail items list no source | Items were AI-drafted and used before checking | Not approved by anyone: an open promise. [TEAM TO COMPLETE] |
| Items written or reviewed by the team | 87 of 89 items AI-drafted | Speed | Advaith approved the runs; team review not shown |

### Procedure

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| 2 pilot cases across all models, then 12 cases | Four rounds: pilot, harder items, long-tail, main | Feedback: "run before refining". Each round's result set the next | Dr Filippov advised; AI assistant proposed each step; Advaith approved |
| Fixed design set in advance | **Item type and susceptible model chosen after seeing results.** 24 of 48 main items reused from the screen | Needed to find an effect. On the 24 new items Nemo still moves 8% → 52% | AI assistant proposed; Advaith approved. Not stated as a limitation in the README |
| Six conditions | Six conditions kept for main study. Rounds 2–3 used two | Screening only | AI assistant proposed; Advaith approved |
| Each case and condition run twice | Done in rounds 1, 3 and 4; one rep in round 2 | Cost, in a screening round | AI assistant, shown in the estimate |
| 1,728 main responses + 192 checks | 3,456 main + 96 checks in round 4; 5,472 trials overall | More items, fewer models | Follows from the rows above |
| Fresh requests, randomised order | Done, and option order also shuffled | Feedback | Delivered |
| Harness with label switched on only for the labelled condition | Done; test checks the prompts differ by the prefix alone | | Delivered |
| Browsing, tools and automatic memory disabled | Done in the request; `transforms` empty | | Delivered |
| Fallback: subject area of the prompt | Not needed | Effect found | n/a |
| Optional open-weight training | Not done | Not needed | No decision recorded |

### Scoring and analysis

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| Two members blind-score every response; feedback narrowed this to a sample with reported agreement | **Not done.** Automatic letter scoring only. Rating sheet and kappa tool exist | Not started. Teammates cannot generate a sheet without the trial logs, which are not in git | Open promise. [TEAM TO COMPLETE] |
| Assess explanations, contradictions, uncertainty | Not done by humans. AI-coded analysis started 5 Nov | Depends on the row above | AI output must be labelled as such |
| Answer-option probabilities | Partial: none for Claude, 4% for Llama, 52% for Mistral Small | Hosts differ. Probabilities also reflect the first answer line | AI assistant, no separate approval; disclosed |
| Report usable counts and uncertainty | Done: Wilson CIs, exact McNemar, usable counts | | Delivered. Bonferroni added afterwards, not planned in advance |
| Compare stored vs current, and labelling | Done | | Delivered |
| Success: lower acceptance with no fall in useful recall | Met for Nemo on automatic scoring. 1 Qwen3.5-9B check unreadable. Checks are easy and n is small | | Delivered, with limits stated in README |

### Logging and AI use

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| Log prompt, model and version, toggle state, raw response | Done, but "version" is only a slug; **logs are not in the repo** | OpenRouter gives no snapshot. Logs were excluded for size | Exclusion: AI assistant proposed; Advaith approved (button) |
| Tools: ChatGPT, Exa, "similar tools" for research; Claude Code and Codex for the build | Claude Code for nearly everything; Firecrawl on 5 Nov. No Exa or Codex in the record | Single-tool session | Advaith |
| Important outputs checked; final runs from the harness, not a chat model | Runs came from the harness. Most checks were AI-on-AI | See AI-use log | Open issue |
| Disclosure of AI-generated work | **Not in README or git.** Co-author line removed at Advaith's request | He did not want it shown | Advaith. Must be disclosed in the report's AI-use log |

### Roles (MS1 plan only)

| Planned (MS1) | What the repo and session show | Why | Who approved |
|---|---|---|---|
| Advaith: systems. Aditya: ideas and research direction. Elkan: evaluation. Tony: run the multi-model tests | Every commit is under Advaith's account. Every run used his session, machine and OpenRouter account. Other members do not appear in the record. **This does not show they did nothing; it shows the record is silent** | Unknown | [TEAM TO COMPLETE]. The README still lists "Tony (runs)": correct it if it no longer holds |

### Feedback items still open

| Feedback (7 Oct) | Status |
|---|---|
| Base vs instruction-tuned pair | Not done |
| Weaker or ambiguous evidence | Evidence rerun approved 5 Nov, pending |
| Double-score a sample and report agreement | Tool built, not done |
| Look into the Bensal/"Bansal" vendor conflict of interest (assigned to Advaith) | Passed to the literature agent 5 Nov, pending |
| Fricker's work on testimonial justice (Dr Filippov to share) | Passed to the societal agent 5 Nov, pending |
| Start the minimal experiment "this week" | Ran 27 Oct, 20 days later |
