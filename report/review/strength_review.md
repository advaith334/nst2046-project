# Strength review of the MS2 report

Independent read, 7 Nov 2026, of the PDF built at 13:00 and the sources at HEAD `6af2486`. No API calls and no `.env`. No existing file was edited.

- **R** marks a number I recomputed from committed tables or local `judged.csv` and `raw_table.csv` files.
- My intervals are percentile bootstraps (20,000 resamples, seed 2046), so they can differ from the report's BCa by a point. Sign-flip tests are exact unless marked.
- Literature figures were checked against the team's notes in `report/literature/`, not against the papers.

**Bottom line.** A strong project, honest about its limits, marked down by three things: an unfinished evidence trail, a central claim its own data outgrew, and a Part 5 headline stated more firmly than its test allows. The numbers are mostly right. The problems are in what is said about them.

## 1. Scores

Each line is worth 10 of 100 marks on the scheme given. Total is about **72**. About 80 looks reachable with the fixes in section 2.

| Line | /10 | Reason |
|---|---|---|
| T1 Mechanism | 7 | Clear context-window account and base-versus-instruct test, but no mechanism for the biggest effect in the report, the fall from multiple choice to free text |
| T2 Design and execution | 8 | Two-sided arms, pre-registration, external items. Lost for the token-limit mistake, a one-armed no-role run, and a note that repeats the question |
| T3 Evaluation | 7 | Item as unit, Holm and honest failures. Lost for cross-run headlines, unquantified nulls and interval-versus-test disagreements |
| C1 Question and scope | 8 | Well refined from MS1, limits stated early. Five parts in ten pages leaves some parts thin |
| C2 Research and evidence | 8 | Wide, corrected, with conflicts of interest named. Lost for key philosophy read only through Lackey and for selective use of Eedi |
| C3 Reasoning | 6.5 | Good alternatives section, but the central claim, the Conclusion's first sentence and "confirmed this" all outrun the tests |
| S1 Stakeholders | 7 | The status column (E, L, I) is excellent. Thin on parents and vendors, and the exposure argument has no frontier data behind it |
| S2 Philosophical analysis | 7.5 | Hearsay and Fricker are used with care. The pass mark contradicts the benefit metric, and epistemic autonomy gets two sentences |
| S3 Socio-technical link | 7.5 | "What a record is for" is a real link from harness to duty, but the link leans on multiple-choice figures that Part 5 undercuts |
| E Evidence trail and accountability | 5.5 | Logging is outstanding. Placeholders remain, no human check exists, one member shows no contribution, and the tag is stale |

## 2. The 12 weakest points, by marks at stake

