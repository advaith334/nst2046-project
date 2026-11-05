# MS1 plan vs what was delivered

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026 from the MS1 report, Dr Filippov's feedback note, the session log and the run files, and updated the same day after the follow-up rounds. Needs a human check.

"Who approved" uses the same rule as the decision log. "(button)" means Advaith clicked a reply written by the AI assistant. No row shows team sign-off, because the record contains none: add it with evidence if it happened.

## The deviations that matter most

| Priority | Deviation | Why it matters |
|---|---|---|
| 1 | No evidence passages in the main study | MS1 defines factual sycophancy as agreement with a false belief "despite the available evidence". Without evidence, the main study tests memory against what the model already knows. Rounds 6–7 added evidence afterwards: Nemo +41 points with none, +17 with weak, +1 with strong |
| 2 | No human item verification or scoring | MS1 promised two members for both. Nothing has been done, though the sheets are ready in `report/human_pack/` |
| 3 | No logic items, and a new "general" category | The main study is not the planned case mix |
| 4 | Base model came late and only for Nemo | MS1 and the feedback both named this contrast. Round 14 ran one pair locally after the main study; the main study itself is instruction-tuned only |
| 5 | Beliefs not balanced | 42 assert, 6 deny after one label was corrected; MS1 said half and half |

## Full table

### Models

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| 12–16 models | 6 in the main study, 7 across rounds 1–4. Follow-ups used 5 of the 6, plus local Nemo base and instruct | Dr Filippov advised 4–6 contrasting models on 7 Oct | Dr Filippov advised; AI assistant proposed the six; Advaith approved (button) |
| Base and instruction-tuned models | **Done as a follow-up, not in the main study.** Round 14 ran Mistral Nemo 12B base and instruct locally at the same quantisation: 1,728 trials, free. One pair only | OpenRouter lists no base model, so the main study had to go without. The base model moved at least as much as the instruct model, which goes against MS1's explanation | Advaith chose OpenRouter only at first (AI recommended). Local pair: Dr Filippov raised it; AI assistant proposed; Advaith approved (button, 5 Nov 13:28) |
| Candidates: Qwen, GLM, Kimi, Llama, Gemma; OpenAI, Anthropic, Google APIs | Qwen, Llama, Gemma, Anthropic, **plus Mistral, which MS1 never named**. No GLM, Kimi or OpenAI. Follow-ups moved Llama to another host and left Claude out, as it stayed at 0% and costs most | Mistral came in as small open models for round 2b. Nemo then produced the main result. `gpt-terra` left the set with no recorded reason | AI assistant proposed; Advaith approved (button). Removal of GPT: no separate approval |
| Same generation settings where supported | Same except Claude (temperature unsupported) and Qwen3.5-9B (8000 tokens) | Claude ignores temperature; Qwen ran out of tokens | AI assistant, no separate approval; disclosed in README |
| Qwen3.5-397B not specifically planned; used in rounds 1–3 | Dropped from main study | Would exceed remaining credit; near ceiling | AI assistant proposed; Advaith approved (button) |

### Test set

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| 12 shared cases | 48 in the main study; 85 factual items across rounds 1–4; 100 MemSyco-Bench items in round 5 | Feedback advised 40–60 | Dr Filippov advised; AI assistant proposed 48; Advaith approved (button) |
| 4 each: numerical, logical, scientific | 20 science, 20 general knowledge, 8 numerical, **0 logic** | **No reason recorded.** Logic items were tried in rounds 1–2 and showed no clear memory effect, then dropped when items changed to long-tail facts | No explicit decision. First flagged by the AI assistant on 5 Nov |
| Each case has supporting evidence; memory supplied "alongside the question and evidence" | **None of the 48 main items has evidence** | Rounds 1–2 hit ceiling, and removing evidence made little difference. Feedback said "weaker or ambiguous" evidence, not none. **Added on 5 Nov as follow-ups:** the same 48 items with stating passages (round 6), weak passages (round 7) and false passages (round 8). All passages are AI-written and unverified | AI assistant proposed; Advaith approved (button, 27 Oct). Not called a deviation until 5 Nov. Rounds 6–8 approved 5 Nov (buttons) |
| Half true, half false statements | 42 assert something false, 6 deny something true, after `lt_letter_states` was relabelled on 5 Nov (labelled 43 and 5 when run) | Not addressed when items were expanded; flagged in the README | No decision recorded. Rebalancing is on the README to-do list |
| Two members check every case; science verified against reliable sources | **Not done.** All 52 items are `draft`. An AI pre-check found no wrong key. The 9 items with no source gained one on 5 Nov, from that audit. Sheet ready in `report/human_pack/` | Items were AI-drafted and used before checking | Not approved by anyone: an open promise. [TEAM TO COMPLETE] |
| Items written or reviewed by the team | 87 of 89 items AI-drafted | Speed | Advaith approved the runs; team review not shown |

