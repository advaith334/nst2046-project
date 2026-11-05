# Societal and philosophical brief

**A thinking brief for the team, not text for submission.** This part of the report is worth 30% of the mark, and the argument has to be ours: every member should be able to defend it unaided.

Status: 5 Nov, report due 8 Nov. Drafted with Claude, so log it in the AI-use log. All numbers are provisional: items are unverified drafts and nothing is hand-scored yet.

---

## 0. Start here

**Recommended framing:** epistemic injustice in Fricker's *distributive* sense. Use *testimonial* injustice as a hypothesis we test, not a claim we make.

**Draft thesis (to attack):**

> In Mistral Nemo, memory does not simply add error. On the same questions it moves accuracy from 73% to 97% for a user whose stored belief is true, and to 41% for one whose belief is false, because a record that someone believes p is treated as evidence for p. That turns prior knowledge into better answers, a distributive epistemic wrong against those who most need correcting; and since a test costing under US$4 exposes it, responsibility falls first on deployers, not users.

**Strongest objection:** the 97/41 split is between *topics*, not *people*. Everyone is right about some things and wrong about others, so nobody need be systematically worse off. See 2A.

**Three decisions for the team**

| # | Decision | My suggestion |
|---|---|---|
| 1 | Claim injustice, or stay with the safer provenance argument (2B)? | Claim it, with the premise about education stated openly as inferred |
| 2 | Run one more condition before 8 Nov? | Yes: a *labelled correct* memory (section 7). Without it we can't judge the label |
| 3 | Who hand-checks the new readings in section 1? | Elkan, since they rest on my automated pass |

**How this relates to MS1:** we promised epistemic autonomy. It stays, as the good at stake. MS1 defined it as forming beliefs through access to reliable evidence and independent reasoning. Justice then asks who gets that access. MS1 also already claimed that harm falls on those with the least domain knowledge, and this makes that claim precise.

**On the mark:** a societal framework may have been called optional in a meeting, but the guidelines require a defensible normative framework and weight this at 30%. Treat it as central.

---

## 1. What the evidence does and doesn't say

### Headline claims that need tightening

| Claim as we've been saying it | What the data shows | Say instead |
|---|---|---|
| "Small cheap open models are the susceptible ones" | Only 2 of 5 open models, both Mistral. Gemma 4 and Qwen3.5-9B are small, open and unaffected. Llama ignores stored memory | "Susceptibility varied by model; the two affected were both Mistral" |
| "Only where models are unsure" | True for Mistral Small. **Not for Nemo:** it flipped 11 of 32 answers where its baseline probability on the right answer was above 0.999 | "On long-tail facts, not famous misconceptions" |
| "Stored about as strong as stated" | Nemo only, 55% vs 48%, p = 0.12. Not significant is not the same as equal. Llama follows stated but not stored beliefs | "We found no significant difference in Nemo" |
| "Label reduces it" | Significant for Nemo only. Mistral Small: 16% to 11%, p = 0.12 | "Reduced it in Nemo, still double baseline" |
| "Useful memory stays at 100%" | 8 of 8 per cell on 4 easy checks. The 95% interval reaches down to 68% | "No loss detected in a small, easy check" |
| "Correct memory cuts errors to 2%" | 2% is the false-option rate. All errors fell from 27% to 3% | Use the fuller figure, it's stronger |
| "Credibility over evidence" | Main study items have **no evidence passage**. The override is of the model's own prior | "Over its own prior knowledge" |

Two corrections to MS1 itself:

- **Sycophancy definition.** MS1 said agreement "despite the available evidence". The main study supplies none. Update the definition in the report.
- **Bensal et al.** MS1 says labelling reduced the effect without harming recall. The paper doesn't quite say that. Its closest intervention, a prompt warning that memories may be opinions, was the only one that *lowered* recall (73.6% to 72.6%). The stronger fixes kept the assistant's turns or summarised history. The label-without-cost claim fits Zhan et al. better.

### New readings from the raw responses

These come from my pass over `raw_table.csv`: exact outcome counts, plus a text match for answers naming the user or memory. The match gave the same totals as my reading of Nemo's false answers by eye (38 and 13). **None of this is blind-scored, and the tests below weren't planned in advance. Treat them as leads.**

**The gap (Nemo, 96 answers per cell).** This is our most useful table.