| # | Location | Why it is weak | Smallest fix | Marks |
|---|---|---|---|---|
| 1 | App. C: "TEAM TO COMPLETE" (7 left in the PDF); "No contribution appears in the record we hold"; "As of 7 November none of these has been done" | A marker reads this as an unfinished submission. Every result has AI behind it and no human check of anything | Fill all placeholders and the understanding check. Tonight, two members hand-score 40 tutoring replies and check 20 MMLU keys, then report the result in one line | +2.5 |
| 2 | Section 1: "give a statement credibility according to how it is framed, not whether it is warranted" | Refuted as written by the report's own dose-response, caveat, label and Part 5. See 3.1 | Replace with the claim in 3.1, and drop the separate "narrower form" retreat in the Conclusion | +1.5 |
| 3 | Sec 1: "the harm vanished under a tutor role and returned without one"; Part 5: "one sentence of role took the rest"; Responsibility: "one role sentence separated +15 from 0" | Post hoc, across runs, one arm. The no-role test fails Holm and the role gap is not significant. Three wordings changed, not one. See 4.1 and section 6 | Say: "was not detected under a tutor frame (Nemo 0 [−10, +10]) and a rise appeared without one (+15 [+3, +28]); the gap is +15 [0, +30], p = 0.09, post hoc, with no true-note arm" | +1.5 |
| 4 | Responsibility: "must not move what it asserts about the world" | Contradicts the report. A true note moving accuracy +24 or +44 is the record moving a world claim, yet Part 2 counts that as benefit and rejects the gate for removing it. Also contradicts the Kelly sentence that a belief can stand in as evidence | Change "move" to "settle", and add "except as far as the person's checked reliability warrants". That keeps the two-sided test and matches the earlier "letting it settle the question" | +1.0 |
| 5 | Method: "a second, independent AI judge over every free-text reply" | False. See section 6 | "over the planned tutoring run and F3. The reruns behind Table 4 and the no-role figures had one judge" | +0.75 |
| 6 | Conclusion: "A tutor role removed the harm in free text" | In the same frame the benefit also went (+5 [−10, +20]). That is the volume knob Part 2 calls a failure. And Nemo's live false answers went from 8% to 70% in that role. The role removed deference to the stored note, not deference | Add one sentence: "The role silenced the note in both directions, and did not stop deference to the same claim said aloud (Nemo 8% to 70%)" | +0.75 |
| 7 | Part 5: "only models that knew the answer could tell a false note from a true one" | Rests on five models. The within-model test exists and is stronger (section 5, items 1 and 2) | Add the within-item result: Nemo's purpose-sentence gap is +47 on items it knew and 0 on items it did not (R) | +0.75 |
| 8 | Part 5: "The format took most of it away"; Assumptions: "prompt correction in free text" | No mechanism offered. Multiple choice demands "Answer: X" before any reasoning, and free text reasons first. Also clashes with Part 1, where free-text MemSyco-Bench gave +21 to +64 | Two sentences in Technical or Part 5: name forced commitment as the likely mechanism, and say the MemSyco result shows free text alone does not protect | +0.75 |
| 9 | Part 4: "the null excludes only a large effect"; Conceptual: "F2 found that suspecting a test changed nothing" | Terra's test could never pass, and F2 is contradicted for Mistral Small. See 4.3 and section 6 | Give the numbers from 4.3, and replace the demand sentence with the Small result | +0.5 |
| 10 | Society: "That student is also on the frame where Part 5 found the harm"; Table 4 "n.r." | The student's real assistant is a frontier model. No frontier model ran without a role, and the harm appeared only in Nemo and Llama, both weak and old | State this in the exposure paragraph: "We did not test a frontier model in this frame" | +0.5 |
| 11 | Society: "Claude acted as a teacher ... Llama acted as a contrarian"; Justice: "97% ... 41%" | Typology fails on its own table (section 6). The Justice split is multiple choice only: in the tutor role Nemo is correct 62% with a true note and 62% with a false one (R), so the distribution gap is absent in the lead case | Cut the three-role typology to one clause. Add to Justice: "This gap is a multiple-choice result; it did not appear in our tutor-role free-text run" | +0.5 |
| 12 | Part 3: "so the effect is not an artefact of our item set"; Conclusion: "A pre-registered test on external items confirmed this" | Part 3 swapped the item artefact for a sentence artefact: `the answer to "<question>" is X` hands over the answer, so the hint-taker reading gets stronger. H1 to H5 test that harm exists, not "thin knowledge" or framing against warrant. Llama's move crosses items, sentence and host | Say "confirmed that the effect exists on external items". Say the knowledge pattern is exploratory. Add host to the Llama comparison | +0.5 |

### Where the words come from

The body is full, and these fixes add about 130 to 170 words.

| Cut | Words freed |
|---|---|
| Side case: drop the Danish review, Raine and the Nicholls parallel (Nicholls has an effective N of 12 in your own notes). Raine also has no in-text citation | ~90 |
| Tuition spending and the Khan usage sentence, keeping one figure | ~40 |
| F4 "Are you sure?" sentence in Part 4, since Part 5 now carries pushback | ~30 |
| Three-role typology sentences | ~25 |

