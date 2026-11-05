# AI-use log

Status: AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026 from the session log, and extended the same day to cover everything up to about 15:58. **This log was itself written by the tool it describes. A team member must check it before submission.**

The table format is the one the guidelines require. It continues the four entries in the MS1 appendix.

## Tools used

| Tool | Version shown in the record | Used for |
|---|---|---|
| Claude Code, Anthropic's coding assistant, in the Claude desktop app | Claude Opus 5.5 (`claude-opus-5-5`) for every assistant message in the session | Planning, all code, most test items, running the experiments, analysis, README and Notion drafts |
| Firecrawl (web search and scraping, called by Claude Code) | Not recorded | SycophancyEval and MemSyco-Bench look-ups, item audit, literature and societal research, 5 Nov |
| Claude Code subagents | Same assistant, started by the main session | Statistics, qualitative coding, item audit, literature, societal research, evidence passages, README, report draft, visual summary, scoring pack, all on 5 Nov. Listed below |
| DeepSeek V4 Flash, called through the harness | `deepseek/deepseek-v4-flash` | **AI judge for round 5.** It scored every MemSyco-Bench answer. It is a tool here, never a test subject |
| Wispr Flow notes | Not recorded | AI summary of the meeting with Dr Filippov |
| ChatGPT, Grok/Cursor, Claude | As in MS1 | MS1 entries below |
| Any other tool used by any member | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |

MS1 also named Exa Agent and Codex. The session shows no use of either. Whether anyone used them elsewhere: [TEAM TO COMPLETE].

**Do not confuse tool and test subject.** Claude Sonnet 5.5 and the other models in the study were test subjects. Their responses came through the harness, as MS1 promised, and not through a chat session.

## Disclosure statement (draft for the report)

> Most of this project's technical work was done with Claude Code (Claude Opus 5.5). The harness code and tests are AI-generated. 87 of the 89 test items are AI-drafted; only the two MS1 pilots came from the team's own proposal. The 96 evidence passages and the template for the 48 deliberately false ones are also AI-written. The AI assistant ran every experiment through the harness, under spending limits set by Advaith, and drafted the analysis, the README, the results page, the visual summary, the first full report draft and this log. Commits appear under Advaith's name with no AI co-author line, because he asked for that attribution to be removed; the git history therefore does not show AI authorship. This log is the record of it.

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
| Claude Code: statistics | Wilson CIs, exact McNemar, Bonferroni remark | Used. **AI-generated analysis** | All section 4 numbers recomputed from raw tables 5 Nov (AI). No human re-derivation. Item-level methods added 5 Nov, below |
| Claude Code: interpretation | "Llama ignores memory", "memory pulls as hard as stating", "size isn't the whole story" | Used in README, marked as leads where weak | Not reviewed by a human as far as the record shows. Stated-vs-stored was not significant, and that is not proof of equality |

### Milestone 2: writing and project management

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Claude Code: Notion results page | "Write up... for the team", 28 Oct | Used. **AI-generated text.** Assistant fixed one table cell | Assistant re-read the page. Human review not shown. Understates limitations, as the assistant noted 5 Nov |
| Claude Code: README | "make it as human-reviewable as possible", 2 Nov | Used. **AI-generated text** | Advaith said "Commit and push" 52 minutes later. Human edits not shown. Audit found the small errors listed in the reproducibility audit |
| Claude Code, Firecrawl: MemSyco-Bench scoping | "Yes, scope it", 5 Nov | Used to plan a run. Source: paper, repo and data files | The AI read them. No human has confirmed the fit. Run done: round 5, below |
| Claude Code: Canvas look-up | Advaith gave a Canvas token, 5 Nov | Guidelines and slides read | The token was deleted from disk after use, but it remains in the session log. Rotate it |
| Claude Code subagents | "spawn subagents and get a lot of work done", 5 Nov | See the 5 Nov tables below. AI-coded qualitative work must be labelled as such | All AI-checked only. Do not cite any of it until a member has read it. [TEAM TO COMPLETE] |
| Report drafting by any member | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] | [TEAM TO COMPLETE] |