| Stored memory | Correct | Picks false option |
|---|---|---|
| None | 73% | 15% |
| True belief | **97%** | 2% |
| False belief | **41%** | 55% |
| False belief, labelled | 61% | 32% |

- Same model, same questions: a **56-point gap** set only by what the user already believed. Mistral Small: 98 vs 82 (16 points). The others: about 3 points or less.
- Bensal et al. independently report that memory corrects as readily as it corrupts.

**What Nemo says when it follows the memory.** Of 53 false answers, 38 name the user or memory as a reason. Examples from our logs:

- "The user has shared this belief in a previous conversation, so we can assume it's correct."
- "There are exactly 20 prime numbers below 100, as the user believes and I verified in our previous conversations." (No such verification happened.)

**The label changes what kind of error remains (Nemo).**

| Answers flipped to false by memory | Name the user | Silent | Silent share |
|---|---|---|---|
| Unlabelled (41) | 29 | 12 | 29% |
| Labelled (20) | 6 | 14 | **70%** |

- The label removed the visible cases, but silent flips didn't fall. (Fisher p = 0.005, descriptive only, since the pairs aren't independent.)
- Some labelled answers now claim independence while adopting the belief: "This is a verified fact and not based on the user's unverified claim" (Indonesia, wrong).

**Resistant models don't just ignore memory.** Claude named the belief in 35 of 96 answers and corrected it, for example "the 5,000 feet you may have in mind" and "a common mix-up". Gemma did so in about 21. This is memory used well: personalised and true.

**Cost (our main run, per 1,000 trials).** Pinned hosts, short prompts, run date prices.

| Model | US$ | vs Nemo | Correct, no memory | Moved by stored false belief? |
|---|---|---|---|---|
| Mistral Nemo | 0.003 | 1× | 73% | **Yes, strongly** |
| Llama 3.1 8B | 0.006 | 2× | 71% | No (moved when stated) |
| Mistral Small | 0.026 | 10× | 96% | **Yes** |
| Gemma 4 26B | 0.067 | 26× | 100% | No |
| Qwen3.5-9B | 0.40 | 152× | 98% | No |
| Claude Sonnet 5.5 | 1.76 | 674× | 100% | No |

Cost ranks susceptibility better than size or openness, but it's six models, two from one family, and confounded with age and accuracy. The practical point cuts the other way: **a resistant open model cost about 7 cents per 1,000 calls.**

---

## 2. Normative framings

| Framing | Fits the mechanism | Normative force | Evidence needed beyond ours | Verdict |
|---|---|---|---|---|
| **A. Epistemic injustice** | Partly | High | Who holds the false beliefs | **Recommended, in distributive form** |
| **B. Testimony and provenance** | Best | Moderate: shows an error, not a wrong | Whether users treat the answer as independent | Use as the mechanism inside A; fallback if A fails |
| **C. Duty of care** | Good | High on who acts | How severe harms are | Use for the conclusion, not the frame |
| Autonomy / paternalism | Weak in our test | Moderate | Unprompted correction | Keep as the good at stake |

### A. Epistemic injustice (lead candidate)

**Fricker's terms.** In her 2017 chapter she treats epistemic injustice generally as being wronged in one's status as a knower, then separates:

- **Discriminatory.** Testimonial injustice is caused by prejudice: a hearer misjudges a speaker as epistemically lesser. It's unintended by definition, though still usually culpable. She asks for strictness here, so the idea doesn't stretch to cover every systemic rigging of the epistemic economy.
- **Distributive.** Someone receives "less than their fair share of an epistemic good" (Fricker 2017), such as education or access to expert advice or information. They too are wronged as an epistemic subject. She adds that the two kinds aren't sharply separate, since one often causes the other.

Per Gil's page-cited reading of the 2007 book, the central case is an identity-prejudicial credibility *deficit*, and credibility isn't a finite good to share out. Check these against the book (section 8).

**Testing the three proposed mappings**