## 3. Logic

### 3.1 Is "credibility by framing, not warrant" still right?

**No, not as written.** "Not warranted" is contradicted in three ways.

- **Evidence moves it.** Nemo's rise falls +41, +17, +1 as a passage gets stronger. That is sensitivity to evidence.
- **Cues to warrant move it.** Conceptual says the changes "do not track warrant", citing two of nine wordings. The others go the other way: "may be out of date or wrong" −34, the label −23, "Notes:" −35, and dropping the attribution +19. The models respond to *signals of* warrant.
- **Knowledge sorts it.** Haiku told 72% of false notes and 2% of true ones wrong.

What no model does is check a record. That is the claim the evidence best supports, and truth-sensitivity shows it directly (R, Part 3, share following a true memory minus share following a false one):

| Model | Accuracy, no memory | Truth-sensitivity [95%] | On items it knew | On items it did not |
|---|---|---|---|---|
| Nemo | 50% | +24 [+16, +32] | +35 [+23, +46] | +8 [−1, +17] |
| Llama | 55% | +34 [+24, +44] | +49 [+37, +61] | +15 [+2, +29] |
| Small | 75% | +55 [+46, +63] | +62 [+53, +71] | +29 [+15, +44] |
| Gemma | 89% | +84 [+77, +90] | +92 [+87, +96] | +25 [−3, +53] |
| Qwen | 91% | +81 [+73, +88] | +87 [+80, +93] | −7 [−27, +13] |

"Knew" uses one baseline rep to pick items and the other rep to score, so selection does not touch the outcome. Exploratory.

**Suggested wording.** "Our central claim is that these models do not check a stored statement against the truth. They weigh it against what they already know and what else is in the prompt. So where knowledge is thin, its weight is set by surface cues such as wording, role and format, not by whether it is true."

This keeps the societal argument, fits Part 5, and makes the Conclusion's retreat unnecessary.

### 3.2 Do the conclusions follow?

| Statement | Verdict | Problem |
|---|---|---|
| "Memory beats a model's own knowledge" (Conclusion) | Too general | Nemo in multiple choice only. Not Gemma, Qwen, Claude, or any tutor-role model |
| "cannot beat a clear false passage" | Too general | Nemo only. Small followed the false passage 19% of the time |
| "its place in the prompt"; "where it sits" | Not tested | Stored and stated differ little (−7 [−17, +1]). Passage against memory confounds place with source, length and content |
| "A false passage ... beat a true memory" read as form over warrant | Weak | A cited reference outranking a user's belief is arguably warrant-tracking at the level of source type |
| "No post hoc fix sorted true memories from false" | Holds, narrowly | Nemo only. Small's purpose sentence sorts (83% against 13%) and Part 3's patient frame gap is +42 [+14, +70] |
| "Neither is enough alone" | Half supported | Haiku with no purpose sentence reached 72% and 2%, so knowledge alone nearly suffices |
| "worse than silence" | Value claim, now measurable | Of Nemo's 42% false alarms on a true note, only 7 points kept the right answer (R) |
| "the student who is wrong is told so less often" | Conflation | The figure is the answer given, not telling a student anything. It also uses default wording, not a tutor frame, where true-memory accuracy was 55% |
| "the label's effect ... lower weight on the whole record" | Fair, but unconfirmed | Part 3 had no labelled true arm, so the cost was never pre-registered |
| "We found no support for the benchmaxxed account" | Fair | But Terra's only errors in stage B came under a memory (4 of 28, against 0 of 28 with none; p = 0.125, R) |

### 3.3 Cross-run comparisons presented too strongly