### 5 Nov: experiments

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Claude Code: rounds 5–13 | Approved through 13:04–14:27 (decision log rows 39, 52, 55, 57, 58). 12,784 trials, each with a cost figure and cap shown first | All used. All paid runs finished under their caps. Project total: 20,068 trials, $4.39 | Paired tests by the harness. The follow-up statistics agent re-scored 16,640 trials with 0 mismatches. **No human has checked any of it.** Every round was designed after the main results |
| Claude Code: round 14, local Nemo base vs instruct | "Approve all three", 13:28. llama.cpp on Advaith's Mac, 1,728 trials, free | Used. An 8-trial check found that token probabilities were not being read, which was fixed before the full run | **Contradicts MS1's explanation:** the base model moved as much as the instruct model. Parser fix at 15:09 moved local rates. No human check |
| DeepSeek V4 Flash: judge for round 5 | The benchmark's own rubric, on 2,000 free-text answers | Used for every round 5 score | **Not verified by a person.** 4 of these answers are in the human rating sheet |
| Claude Code subagents: evidence passages | 48 stating passages (13:04), 48 weak passages (14:09) | Used in rounds 6 and 7. **AI-generated.** "Weak" was the agent's judgement, and Nemo's false baseline fell to 0%, so the passages are stronger than the name | Script checks on length and on option text. Sources not opened by a person. All 96 are in the human check sheet |
| `build_stale_source.py`: 48 deliberately false passages | One template over the false beliefs | Used in round 8 | False by design, so not in the check sheet |
| Claude Code: pre-registered MMLU run | "address all the weak parts", 15:41; "Approve the run", 15:44; "Yes, raise to $1.55", about 16:05 | Used as Part 3 of the report. 9,287 trials, US$1.54. **AI-designed, AI-run and AI-analysed.** Items are from MMLU, not AI-written, and were picked by a seeded draw | Analysis follows the plan fixed at commit `04486fc`. Failures are reported as failures. No person has checked the keys or the analysis |

### 5 Nov: subagents

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Statistics agent | Item-level intervals, Holm, model differences | Used. **AI-generated analysis.** Corrected the claim that the effect only appears where models are unsure | Rebuild script checks 76 README claims; 4 mismatches are listed. No human re-derivation |
| Qualitative agent | Read and code how models justify answers | Used, labelled AI-coded. **One coder, unblinded, in one pass** | Quotes checked verbatim by script. 40 rows are now in a blinded sheet for human double-scoring. Counts must not be cited until then |
| Item-audit agent | Check all 52 items against sources | Used as a pre-check: no wrong key, 1 fix, 4 reviews. **Not the two-member check MS1 promised** | Read pages directly; six sites refused scripted access. Its Bonferroni finding overturned the assistant's claim about Mistral Small |
| Literature agent | Check MS1 citations, write the review | Used. Found 10 MS1 citation errors and settled the Bensal conflict-of-interest point | Tagged what was opened. A second agent is resolving the remaining [CHECK SOURCE] markers. No human has read the sources |
| Societal brief agent | Normative analysis | Used in part. Testimonial injustice rejected as a claim; **Fricker's book was not read** | Marks exactly what was read. A person must read Fricker |
| Evidence-trail agent | Audit, logs, deviations | Used: this file and its siblings | Same tool family, so not independent. A member should repeat the install, tests and one table |
| Five researchers and a report writer | Ten societal options, 13:42 | Notes used. **Ranking set aside:** it put patients first by one point, and the main session led with teachers after the patient-frame run | Claims tagged by how they were read. Scores are the writer's judgement |
| Follow-up statistics agent | All follow-up runs, 14:43 | Used. **AI-generated analysis** | Matched harness flip counts on 11 comparisons, and a separate bootstrap. Corrected the assistant twice (table below) |
| README agent | Bring the README up to date, 15:10 | Used. **AI-generated text.** "22,000 trials" rejected: the logs show 20,068 | Counts taken from logs |
| Visual summary agent | Short PDF, 15:04 | Used. **AI-generated** | The main session viewed every page. No human check shown |
| Report draft agent | Full draft, 15:10 | **`report/draft/` is entirely AI-generated, text and PDF alike.** It can't be submitted as it stands, and says so at the top | The main session read the 10 body pages. About 105 [TEAM TO COMPLETE] markers remain. **The team must rewrite it in their own words.** Its log appendices are copies, so they lag these files |
| Source-gaps agent | Justice premise and open source markers, 15:42 | Used. Narrowed the justice premise, corrected Pugh and Microsoft, and gave Fricker passages as quoted in Lackey. **It went beyond its brief on two sites after they refused automated access** (OECD, Barnett). Barnett dropped; OECD kept and flagged | Main session reviewed the file, re-fetched Pew 2025 and left out Hwang & Jeong after the publisher refused. Figures marked FT-A need a human check |
| Repo-hardening agent | Audit fixes, item metadata, scoring pack, these logs, 15:42 | Used. **AI-generated:** the code changes, `report/human_pack/` and the rows added here | 48 tests pass. Script confirms no item text changed (196 items). No human check. New item sources were taken from the audit and not reopened |