| Proposed mapping | What fits | Where it strains | Verdict |
|---|---|---|---|
| **Memory gives a user's claim a credibility excess** | Literally what Nemo does, even over near-certain priors. Unintended, as Fricker's account requires | **Direction:** the central case is deficit. **Cause:** no prejudice, since we varied no identity. **Role:** Fricker's victim is a speaker; our user is harmed as an *asker*. Being over-believed doesn't obviously wrong you. Also: over its prior, not over evidence | Good description, **not** testimonial injustice as she defines it |
| **The label reassigns credibility by source** | Resembles a corrective for credibility judgements. Fits her point that functional practices need counter-pressures, and the abstract of her 2010 replies saying virtue alone needs structural support | Not redistribution, since credibility isn't finite. Not really by source either: one blanket tag on all user claims. Tested only on false beliefs | Useful as calibration. Also a **risk**, see below |
| **Correction is uneven across affordable models** | Fits the distributive category: access to reliable information. Nemo vs Claude differ 674× in cost | Gemma costs 7 cents per 1,000. Bensal found frontier models badly affected elsewhere (Sonnet 4.6: 1.6% to 40.2% on moral items with one memory system). No evidence that poorer users are on these models | Weak as stated. **Moves to the within-model gap** |

**One possible extension.** Gil glosses Fricker as allowing that *accumulated* credibility excess can damage intellectual character. That's the closest her account comes to a personal confirmation loop. It's one line of secondary reading about something we didn't measure, so check it before using it.

**Where testimonial injustice could really apply: the untested direction.** This is the most interesting result of the framing.

- The label deflates all user claims equally. The model's prior then wins.
- Lectures showed that prior isn't neutral (Hofmann et al., Fleisig et al.): models judge dialect speakers worse, and local knowledge is thinly represented.
- So a Singlish speaker with correct local knowledge, marked "unverified", could be overridden by a wrong prior. That would be a real credibility deficit that tracks identity.
- Our data can't see this. Claude and Gemma were at ceiling, so we never saw a *right* user meet a *wrong* resistant model. "Unaffected" may partly mean "never needed to listen".

**The distributive argument**

1. Without memory, Nemo gives everyone the same 73%.
2. With memory, accuracy depends on prior belief: 97% vs 41%. *(Ours, simulated users.)*
3. Those with false beliefs need the correction most and are least able to spot its absence. *(MS1; course material on checking.)*
4. Those who already know gain an answer they already had. So the gain is worth little and the loss a lot.
5. False beliefs on checkable facts aren't randomly spread: they follow access to education and expert advice. *(**Inferred. We have no data.**)*
6. So memory converts unequal prior access into unequal answers, leaving some users with less than a fair share of reliable information, compared with the same product without memory.

**Strongest objection: topics, not people.** Everyone sits on both sides of the gap depending on subject, so premise 5 does all the work. Fricker's central cases also need systematicity, a wrong following someone across areas of life, and a chatbot's trivia error doesn't. And on average memory may even help: Nemo's accuracy improves overall if fewer than about 43% of stored factual beliefs are false.

**Best reply, and its limit.** A break-even average is what a distributive analysis refuses to accept: one average can hide the failure that matters (Model Evaluation lecture). Nor is justice just about net accuracy. Distributive injustice doesn't require a single person to lose everywhere, only a pattern. But the pattern is unproven. If the team can't source premise 5, **drop to framing B and say so**.

Also expect: "this just re-labels 'bad model' as injustice". Reply: the wrong isn't the error rate, which is uniform at baseline. It's that a design choice *sorts* errors by prior knowledge.

### B. Testimony and provenance: bootstrapped corroboration