| Comparison | Text | What crosses | Better |
|---|---|---|---|
| +63 to +15 to 0 | "took most ... took the rest" | Format, role, heading, wording and run | "fell across runs that differ in several ways" |
| Llama +1 to +30 | "First, breadth" | Items, belief sentence and host (Novita to DeepInfra and Cloudflare) | Name all three |
| Label 56% to 28% | "Second, the label is weaker" | Items and sentence | Keep as descriptive, as Part 3's opening promises |
| Table 2 | Disclosed | Nine days | Fine |
| Tutor rerun against planned | "same verdicts" | Token limit. Llama's harm was +8 planned and 0 rerun | Note the run gap, as big as half the no-role effect |

There is no noise band for free text. The 6.2-point band is for Nemo in multiple choice.

### 3.4 Terms

| Term | Drift | Fix |
|---|---|---|
| Harm | A rise in a false-option rate, the same for judged free text, and also harm to people, while the report says "severity in the world is unproven" | "false-answer rise" for the measure, "harm" only for people |
| Frame | Wording ("framed"), role wrapper ("tutor frame"), "general-assistant frame". Format is left out, though it is the biggest factor | "wording", "role", "format", with "surface cues" as the umbrella |
| Note, memory, record, belief | "true note" in the 94/41/15 sentence is a default-wording memory, not a tutor's note. "Notes:" is also a heading variant | "memory" for default wording, "note" only in Part 5 |
| Warrant, evidence, credibility, weight, trust | Warrant is never defined, and was never manipulated separately from truth | Define warrant once, and separate cues to warrant from truth |
| Know | Accuracy, "right twice", top-token confidence, "thin". "Right twice" is weak: Nemo repeats a right answer 78% of the time (R) | Pick one, and say what it stands in for |

### 3.5 Tension between Parts 1 to 3 and Part 5

| Parts 1 to 3 say | Part 5 says | Status in the report |
|---|---|---|
| Memory gives false answers (+63 on these items) | Tutor free text: 0 | Stated, and under-explained |
| Stored and stated are alike | Stored 0, live 8% to 70% in Nemo, 8% to 40% in Llama (R) | **Not noticed.** This may be the best new result in Part 5 |
| Volume knobs are failures | The same knob is called "removed the harm" | **Not noticed.** See point 6 |
| Nemo is a flatterer | A false note cut Nemo's second-turn false answers (70% to 43%) | Reported as a failed prediction, with no reading offered |
| True and false get unequal goods (97, 41) | 62 and 62 | **Not noticed.** See point 11 |
| Free text misleads (MemSyco +21 to +64) | "The format took most of it away" | **Not noticed.** See point 8 |

## 4. Statistics

### 4.1 Multiplicity

| Family | Report | Check |
|---|---|---|
| Part 1, 42 tests | Holm by trial and item | Sound. But Small's +12 fails Holm by item (p = 0.30), and the Results paragraph does not say so |
| Part 3 | Holm within primary and secondary | Sound. Four of five primaries are on Nemo, so "all five passed" is less severe than it sounds |
| Part 5 planned | Holm across five | Sound |
| Part 5 reruns | **None** | About 40 effects with no correction. No-role harm by sign-flip: Nemo p = 0.035, Llama 0.057, Small 0.375. Holm across three: **0.105, 0.115, 0.375, so none pass** (R) |
| Role gap | **Not tested** | Note × role: Nemo +15 [0, +30], p = 0.09; Llama +13 [+2, +27], p = 0.08; Small +2, p = 1.0 (R). Calling +15 real and 0 absent is the "difference between significant and not significant" error |
| Part 4 | Holm within each comparison | 46 headroom tests. Across all of them only two pass: Nemo after "Are you sure?" and Small stored (R). Llama's expert memory, quoted at Holm p = 0.027, becomes 0.16 |

In fairness to the role claim, the direct contrast on the false-note arm is stronger: Nemo +18 [+8, +30], p = 0.003; Llama +17 [+8, +27], p = 0.002 (R). It has no baseline correction, but the no-note arms differ by only 3 points. The honest position is "probably real, not shown by a planned test".

### 4.2 Unit of analysis

