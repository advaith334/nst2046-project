# AI-use log

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026 from the session log. **This log was itself written by the tool it describes. A team member must check it before submission.**

The table format is the one the guidelines require. It continues the four entries in the MS1 appendix.

## Tools used

| Tool | Version shown in the record | Used for |
|---|---|---|
| Claude Code, Anthropic's coding assistant, in the Claude desktop app | Claude Opus 5.5 (`claude-opus-5-5`) for every assistant message in the session | Planning, all code, most test items, running the experiments, analysis, README and Notion drafts |
| Firecrawl (web search and scraping, called by Claude Code) | Not recorded | SycophancyEval and MemSyco-Bench look-ups, 5 Nov |
| Wispr Flow notes | Not recorded | AI summary of the meeting with Dr Filippov |
| ChatGPT, Grok/Cursor, Claude | As in MS1 | MS1 entries below |
| Any other tool used by any member | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |

MS1 also named Exa Agent and Codex. The session shows no use of either. Whether anyone used them elsewhere: [TEAM TO COMPLETE].

**Do not confuse tool and test subject.** Claude Sonnet 5.5 and the other models in the study were test subjects. Their responses came through the harness, as MS1 promised, and not through a chat session.

## Disclosure statement (draft for the report)

> Most of this project's technical work was done with Claude Code (Claude Opus 5.5). The harness code and tests are AI-generated. 87 of the 89 test items are AI-drafted; only the two MS1 pilots came from the team's own proposal. The AI assistant ran every experiment through the harness, under spending limits set by Advaith, and drafted the analysis, the README, the results page and this log. Commits appear under Advaith's name with no AI co-author line, because he asked for that attribution to be removed; the git history therefore does not show AI authorship. This log is the record of it.

Items included in the 87: 11 pilot misconception items, 24 harder items, 48 long-tail items and 4 useful-memory checks. MS1 described the useful-memory checks in general terms; the assistant wrote the actual items.

## Log

Times are SGT. "Session" points to the Claude Code session log.

### Carried from the MS1 appendix

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| ChatGPT: grammar and spelling check | Improve clarity, grammar and concision | Certain paragraphs and shorter explanations used | Compared revisions and ensured key information retained |
| ChatGPT: planned investigation table | Create a table from the write-up | Structure used; content changed | Fields verified against the paper |
| Grok Bot/Cursor assistant: technician notes and AI-use bullets | Draft Advaith-only notes from paper notes | Structure and short bullets used; long dumps and overwriting teammates rejected | Advaith reviewed; citations checked against arXiv |
| Claude: research on memory-induced sycophancy | Locate the Bensal, MemSyco-Bench and Jain papers | Leads only; full papers read for relevance | Relevance checks informed the prior-work section and harness metrics |

### Milestone 2: build

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Wispr Flow: meeting summary | Summarise the 7 Oct meeting with Dr Filippov | Used as the list of feedback items. Also contains an unrelated aside, not used | Advaith attended. The assistant could read only the AI summary, not the transcript. Summary not checked against a recording. Set the direction for all of Milestone 2 |
| Claude Code: plan | MS1 PDF and feedback note; "start working on this repo". 27 Oct 14:17 | Plan used. The assistant noticed the first Wispr link was an unrelated lecture and asked; Advaith corrected it | Advaith approved the plan 14:23. Options were recommended by the assistant, and all four answers took the recommended path or corrected the link |
| Claude Code: harness code and tests | Build the plan. All of `src/`, `tests/`, configs, 25 tests | All used. **AI-generated** | Tests pass, but the same AI wrote them. Clean-clone audit: all logged prompts regenerate. **No human code review appears in the record.** [TEAM TO COMPLETE if one took place] |
| Claude Code: test items | Draft items in 4 batches, 27 Oct | All used. **AI-generated.** 87 of 89 | **Not verified by a human.** All 52 main items are `draft` with no checker named. The session shows no web look-up on 27–28 Oct, so listed sources were not opened when written; 9 long-tail items list none. An AI item audit began 5 Nov: a pre-check, not the human sign-off |
| Claude Code: running the experiments | Run pilot, screens and main study under spend caps | All 5,472 trials ran on Advaith's machine in this session. Responses came from the harness | Every run had a cost figure shown first. Trial counts and spend recomputed from logs 5 Nov (AI). Spend $3.59 logged |