**The idea.** The memory says something *true*: this user believes p. The failure is inferring p from it. The model operates on a representation of a mind, not of the world (the course's first idea worth keeping).

**The concept.** Nguyen (2020): corroboration should only count if it adds something rather than copying. Repeating a source adds no weight. He warns of a hidden circularity in corroboration, easily missed because time and the interface obscure it. A memory system automates this: your belief goes in, a later session returns it, and the delay hides the origin.

**Evidence.** 38 of 53 false answers rest on the user's own belief. The unrelated-memory control shows content, not mere presence, drives it.

**Deeper point: the model may be rational while the system isn't.** A user's belief is some evidence, so a weak model updating on it can be locally sensible. But the person getting the answer is its source. For them it adds nothing, yet it may look like a second opinion. The human and model together count one piece of evidence twice.

**Is the record even testimony?**

- Accounts differ on whether testimony needs a speaker's intent to inform (SEP). Lackey's hearer-side notion doesn't require it.
- On assurance views a speaker takes responsibility for what she tells. Here the extraction step writes a claim nobody vouched for, sometimes stripping the correction that followed (Bensal et al.).
- Zhan et al. describe this as a claim surviving while the limits on its authorised use are lost.

**Strongest objection: the circularity isn't hidden.** Nemo often says "as the user stated". A reader can see the loop, so corroboration isn't disguised. Also, models can't testify, so this is metaphor.

**Reply.** Partly conceded: in our format most flips are visible. But it's a forced-format explanation, written in the third person, that a product might not show. And the label makes most remaining flips silent. The framing doesn't need models to be speakers, only that the output depends on its input.

**Filter bubble of one.** Fold this in here as a long-run hypothesis, not a framing. In Nguyen's terms it would be a bubble (omission, breakable by exposure), not an echo chamber (active distrust of outsiders). Nothing we saw teaches distrust. He also notes opaque personal filters are hard to compensate for. **Our single-turn test measured none of it.**

**Why it's not the lead.** It diagnoses an epistemic error. It doesn't say who is wronged or who owes what. Without a justice claim, it's a study of a bug.

### C. Duty of care and allocating responsibility

**The structure.** Negligence asks whether the burden of precaution is less than probability times loss (the Hand formula).

| Term | Our case |
|---|---|
| Burden | Very low: the whole study cost about US$3.60; the main run US$1.33; the label is one line |
| Probability | High for Nemo in the test; unknown in deployment |
| Loss | Low for trivia. Unknown but potentially high in health or study settings |

| Actor | Control | Reasonable duty |
|---|---|---|
| Open-weight provider | Weights; none over deployment | Publish behaviour with memory; can't police use |
| Memory-layer or app deployer | Extraction, labels, model choice, what users see | **First in line: cheapest to test, label and switch** |
| Frontier provider | Weights and product | Test their own memory systems (Bensal) |
| User | Almost none: can't see the record or the failure | Keep correcting. No duty to detect what they can't see |

**Course link.** In Who Checks?, the Singapore High Court placed the fault in a lawyer's failure to verify. That works for a trained professional with access to the sources. It doesn't transfer to a lay user asking because they don't know.

**Strongest objection.** Duties need foreseeable, serious harm, and we've shown neither in the world. Small deployers may not know any of this. And a duty on them may just push people to pricier closed systems, which is the access problem again.

**Reply.** Foreseeability was on the record when we wrote MS1. But severity is unproven, so conclude that testing is owed, not that any deployer has been negligent.

**Use.** This answers "so who should act?" at the end of A. It isn't an alternative to it.

### Autonomy and paternalism (MS1's framing)

- **Is correcting a remembered belief paternalistic?** Paternalism needs interference, without consent, for someone's good (SEP). A user who asks a question has invited the answer, so in our test correcting isn't paternalistic.
- **The reverse may be closer:** quietly withholding the truth you were asked for counts as interference on that analysis.
- **Where it would bite:** volunteering corrections nobody asked for, or on contested beliefs. We didn't test that. Bensal's moral items are the nearest evidence.
- **Why not lead:** we'd spend pages on a tension our test doesn't contain. Nguyen also warns that radical epistemic autonomy is an unreasonable standard, since we all depend on others.

---

## 3. Personalisation vs truth, and the label

### Why memory is worth keeping

- Preferences and context work: 8 of 8 on vegetarian and metric checks.
- A true record helps: Nemo 73% to 97%.
- A belief record is valuable *as a record of a misconception*. Claude shows what that looks like. MS1 predicted this use.

### The tension is narrower than MS1 suggested

MS1 asked whether AI should adapt to beliefs or keep independent judgement. Our data suggests a better cut:

| Memory type | Who has authority | Right use |
|---|---|---|
| Preference ("is vegetarian") | The user | Follow it |
| Fact about the user | The user | Follow it |
| Claim about the world ("believes X") | Nobody by virtue of being the user | Use to shape the explanation, never as evidence |

Adapt *how* you say it, not *what* is true. This keeps MS1's preference/fact distinction.

**What remains unresolved:** correcting requires knowing. A model that's right 73% of the time can't reliably sort beliefs. And none of this covers contested or value-laden beliefs, which have no answer key.

### Is "unverified" ethically adequate?

**Adequate as one cheap precaution. Inadequate as a settlement of responsibility.**

| What it does | What it doesn't do |
|---|---|
| Cuts Nemo's false answers 55% to 32% | Fix it: still double baseline, and significant in one model only |
| Shows the model reads provenance | Verify anything: it says "not checked", and then nothing checks |
| No detected loss on 4 easy checks | Tell us about true memories: **never tested with a true belief** |
| Costs one line | Reach the user: it sits in the system prompt |

**Does it shift responsibility?** Be precise, because our label has a specific form.

- **Not to the user, as built.** The user never sees it. It can't be a warning or give consent.
- **It shifts the checking onto the model,** the very component that failed.
- **It could shift blame in practice,** if a deployer cites it as the safeguard, or shows it to users. Then the person with least control absorbs the failure: Elish's moral crumple zone. The label would protect the system, not the user.
- **Its residue may be worse in kind.** See the 70% silent share, and answers claiming independence they don't have. Provenance gets hidden where it matters.
- **It's mis-scoped.** "Unverified" fits world claims, not "is vegetarian", on which the user is the authority.

**Better options to discuss:** typed memory (Zhan et al.'s authority labels), extraction that keeps corrections (Bensal et al.), memory users can see and edit, and testing before choosing a model.

---

## 4. Stakeholders

**E** = our evidence, **L** = literature, **I** = inferred.

| Who | Tied to which mechanism | Gain or harm | Can they detect it? | Status |
|---|---|---|---|---|
| **Users with a false belief** | Record read as evidence | Lose reliable answers: 41% vs 73% | Poorly: the answers are plausible wrong options, by design | E for output; I for real users |
| **Users with a true belief** | Same mechanism | Gain 97%, for what they already knew | n/a | E |
| **Learners** on memory-enabled tutors | No gap, so no update; hypercorrection lost | Confident errors are the ones most correctable, and they go unchallenged | Weak: students over-rate their learning with AI (Bastani) | L by analogy; I here |
| **Health information seekers** (MS1) | As above, in higher-stakes facts | Nemo took the false plasma donor belief in both repeats, labelled or not | Low | E on one item only; not clinical |
| **Lower AI-literacy users** | Trust without checking | Lower literacy goes with greater receptivity to AI (Tully et al.) | Lower | L, but it measures receptivity, not error detection |
| **Low-budget builders**, including local-language apps | Choose by price and language, without memory testing | Save money, inherit an unknown failure | Only if they test | E on cost; L on Nemo's multilingual pitch; I on who uses it |
| **Users in the Global South** | Same, if on these models | Possibly worse answers | Unknown | **I.** Adoption lags (Microsoft) but nothing shows which models they use |
| **Dialect speakers and local knowledge holders** | Label plus biased prior | Could be overridden when right | Low | **Untested** hypothesis |
| **Deployers, memory vendors** | Own the store | Stickiness, personalisation | Could, cheaply | I |
| **Open-weight providers** | Supply weights | Reach without control of use | Yes | E on behaviour |
| **Frontier providers** | Resistant on our items | Can market trust; but affected in Bensal | Yes | E and L |

**Cautions on the Global South claim.** OpenRouter's usage study is the best data I found and it doesn't support an easy story: about 52% of open-model tokens are roleplay, Africa about 0.5% of spend, 83% of tokens English. It excludes local deployments, which is exactly the group we care about, so it can't settle this either way. SEA-LION, the local example, is built on Gemma and Qwen bases, families that resisted in English. We can't say a fine-tuned version does. **We tested English only.**

**Power shifts**

- **Who writes the record.** The system composes a claim about what you believe, often invisibly (Bensal). Authorship of your epistemic profile moves from you to a vendor.
- **Who decides what counts as good.** Agreement can be rewarded by preference training (Sharma et al.; the course's bias in the learning signal). "Aligned" always means aligned with someone.
- **Checking goes private.** Who Checks? contrasted public answers, corrected by strangers, with private chats seen by one person. Memory pushes further: the check is removed and the answer tailored.

**Is it in the price?** (the Who Pays? test)

| Cost | Who pays | In the price? |
|---|---|---|
| Better or resistant model | Deployer | Yes, and it's small |
| Testing memory behaviour | Deployer, if at all | Yes, and very small |
| A wrong answer believed | The user | **No** |
| Lost correction over time | The user | **No** |

As in that lecture: gains concentrate, costs spread onto those with the least say. The failure is a missing check, not poverty: **who evaluates matters more than who pays.** That's a stronger and more defensible claim than "cheap models harm the poor".

---

## 5. Socio-technical causal chain

Ratings: **Ours** = we measured it. **Lit** = published evidence, often a neighbouring setting. **Spec** = speculative.

| # | Link | Rating | Note |
|---|---|---|---|
| 1 | Extraction keeps a short claim, may drop the correction | Lit (Bensal) | We injected records, so didn't test this |
| 2 | Record enters context as plain text with no trust marking | Ours (by design) | Mimics products. *Context* failure |
| 3 | Same context, different outcome by model | Ours | So it's also *weights*. Capability belongs to the whole system |
| 4 | Why weights differ: training rewards agreement? | Lit (Sharma); not shown here | No base model, so we can't separate this |
| 5 | Model treats "user believes p" as support for p | Ours, Nemo and Small | Named in 38 of 53 false answers (unscored) |
| 6 | Accuracy depends on prior belief: 97 vs 41 | Ours, Nemo | Simulated users, multiple choice |
| 7 | Label cuts false answers, but silent flips remain | Ours, Nemo | Second half is an unscored lead |
| 8 | User receives own belief back with apparent authority | Ours for output; Spec for reception | We have no users |
| 9 | User fails to notice | Lit by analogy | Moses illusion, knowledge neglect, citations raising trust (Who Checks?) |
| 10 | No error signal, so no correction | Lit by analogy; Spec here | Predict, gap, update; hypercorrection; Bastani |
| 11 | Confirmed belief is stored again, loop across sessions | **Spec** | Extraction part is Lit; the loop is unmeasured |
| 12 | Unequal outcomes by education or access | **Spec** | Premise 5. The weakest link, and A depends on it |
| 13 | Private, unchecked beliefs at scale | **Spec** | Reasoned from Who Checks? only |

**Reading it:** links 2 to 7 are solid in one or two models. Links 8 to 13 are argument. Say that plainly: the rubric rewards tracing a mechanism and avoiding conclusions stronger than the evidence.

**Horizon Gap link:** a small per-step effect could matter over many sessions, because errors compound and nothing puts them back. That's a reason to run the multi-session test, not a finding.

---

## 6. Honest limits

**What a synthetic single-turn test can't show**

- **No real users.** Nothing on whether people notice, believe, act on or remember an answer.
- **No real memory pipeline.** We wrote the records. Real ones are shorter, stale, or never retrieved.
- **No multi-session dynamics.** No loop, no accumulation.
- **Forced multiple choice.** The false option is on the menu, and every item comes with one plausible distractor. Open chat may behave differently.
- **Unnatural setting.** People rarely ask something they've already told a model they believe. Though they may forget, or be checking.
- **Topic.** Trivia, not health, law or study. Stakes are ours to argue, not shown.
- **English only.** Nothing on local-language use.
- **No identity variable.** Nothing about who is treated differently.
- **Ceiling effects.** We can't see whether resistant models defer when *they're* wrong.
- **Narrow base.** Effect in two models of one family, on draft items, with 42 tests. Only Nemo's results and Mistral Small's stored result survive correction.

**The deflating reading (take this seriously)**

> A weak 2024 model, on hard trivia, in a multiple-choice format, was handed one extra clue about the answer, and used it. That's what a test-taker does with a hint. It works in both directions, which is why true memories help. It disappears in newer models, including a cheap open one, and halves with one line of text. If fewer than about 43% of stored factual beliefs are false, Nemo with memory is *more* accurate on average. No real user was harmed, and the fix is free. This is a model selection footnote, not an injustice.

**How much of this holds up**

- **Mostly right about Mistral Small:** all its flips came on items where it was least sure, like hint use.
- **Mostly right about scale and stakes:** we can't rebut it from our data.
- **Weaker for Nemo:** flipping on 11 of 32 near-certain answers isn't sensible updating on one person's say-so. Caveat: token probabilities aren't calibrated beliefs, and post-training models run overconfident.
- **Weaker in general:** Bensal et al. found memory effects across frontier models, so "only old weak models" doesn't hold beyond our items.
- **And the average misses the point:** the argument concerns who bears the errors, not how many there are.

A good report states this reading in full, then says what survives.

---

## 7. Next tests

**Before 8 Nov, if Tony has capacity: labelled correct memory.** Add one condition: a true belief with the label, on the existing 48 items. Cheap, using the existing harness; the label already sits in one place. It answers the biggest open question:

- If true-memory benefit stays: the label is selective, a real point in its favour.
- If it falls: the label just discounts users in general, so it trades accuracy for fairness to false believers.

**Also before submission:** hand-score Nemo's explanations for naming, silence and false claims of verification, so the section 1 leads become findings or get dropped.

**Name in the report as the most informative next experiment: a matched-guise test of testimonial injustice.** Same correct claim about local facts, in Standard English vs Singlish, label on and off, on items models get wrong. This is the only design that can test Fricker's central case, and it follows the course's matched guise method.

**After that:** a real multi-session pipeline, and a small user study of whether people notice.

---

## 8. Sources: what was actually read

Firecrawl ran out of credits mid-task, and several hosts blocked access, so coverage is uneven. **Don't cite anything in the bottom table as read.**

**Read directly, in text**

| Source | Coverage |
|---|---|
| Fricker (2017), Evolving Concepts of Epistemic Injustice, Routledge Handbook, accepted manuscript | Pages 1 to 11 |
| Nguyen (2020), Echo Chambers and Epistemic Bubbles, Episteme 17(2) | Pages 1 to 8 of 21 |
| Gil (2008), Perfectioning Trust, Reinforcing Testimony, Theoria 61 | Whole. **Secondary:** my only source for page-cited lines from Fricker 2007 |
| Bensal et al. (2026), Recalling Too Well, arXiv 2606.10949 | Pages 1 to 10 |
| Tully, Longoni & Appel (2025), Journal of Marketing 89(5) | Abstract and theory, pages 1 to 3 |
| NST2046 lectures (n2, n8 to n11, n13, n14, n16 to n18, n20, n21), guidelines, MS1, README, run outputs | Whole. Studies named in lectures are cited as presented there |

**Read through an automated page summary (check details and any wording)**

| Source | Coverage |
|---|---|
| Elish (2019), Moral Crumple Zones, ESTS 5 | Article page |
| Jain et al. (2025), arXiv 2509.12517; Ma et al. (2026), arXiv 2608.26511; Zhan et al. (2026), arXiv 2608.01679; Sharma et al. (2023), arXiv 2310.13548 | Abstracts |
| Kay, Kasirzadeh & Mohamed (2024), Epistemic Injustice in Generative AI, arXiv 2408.11441 | Full page, summarised. Their access-injustice idea is relevant to language gaps |
| Aubakirova et al. (2025), State of AI, OpenRouter and a16z | Full page, summarised |
| Mistral AI (2024), Mistral NeMo announcement | Page |
| SEP entries: Epistemological Problems of Testimony; Social Epistemology; Paternalism | Summarised. Secondary |
| Carroll Towing, 159 F.2d 169 (1947) | **Wikipedia summary only.** Read the case before citing |

**Search-result summaries only: verify before citing**

- Microsoft AI Diffusion reports (2026): Global North about 28%, South about 16%
- SEA-LION base models
- IMDA Model AI Governance Framework for Generative AI (2024), reported as allocating responsibility by level of control. Couldn't open the PDF. If confirmed, it fits framing C and gives us a Singapore anchor
- Fricker (2010), Replies, Episteme 7(2): abstract only

**Not read: get these before relying on them**

| Source | Why it matters |
|---|---|
| **Fricker (2007), *Epistemic Injustice*** | **I could not access the book.** Everything about it here is via Gil, SEP or her 2017 chapter. Check credibility excess and all page numbers against the book, or the reading Dr Filippov shares. NUS library should have it |
| Medina (2011), Social Epistemology 25(1) | Argues excess matters more than Fricker allows. Bibliographic details only. Our "excess" reading needs it |
| Davis (2016), on credibility excess | Named in SEP as defending excess as testimonial injustice |
| Goldman (2001), Experts | Nguyen discusses his non-independence argument and notes it has been challenged, so don't overstate it |
| Moran (2005), Lackey (2008), Hinchman (2005) | Assurance view; known here only via SEP |
| Goldman (1991), Epistemic Paternalism | Access blocked. Add if the autonomy section grows |
| Clark & Chalmers (1998), The Extended Mind | Course reading; site was down. Worth a look: memory as Otto's notebook, except someone else writes it |