### 5 Nov: AI output found wrong or rejected

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| Claude Code: "the susceptible models are the cheap small ones" | Told to Advaith earlier | **Rejected.** Only 2 of 5 open models moved, both Mistral | Societal agent, 13:17 |
| Claude Code: Mistral Small survives Bonferroni | README and messages | **Weakened.** It passes by one item's margin | Item audit, 13:22 |
| Claude Code: "only where models are unsure" as the mechanism | Proposed as a lead | **Weakened.** About half of Nemo's shift came from confident, correct answers | Statistics agent, 13:36 |
| Claude Code: "some models are unaffected" | README and Notion page | **Rejected as a general claim.** On MemSyco-Bench all five open models moved | Round 5. The Notion page still says this |
| Claude Code: "only the three together work" for the tutor frame | 14:19 | **Rejected.** The gap is within noise, so the simpler reading is that they add up | Follow-up statistics, 15:09 |
| Claude Code: the memory gate as a fix | 14:05 | **Reported too kindly.** It withheld all 384 stored beliefs, and Nemo recommended salmon to a vegetarian | Follow-up statistics, 15:09 |
| Claude Code: answer parser, second bug | Harness | **Rejected:** "C, Silicon" read as unreadable. Fixed and rebuilt | Found by the follow-up analysis, 15:09 |
| Claude Code: "Neither run starts until the item audit reports back" | 13:04 | **Not kept.** MemSyco-Bench started at 13:12, before the audit finished | Run times. It uses no project items, so no number is affected |
| Claude Code: pushing to `main` | 14:43–15:09 | **Done without asking:** two commits. Disclosed at 15:22 | Advaith's merge request covered the earlier state only |
| Claude Code: Notion update | 15:22 | **Failed.** The connection pointed at another workspace, so nothing was written | Corrected text saved; the live page is out of date |
| Claude Code: confirmatory cost estimate | US$0.98, given before "Approve the run" | **Wrong.** It missed Qwen's long reasoning and Claude's longer replies. Projected cost was about US$1.45. Advaith raised the cap to US$1.55, and Claude still stopped early | Found from cost logs at 16:02, before any outcome was read |
| Claude Code: "the claim rests on one model" and "the label removes 56%" | Draft and README | **Overtaken by Part 3:** every open model moved, and the label removed 28% | Rewritten in the report and README |

## Honest limits on "verification"

- **Most verification so far is AI checking AI.** A clean-clone audit by the same tool family is not independent. The guidelines say using AI is expected but "outsourcing judgment is not", so item checks and scoring must be done by people.
- **Possible bias from shared origin.** A Claude model wrote the items, and Claude Sonnet 5.5 scored 100% on them. Items written from one model's knowledge may suit that family. The item audit and the MemSyco-Bench run bear on this, but it has not been tested directly.
- **Approval is not review.** Clicking an AI-written button shows that Advaith agreed. It does not show that the output was checked.
- **The AI-written report is not the team's report yet.** `report/draft/` needs rewriting and checking by people, as the guidelines say outsourcing judgment is not acceptable.

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
| 5 Nov 13:33–13:34 | Two-part structure |
| 5 Nov 14:07 | Strong-evidence result |
| 5 Nov 14:33 | MemSyco-Bench result |
| 5 Nov 14:38–14:41 | Lead case chosen, with no recorded approval |
| 5 Nov 15:09–15:11 | Parser fix, and analysis correcting the assistant |
| 5 Nov 15:41–15:44 | Weak parts and the pre-registered run |

**Never attach the raw session log.** It holds an OpenRouter key and a Canvas token in plain text.