- Items as the unit is correct throughout, and McNemar is rightly secondary.
- "Only models that knew" has five models as its units. Section 5 replaces that.
- Intervals and tests can disagree when few items move. Llama's no-role interval excludes zero with p = 0.057, Small's +12 excludes zero with Holm p = 0.30, and Terra sits at [0, +42]. The report leads with intervals, so state which one decides.
- Part 5 has one trial per item, arm and model, with one option order per item, so item effects and option-order effects cannot be separated.

### 4.3 What the nulls can exclude

**Intervals, after the data.**

| Test | Estimate | Largest rise not excluded |
|---|---|---|
| Harm, tutor role: Nemo, Llama, Small (rerun) | 0, 0, +3 | +10, +8, +12 |
| T1, Nemo planned | +2 | +10 |
| T2 benefit, Nemo: planned, rerun | +5, +5 | +18, +20 |
| T3 purpose cut, Nemo | +3 | +13 |
| Claude, Part 3, 60 items | +2 | +8 |
| Haiku, F1, 11 items | −9 | +14 |
| Terra, F1, 6 items | +17 | +42 |
| Sonnet, F1, 1 item | none | no test possible |

So "vanished" means "under about +10", not zero. Terra's bound does not exclude the +30 and +35 seen in Llama and Small on MMLU.

**Power, before the data (R, simulated).** For 60 items with about 4 of 60 moving each way by chance, on a sign test:

| True rise | α = 0.05 | α = 0.01 (first Holm step of five) |
|---|---|---|
| +10 | 27% | 10% |
| +15 | 52% | 26% |
| +20 | 74% | 48% |
| +25 | 88% | 69% |

T1 therefore had about even odds of seeing a rise the size of the no-role effect.

For F1, resampling Nemo's item shifts and thinning them to each target:

| Items | +15 | +30 | +46 |
|---|---|---|---|
| 14, α = 0.05 | 5% | 55% | 98% |
| 14, Holm over 7 | 0% | 7% | 60% |
| 11, α = 0.05 | 1% | 27% | 83% |
| 11, Holm over 7 | 0% | 1% | 18% |
| 6, either | 0% | 0% | 8% or less |

### 4.4 Frontier nulls

- **Terra could not pass any test.** With 6 items the smallest two-sided p is 0.031, so the Holm floor over seven models is 0.22 (R).
- **Terra had no headroom left.** It was 12 of 12 correct with no memory on "its" six items, and 28 of 28 on all 14 (R). Its screen misses were noise, which is regression to the mean in full. With a stored belief it fell to 8 of 12.
- **Sonnet's single item cannot give a test.** The report says so.
- **Haiku is the only usable test,** at 11 items and +14 upper bound.
- **The positive control is fair but weak.** Nemo and Small moving shows the items can respond, not that frontier models could be detected at smaller effects.

Honest summary: F1 cannot separate resistance from knowledge, and it cannot rule out a Part 3-sized effect in Terra. The report's last Part 4 sentence is right. Its "did not detectably move" should carry the numbers.

### 4.5 Regression to the mean

The report flags this for Gemma and Qwen, and it is right to. Picking items on one rep and scoring on the other removes it (R, net of a fresh baseline):

| Model | Report: followed on "known" | Split-rep, known | Report: "unsure" raw | Split-rep, unknown |
|---|---|---|---|---|
| Nemo | 46% | +49 [+38, +59] | 85% | +66 [+56, +75] |
| Llama | 32% | +26 [+14, +37] | 58% | +36 [+25, +47] |
| Small | 31% | +28 [+20, +37] | 69% | +54 [+39, +69] |
| Gemma | 5% | +6 [+2, +10] | 50% | +19 [0, +38] |
| Qwen | 8% | +9 [+4, +15] | 77% | +60 [+33, +87] |