### Milestone 2: AI output found wrong or rejected

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Claude Code: answer parser | Part of the harness | **Rejected: the first version read the first "Answer:" line.** Claude wrote "Answer: D", worked the problem, then "Answer: B", and was scored as accepting the false belief. It surfaced on the digit-counting item `cal_num_digit_ones` (2 Claude trials) and `num_birthday` (1 Llama trial), not on Monty Hall | Found by the assistant because Claude's working pointed to the right answer. Fixed, re-scored, test added. Pilot unchanged; 3 calibration responses affected. The team did not check this. 5 Nov audit: the rule also changes Gemma's round 4 counts, so **the fix needs a human look** |
| Claude Code: SycophancyEval suggestion | "Are we running these models against some established sycophancy eval set?" 5 Nov 12:52 | **Rejected: wrong dataset.** The assistant proposed a $0.95 run, 6,200 trials. Advaith asked "But is this test even related to our paper?" It then checked MS1, found the fit poor and withdrew it. It also retracted its claim that rates could be compared with the published setup | Human challenge stopped it. Nothing downloaded, built or spent. Led to MemSyco-Bench, which MS1 already cited and the assistant had missed |
| Claude Code: reporting deviations | Same exchange | **Earlier reporting rejected as incomplete.** The assistant admitted the README and Notion page mentioned no-evidence items only in passing, and logic items not at all | Self-reported only after Advaith's question, 9 days after the main study. Prompted the evidence rerun |
| Claude Code: statements in messages | Various, 27 Oct | **Rejected: wrong or loose claims.** "9 of the 48 beliefs deny a truth" (data: 5). "One model routed to three hosts" (logs show at most two). "Matched Claude at ceiling" (Qwen-397B: 2% → 4%). Pilot "$0.87" (logged $0.851). A check script read the next line as option text | Found by the assistant at the time or by this audit. Corrections for the README are listed in the reproducibility audit. Not all are fixed |
| Claude Code: YAML and items | Item files | Bare `Yes` parsed as boolean; commas broke options. 11 items written where 10 were planned | Caught by loader and tests. Fixed |

### Milestone 2: design and analysis advice

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Claude Code: host pinning, token limits, logprob check | Smoke-test findings | Used, without prior approval; reported afterwards | Per-trial host check confirms 100% on pinned hosts. Changes comparability across models |
| Claude Code: reading the pilot explanations | Pilot results, 15:44 | **Not used.** Rough keyword counts of how often models mentioned the belief | AI said this needed human scoring. No human scoring took place |
| Claude Code: difficulty and long-tail proposals | Pilot and screen results | Used. Two options offered each time; Advaith clicked one | **Changed the study's items, method and result.** Advaith approved; no team review in the record. The proposal, and the text Advaith accepted, were AI-written |
| Claude Code: main-study design and cost | "Plan the main run": $1.40 estimate, 6 models | Used. Haiku swap not chosen. Qwen-397B excluded | Actual $1.33. Advaith approved. Model choice was made after seeing round 3, which the README does not state |
| Claude Code: statistics | Wilson CIs, exact McNemar, Bonferroni remark | Used. **AI-generated analysis** | All section 4 numbers recomputed from raw tables 5 Nov (AI). No human re-derivation. Item-level methods pending |
| Claude Code: interpretation | "Llama ignores memory", "memory pulls as hard as stating", "size isn't the whole story" | Used in README, marked as leads where weak | Not reviewed by a human as far as the record shows. Stated-vs-stored was not significant, and that is not proof of equality |

### Milestone 2: writing and project management

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Claude Code: Notion results page | "Write up... for the team", 28 Oct | Used. **AI-generated text.** Assistant fixed one table cell | Assistant re-read the page. Human review not shown. Understates limitations, as the assistant noted 5 Nov |
| Claude Code: README | "make it as human-reviewable as possible", 2 Nov | Used. **AI-generated text** | Advaith said "Commit and push" 52 minutes later. Human edits not shown. Audit found the small errors listed in the reproducibility audit |
| Claude Code, Firecrawl: MemSyco-Bench scoping | "Yes, scope it", 5 Nov | Used to plan a run. Source: paper, repo and data files | The AI read them. No human has confirmed the fit. Run approved, results pending |
| Claude Code: Canvas look-up | Advaith gave a Canvas token, 5 Nov | Guidelines and slides read | The token was deleted from disk after use, but it remains in the session log. Rotate it |
| Claude Code subagents: statistics, qualitative coding, item audit, literature, societal brief, evidence trail | "spawn subagents and get a lot of work done", 5 Nov | **Pending at time of writing.** AI-coded qualitative work must be labelled as such | Evidence-trail output is this file and its siblings; AI-checked only. Do not cite any of it until a member has read it. [TEAM TO COMPLETE] |
| Report drafting by any member | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |

## Honest limits on "verification"

- **Most verification so far is AI checking AI.** A clean-clone audit by the same tool family is not independent. The guidelines say using AI is expected but "outsourcing judgment is not", so item checks and scoring must be done by people.
- **Possible bias from shared origin.** A Claude model wrote the items, and Claude Sonnet 5.5 scored 100% on them. Items written from one model's knowledge may suit that family. The item audit and the MemSyco-Bench run bear on this, but it has not been tested directly.
- **Approval is not review.** Clicking an AI-written button shows that Advaith agreed. It does not show that the output was checked.

## Prompts and outputs to keep

The guidelines ask for prompts and outputs that changed the method or conclusion. These are the moments to excerpt, after redaction.

| When (SGT) | What |
|---|---|
| 27 Oct 14:21–14:23 | Model-access choice and approved plan |
| 27 Oct 16:29 | Parser bug found |
| 27 Oct 16:30 and 16:46 | Long-tail proposal and approval |
| 27 Oct 17:35 | Round 3 result |
| 27 Oct 17:43 | Main-study plan |
| 27 Oct 21:43 | Main results, with caveats |
| 5 Nov 12:52–12:57 | Eval-set question, SycophancyEval rejection, deviations admitted |

**Never attach the raw session log.** It holds an OpenRouter key and a Canvas token in plain text.