### Procedure

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| 2 pilot cases across all models, then 12 cases | Four rounds: pilot, harder items, long-tail, main | Feedback: "run before refining". Each round's result set the next | Dr Filippov advised; AI assistant proposed each step; Advaith approved |
| Fixed design set in advance | **Item type and susceptible model chosen after seeing results.** 24 of 48 main items reused from the screen | Needed to find an effect. On the 24 new items Nemo still moves 8% → 52% | AI assistant proposed; Advaith approved. Not stated as a limitation in the README |
| Six conditions | Six conditions kept for main study. Rounds 2–3 used two | Screening only | AI assistant proposed; Advaith approved |
| Each case and condition run twice | Done in rounds 1, 3 and 4; one rep in round 2 | Cost, in a screening round | AI assistant, shown in the estimate |
| 1,728 main responses + 192 checks | 3,456 main + 96 checks in round 4; 5,472 trials in rounds 1–4; 20,068 overall | More items, fewer models, then ten follow-up rounds | Follows from the rows above |
| No external benchmark planned; MS1 cites MemSyco-Bench as prior work | **Added: round 5 ran 100 MemSyco-Bench items** on five open models, 2,000 trials, $0.47. Every score is from an AI judge, DeepSeek V4 Flash. All five models moved, so "some models are unaffected" holds only for our multiple-choice task | All our items were written for this project, so an outside check was needed. It tests a preference memory, not a belief, in free text, so it is not a like-for-like repeat | AI assistant proposed; Advaith approved (button, 5 Nov 13:04) |
| Label tested on false memories only | **Added:** label on true memories (round 9), wording tests (round 10), tutor and patient frames (rounds 11–12), three harness fixes (round 13) | Dr Filippov warned about wrapper text. The report's Part 2 needed fixes to test. All designed after the main results | AI assistant proposed; Advaith approved (buttons, 5 Nov) |
| Fresh requests, randomised order | Done, and option order also shuffled | Feedback | Delivered |
| Harness with label switched on only for the labelled condition | Done; test checks the prompts differ by the prefix alone | | Delivered |
| Browsing, tools and automatic memory disabled | Done in the request; `transforms` empty | | Delivered |
| Fallback: subject area of the prompt | Not needed | Effect found | n/a |
| Optional open-weight training | Not done | Not needed | No decision recorded |

### Scoring and analysis

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| Two members blind-score every response; feedback narrowed this to a sample with reported agreement | **Not done.** Automatic letter scoring only. A blinded sheet of 60 responses across the main study and follow-ups is ready, and needs no trial logs | Not started | Open promise. [TEAM TO COMPLETE] |
| Assess explanations, contradictions, uncertainty | Not done by humans. AI-coded analysis done 5 Nov, in one unblinded pass. 40 rows are ready for blinded double-scoring | Depends on the row above | AI output must be labelled as such |
| Answer-option probabilities | Partial: none for Claude, 4% for Llama, 52% for Mistral Small | Hosts differ. Probabilities also reflect the first answer line | AI assistant, no separate approval; disclosed |
| Report usable counts and uncertainty | Done: Wilson CIs, exact McNemar, usable counts | | Delivered. Bonferroni, Holm and item-level intervals added afterwards, not planned in advance |
| Compare stored vs current, and labelling | Done | | Delivered |
| Success: lower acceptance with no fall in useful recall | Met for Nemo on automatic scoring. 1 Qwen3.5-9B check unreadable. Checks are easy and n is small | | Delivered, with limits stated in README |

### Logging and AI use

| Planned (MS1) | Done | Why | Who approved |
|---|---|---|---|
| Log prompt, model and version, toggle state, raw response | Done, but "version" is only a slug; **logs are not in the repo** | OpenRouter gives no snapshot. Logs were excluded for size | Exclusion: AI assistant proposed; Advaith approved (button) |
| Tools: ChatGPT, Exa, "similar tools" for research; Claude Code and Codex for the build | Claude Code and its subagents for nearly everything; Firecrawl on 5 Nov; DeepSeek V4 Flash as the round 5 judge. No Exa or Codex in the record | Single-tool session | Advaith |
| Important outputs checked; final runs from the harness, not a chat model | Runs came from the harness. Most checks were AI-on-AI | See AI-use log | Open issue |
| Disclosure of AI-generated work | **In the README since 5 Nov, not in git.** Co-author line removed at Advaith's request. `report/draft/` is AI-generated and says so at the top | He did not want it shown in commits | Advaith. Must be disclosed in the report's AI-use log |

### Roles (MS1 plan only)

| Planned (MS1) | What the repo and session show | Why | Who approved |
|---|---|---|---|
| Advaith: systems. Aditya: ideas and research direction. Elkan: evaluation. Tony: run the multi-model tests | Every commit is under Advaith's account. Every run used his session, machine and OpenRouter account. Other members do not appear in the record. **This does not show they did nothing; it shows the record is silent** | Unknown | [TEAM TO COMPLETE]. The README still lists "Tony (runs)": correct it if it no longer holds |

### Feedback items still open

| Feedback (7 Oct) | Status |
|---|---|
| Base vs instruction-tuned pair | Done for one pair, in round 14, after the main study |
| Weaker or ambiguous evidence | Done in rounds 6–7. The "weak" passages are stronger than the name: they take Nemo's false baseline to 0% |
| Double-score a sample and report agreement | Sheets and guide ready in `report/human_pack/`, not done |
| Look into the Bensal/"Bansal" vendor conflict of interest (assigned to Advaith) | Literature agent reported 5 Nov: "Bensal" is the right spelling; the authors work at Writer, Inc., which now sells a memory product. Needs a human read |
| Fricker's work on testimonial justice (Dr Filippov to share) | Societal agent used her 2017 chapter and commentary. **The book has not been read** |
| Start the minimal experiment "this week" | Ran 27 Oct, 20 days later |