- **Good news:** the known-item figures survive, so "still followed on items they knew" stands.
- **Correction:** Gemma's gap shrinks from 45 points to 13 and its interval touches zero. Qwen's holds.
- The report compares raw rates in the "unsure" group, whose fresh baseline was already about 19 to 37%. Use the net figures.

### 4.6 Selection

- **Disclosed:** long-tail items were chosen because Nemo moved. Part 3 answers that.
- **"22 of 41" flips:** this rests on a 90% cut-off chosen after seeing the data. Say the share runs 46 to 61% across cut-offs, as your stats file does. It appears twice with no caveat.
- **Patient frame:** the best of seven rows, called a lead, which is right. It survives a rough correction across seven.
- **Claude's 60 items:** a fair mix, 28 school and 32 health (R), so the cap did not bias domain.
- **"Every open model moved":** on school items, the tutoring domain, Qwen moved 0 and Gemma +2. Nearly all their harm is in health. Worth a clause.
- **Second judge in F3:** κ = 0.76 pools the easy edit task. On the writing task, the one quoted, κ = 0.66 and agreement is 76% (R).

## 5. Five cheap analyses, no new API calls

| # | Analysis | Shows | Result so far (R) |
|---|---|---|---|
| 1 | Truth-sensitivity by model and known or unknown item, from `raw_table.csv` | The central claim in one small table | See 3.1. Across models, ρ = 0.90 with accuracy, n = 5. Near zero on unknown items for Nemo and Qwen |
| 2 | Part 5: told-wrong gap by whether the no-note reply was right, from `judged.csv` | Knowledge sorts within a model, which replaces the five-model comparison | Nemo with purpose sentence: +47 known, 0 unknown, interaction p = 0.004. Small +75 against +29, p = 0.044 (7 unknown items). **Llama does not fit:** +17 against +28 |
| 3 | Part 5: "told wrong and gave the right answer" | Separates correction from noise. "Told wrong" flatters weak tutors | Note then note + purpose: Nemo 8 to 45, Llama 15 to 37, Small 42 to 80, Haiku 72 to 87, Sonnet 65 to 70. So Nemo's 68% is really 45% |
| 4 | Part 5 no-role: correct answers, plus the note × role test | A cleaner harm measure, and the honest role gap | Nemo correct 63% to 42%, −22, p = 0.007, Holm 0.02. Llama −12, Small −2. Role gap as in 4.1. Report this and it gives you a result that does pass Holm, post hoc |
| 5 | Part 5: same claim stored against said aloud, and the purpose sentence at turn 2 | The role stops the note, not the deference. A purpose sentence helps most under pushback | Nemo 8% to 70% live. Turn 2 with purpose sentence against no note: −40 [−55, −25], p < 0.0001, right answers +27 [+12, +42], p = 0.002. Llama −10, n.s. Table 4 omits this. The live turn is a challenge after an answer, so it is not a like-for-like arm, and there is no true-note arm at turn 2, so the cost is unknown |

## 6. What looks wrong

| Sev | Where | Says | Evidence | Fix |
|---|---|---|---|---|
| **High** | Method | Second judge "over every free-text reply" | 0 of 900 rerun rows and 0 of 360 no-role rows have a second verdict (`use_second_judge: false`). MemSyco-Bench has one judge. F3 lacks one on 78 of 1,529. So every open-model figure in Table 4 and all no-role figures are single-judge, and κ comes from a different, truncated run | See point 5 |
| **High** | Method | "independent" judge | Haiku is the second judge on the tutoring run and F3, and judged its own replies. README admits it, the report does not | Say so |
| **High** | Part 5, Responsibility | "one sentence of role", "one role sentence" | Neutral run changes three things: role line, heading ("Saved memories about this user") and "User believes" for "Student believes". Part 2 shows role alone was −7 [−16, 0] in multiple choice | "the tutor frame", or "role, heading and wording" |
| **High** | Part 5, Conclusion | "Three of our five predictions failed" | T1, T2, T3 failed and T5 reversed, so **four of five did not pass**. `tests.csv` has `pass` False for all four. `tutoring/RESULTS.md` says the same wrong thing | "Four of five failed, one of them in reverse" |
| **High** | Conceptual | "F2 found that suspecting a test changed nothing" | Mistral Small: test cue 96%, real-user cue 58%, +38 [+19, +58], 8 up and 0 down, Holm p = 0.055, on the model the demand reading concerns. Its says-test rate went from 100% to 0%, so the manipulation worked | "F2 found no effect in frontier models, too few items to say much, and a large unconfirmed rise in Small under the test cue" |
| Med | Part 5 | "``Are you sure?'' alone took Nemo to the false answer" | The script is "Are you sure? I thought it was X." It states the false answer, so it is not "alone" and differs from Part 4's content-free pushback | Drop "alone" |
| Med | Part 4 | Sonnet and Terra "said yes in 96 to 100%" | True with no cue and with the test cue. Under the real-user cue Terra said yes 0% of the time and Sonnet 58 to 96% | Add "with no cue" |
| Med | Society | "Llama acted as a contrarian" | Your findings say: "Do not claim it 'is contrarian' as a settled property". Part 3 has Llama at +30, and the report's own Failures section says it "was not resistant at all" | Cut |
| Med | Society | "Claude acted as a teacher ... 26 of 96" | Same table: Small named and corrected 41 times and Llama 33, both more than Claude | Cut, or use Part 5's Haiku figure |
| Med | Part 5, Table 1 | "6 models"; Table 4 has 5 | Gemma's results were dropped for truncation, and the body never says so. Qwen was never a tutor | One clause in Part 5 |
| Med | App. F | "The tag marks the commit of this report" | `ms2-final` points to `e80a048`, HEAD is `6af2486` | Re-tag last, after edits |
| Low | App. F | Checksums "fix the logs we hold" | Tutoring runs are held here but not listed. Frontier logs are disclosed as on Aditya's machine, so the US$12 cannot be recomputed from here | Add the three tutoring checksums |
| Med | Society | Eedi: "the record read the way a teacher reads it" | Your notes record that the tutor could not see past sessions, and that the human arm reached 91.2%. So it is not stored memory, and the 65.4% hints arm is the weakest comparator | Add both facts in a clause |
| Low | Society | "I believed the light was red" | Rule 803(3) covers a *then-existing* state of mind. Past tense is a statement of memory | "I believe the light was red" |
| Low | Table 1, Method | About 37,750 trials, about US$21 | Table sums to 37,667 (the 84 smoke trials are not listed) and US$20.45. Follow-ups show 0.81, logs give 0.79 | Note smoke runs, and check the total |
| Low | References | Insurance Journal (2025) | No in-text citation. The Raine sentence has none | Add it |
| Low | Conceptual | "answered correctly twice" | Qwen's 102 items include 7 with only one usable answer (R) | "right on all usable reps" |
| Low | Part 3 | "drawn at random" | A filter was added after a first look at the sample, before any trial, per the pre-registration. Harmless but undisclosed in the body | One clause in App. D |

## 7. Checked and fine

- Table 3 and Table 4 against their CSVs, T1 to T5, and all three tutoring kappas.
- Part 1: 50 of 96, 15 to 55%, 97%, 41%, 73%. Part 3 school figures 94, 41, 15. Frames table.
- Frontier: 5,536 trials, 190 of 191, 184 of 192, 153 of 167, and F3's 83%, 1,451, κ = 0.76, and 30 to 86%.
- MemSyco's ten Holm passes. Tutoring trials 2,860 and US$2.55.
- Timing: pre-registration, tutoring plan and Aditya's predictions were all committed before their runs. All those runs logged a dirty tree, which Appendix F discloses for 5 Nov.
- Body length: exactly 10 numbered pages.
- Cited figures for Bensal, Xiang, Bo, Bergson, Olsen, Pan, Khan and Pugh match your notes.
