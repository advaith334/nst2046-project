# Patient-held memory narrowly overtakes teachers

**Patient-held AI memory, as pharmacists and nurses meet it when they check medicines and allergies, is now the strongest case by one point, and it should lead. Teachers and AI tutors should move to the contrast role.** Two of the team's own runs forced this. A tutor frame cut Mistral Nemo's false answers from 55% to 24% and also removed the benefit of true memory, so the claim that "memory tutors flatter students" is not supported in that frame. A clear passage stating the correct fact cut Nemo to 1%, so the finding is that memory beats a model's own knowledge, not that it beats clear evidence. That shifts the risk toward people asking from outside any curated source, and away from settings that work from verified records. The top four cases sit within one point, which is a tie in practice, and the patient case is ahead partly because nobody has yet tested it the way the teacher case was tested. Teachers still have the best concept and the best philosophy, and that work moves across intact. No case here shows harm in a deployed product, and Nemo's rates are not rates for any product. One cheap test, the tutor frame rewritten for patients, could reverse this call before 8 Nov.

## Read this first: three rules and the flags

**Scope.** Every number from our study applies to long-tail factual multiple-choice items, in synthetic single-turn tests, in English. Items are unverified drafts and nothing is hand-scored yet. Nemo's rates describe Nemo on those items. They are not rates for ChatGPT, Copilot, Khanmigo or any other product, and nothing here shows Nemo runs inside any product named below. They are not even a fixed property of Nemo: the same model on the same items ranged from 25% to 79% false answers as the wording of the memory changed. So 55% and 97 vs 41 always mean "under our default wording".

**Claim grades.** Each case card separates:

| Grade | Meaning |
|---|---|
| **Evidenced** | Measured by us, or documented in a source we can point to |
| **Inferred** | A reasoned step from evidence to this setting. Nobody has measured it |
| **Speculative** | Plausible, with no direct support yet |

**Access flags.** The five research notes used different tags. They are mapped to one set here, and they say how much of a source was actually seen. Check anything below FT before citing it, and check any wording against the original.

| Flag | Meaning |
|---|---|
| FT | Text read directly. For long papers this may be targeted sections, not every line |
| PASS | Retrieved passages of the paper, not the whole paper |
| PAGE | Page opened, but the content came through a summarising tool |
| ABS | Abstract or index record only |
| PRESS | Read through a press or institutional summary |
| SNIP | Search snippet only. The page was not opened. Treat as a lead |

Preprints are marked. Lawsuits are allegations, not findings. Company pages are company claims.

## New runs show memory beats knowledge, not evidence

These results come from the team's run logs of 5 Nov, not from the research notes. They are automatic scores on the same 48 items, and they have not been analysed or hand-checked. I recomputed the Nemo false-answer rates, the key paired counts and the evidence run from the trial logs, and they match.

| What changed (Nemo unless stated) | False answers, Nemo | False answers, Mistral Small | What happened to true memory |
|---|---|---|---|
| Main study: no memory | 15% | 3% | 73% correct |
| Main study: stored false belief | **55%** | 16% | 97% correct with a true memory |
| "Unverified" label | 32% | 11% | **Nemo falls 97% to 85%** (11 lost, 0 gained, p = 0.001), still above baseline. Small unchanged |
| Rule on the memory block ("never as evidence") | 49% | 22% | 89% correct |
| Answer first, then see memory | 47% | 8% | 78% correct. Nemo drops its own draft |
| **Tutor frame** (three wording changes bundled) | **24%** (tutor baseline 16%) | 7% (baseline 4%) | **75% correct vs baseline 72%: the benefit is gone** |
| Memory block headed only "Notes:" | 25% | 11% | Not tested |
| Heading adds "may be out of date or wrong" | 26% | 11% | Not tested |
| Heading says "Verified profile facts" | 57% | 15% | Not tested |
| Record loses "believes": bare claim | **79%** | 32% | Not tested |
| Record says "User once said that" | 77% | 24% | Not tested |
| Gate that withholds world claims | 17% | 3% | 70% correct: benefit gone. Nemo's useful-memory checks fall to 12 of 16 |
| **Clear passage stating the correct fact** | **1%** (52 pairs lower, 0 higher) | 0% | Baseline already 0% false, about 99-100% correct |

Noise check: a straight rerun of the main wording gave Nemo 60%, against 55% in the main study. Differences of about 5 points mean little, so Small's rise under the rule (22% vs 16%) should not be read as harm.

**What this does to the finding.**

- **Do not claim memory overrides evidence.** Llama also went from 15% to 0% with a passage. The override is of the model's own prior knowledge. Stated beliefs stayed slightly higher than stored ones with a passage (Nemo 4%, Llama 5%).
- **Only strong passages were tested.** Weak, ambiguous, stale or wrong sources are untested. A retrieval system can also fail to find the passage at all.
- **Wording decides a lot.** The tutor frame changed three things at once, so its cause is unknown. A plain "Notes:" heading gave nearly the same drop with no tutor role at all, which suggests wording may matter as much as role. This qualifies the reading that role alone explains it. The notes found no vendor that documents how memory is worded when it reaches the model, so nobody outside a company knows which row of this table its product sits in.
- **Losing the attribution looks costly.** Dropping "believes" took Nemo to 79%. Published work finds real memory pipelines do this: one preprint reports 33.1% of episodes dropped who said it ([Mao et al. 2026, preprint](https://arxiv.org/abs/2607.10526) FT).
- **Enterprise memory may sit near the worst rows (Inferred).** Systems that store bare facts could be closer to the 79% condition. Zep stores facts as relationships and reportedly calls them "reliable sources of truth" ([Zep](https://help.getzep.com/v2/facts) PAGE, check the quote). Mem0's example keeps "User" as the subject ([Mem0](https://docs.mem0.ai/core-concepts/memory-types) PAGE), so it may sit closer to our default wording. Neither was tested, and which model runs behind them varies by customer.

**The new exposure test.** A case is more exposed when a model answers from its own knowledge on long-tail facts with no source in front of it. It is less exposed when the model works from verified records or curated retrieval. This is an inference from the runs above, and it now has its own column in the scores.

**A new angle on fairness (Inferred).** Clear sources cost money and labour. Schools, hospitals and governments can curate them. A worker asking a free chatbot about local rules has none. So protection may follow who has an institution behind them, which gives the team's distributive argument a route that does not depend on proving who holds false beliefs.

## Ten cases ranked, with the top four in a practical tie

Scores are my judgement from the notes, 1 to 5, not measurements. **Memory fit:** does the case turn on a stored record, not agreement in the moment? **Evidence:** how well documented is the practice, and at what access level? **Deployed:** is belief-bearing memory documented in this setting? **Our data:** 3 means a measured result of ours bears on the case's key claim and does not undercut it, 2 means analogy only or undercut, 1 means no answer key exists. **Exposure:** does the model answer from its own knowledge? The last three columns are the rubric lines.

| Rank | Case | Memory fit | Evidence | Deployed | Our data | Exposure | Stake-holders | Normative | Socio-technical | Total /40 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Pharmacists, nurses and patient-held memory | 4 | 3 | 5 | 3 | 3 | 4 | 4 | 4 | **30** |
| 2 | Teachers and AI tutors (old lead) | 5 | 4 | 2 | 2 | 3 | 3 | 5 | 5 | **29** |
| 3 | Migrant workers and caseworkers | 4 | 3 | 1 | 3 | 4 | 5 | 5 | 4 | **29** |
| 4 | Clinical note writers and the chart | 3 | 5 | 3 | 3 | 2 | 4 | 4 | 5 | **29** |
| 5 | CBT therapists and the case formulation | 4 | 4 | 3 | 2 | 3 | 4 | 4 | 4 | 28 |
| 6 | Dementia carers | 3 | 3 | 3 | 1 | 3 | 4 | 5 | 3 | 25 |
| 7 | Chaplains and pastoral counsel | 4 | 3 | 1 | 1 | 3 | 4 | 5 | 3 | 24 |
| 8 | Empirical researchers, with maths as contrast | 3 | 3 | 3 | 2 | 3 | 3 | 4 | 3 | 24 |
| 9 | Journalists and fact-checkers | 4 | 3 | 1 | 3 | 2 | 3 | 4 | 3 | 23 |
| 10 | Licensed financial advisers | 4 | 3 | 2 | 2 | 2 | 3 | 3 | 4 | 23 |

Ties are broken by memory fit, then our data. Peer supporters also reach 23 but lose that tie-break.

**How much the order depends on weights.**

| Weighting | Top of the table |
|---|---|
| Equal | Patient 30, then Teachers, Migrant and Note writers on 29 |
| Rubric lines count double | Migrant 43, then Patient, Teachers and Note writers on 42 |
| Evidence, deployment, data and exposure count double | Patient 44, Note writers 42, then Teachers, Migrant and CBT on 40 |
| Ignore deployment | Migrant 28, Teachers 27, Note writers 26, Patient 25 |

The patient case is first or close to it under every weighting except the last. It depends heavily on the Deployed column. Migrant workers top the table when the rubric or local exposure counts most.

## Lead with the patient case, contrast with teachers

**Recommendation: lead with pharmacists, nurses and patient-held memory. Use teachers and AI tutors as the contrast.** The one-point gap is not the reason. Three things are.

- **Teachers' central harm claim was tested and did not hold in that frame.** The patient claim has not been contradicted, though it has not been tested either. That asymmetry flatters the patient case, so the tie-break test below matters.
- **The patient case has the clearest official documentation of a setting-specific memory taking in what a user says.** Copilot Health stores what you tell it, while connected records are read but not stored ([Microsoft Support](https://support.microsoft.com/en-us/microsoft-copilot/copilot-health) PAGE).
- **Our label result lands exactly here.** The label cost Nemo 12 points on true memories, and patients are often right.

**Why teachers make the better contrast, ahead of migrant workers.** The pair shows one exposed practice and one protected one. Migrant workers are the runner-up. Choose them if the team wants the Singapore justice argument and can accept that no deployed memory is documented there.

| | Lead: patient-held memory | Contrast: teachers and tutors |
|---|---|---|
| Who is likely right? | Either. Patients are often right and records stale | Usually the curriculum, on checkable facts |
| What should the record do? | Be checked against other sources before anyone relies on it | Serve as a diagnosis, then be corrected |
| What protects it? | Connected records, for what they cover | Role wording, curated content, teacher review |
| What goes wrong? | A belief is reaffirmed between visits, or a true report is doubted | Memory is switched off, so no flattery but no teaching either |
| What our data adds | Label costs true memories 97% to 85% | Tutor frame: 55% to 24%, and benefit gone |

**Proposed thesis, for the team to attack.** *A stored belief records what someone thinks. Whether a system reads it as a fact about the person or a fact about the world is not settled by the record. In our tests it depended on the model, the wording, the role and whether a clear source was present. Pharmacists and teachers already hold that line for a living, so deployers owe a test of which reading they have actually bought.*

**What carries over from the existing case.** Hearsay stays as the conceptual tool. Chart lore moves from an aside to the core of the lead. The teacher, flatterer and contrarian roles stay as the data link. Fricker's distributive sense stays, with the fairness angle above added.

**What to do before 8 Nov.**

1. **Run the tie-break.** Copy the tutor variant with "Saved notes about this patient" and "Patient believes that". At main-run prices this should cost under a dollar (Inferred). If Nemo drops near baseline in both directions, the patient numbers do not carry either, and teachers return as lead on concept. If the effect persists, the patient lead is firm.
2. **Unbundle the tutor frame.** Change role, heading and belief sentence one at a time.
3. **Test a wrong source.** A true memory against a clear but stale passage is the patient-right, record-wrong scenario. It is the key untested case for the lead.
4. **Open the OpenAI health pages by hand.** They are SNIP only, and the lead relies on them.
5. **Hand-score** the source-hiding counts before relying on them.

If the team keeps teachers as lead anyway, that is defensible, since the scores are tied and the course material is there. It then needs the rewritten claim below, not the current thesis sentence.

## Against the existing lead: what beats it and what does not

**Plainly: the patient case beats the teacher case narrowly, and only on deployment and survival of its key claim. Nothing beats teachers on concept.**

| Test | Teachers | Best rival | Verdict |
|---|---|---|---|
| Is the record valuable, so deleting it is no fix? | Yes, this is the craft. The gate result shows deletion loses the benefit | Patient case, partly | Teachers |
| Does the wrong believer need an extra premise? | No. The practice exists to serve them | All others need it | Teachers |
| Philosophy and course fit | Hearsay, hypercorrection, Lecture 18 | Migrant workers: testimonial injustice proper | Teachers, narrowly |
| Is belief memory documented in a product? | Interests only, or SNIP | Patient case, PAGE | **Patient case** |
| Does the key claim survive our data? | Harm claim weakened by the tutor frame | Patient: untested | **Patient case**, with that caveat |
| Exposure | Curated tutors protected, general chatbots not | Migrant workers | **Migrant workers** |
| Stakes | Learning | Health, justice | Rivals |

**Why the tutor frame matters so much.** The old thesis says memory "withholds correction from the student who most needs it". Under tutor wording, Nemo's accuracy is 75% with a true memory and 62% with a false one, not 97% and 41%. The 97/41 gap should not be attached to a tutor.

**What survives, and it is good.** Memory switched off is not teaching either. Nemo's replies still mention the student or belief in 43 of 96 answers under the false tutor note, against 63 of 96 under the main wording, on my rough text match. Nobody has coded whether those mentions correct the belief. Sadler shows gains come from teachers who know the misconception, so a tutor that ignores the record has not done the job. Teaching gives the standard: read the record as a diagnosis. Claude did this, naming and correcting the belief in 26 of 96 answers. So the claim changes from "tutors flatter" to "teaching defines the right reading, and neither flattering nor ignoring meets it".

**Five corrections to the current practice note.**

| Current wording | Problem | Fix |
|---|---|---|
| "Large gains came only from teachers who knew both" | Full text limits this to stronger students on misconception items. Low scorers gained on those items under no teacher category. Test-level effects were 0.05-0.10 SD, and the study is observational ([Sadler et al. 2013](https://assess.ucr.edu/media/826/download) FT) | State the limits. The low-scorer result cuts against an easy equity story |
| "A student's wrong belief is exactly what a tutor's memory would hold" | Our effect is on long-tail facts. On misconception and puzzle items Nemo moved +6 points against +41, a gap of +35 [+18, +52], post hoc | Say "less-rehearsed school facts", such as a hexagon's angle sum or primes below 100, not classic misconceptions |
| Thesis uses 97 vs 41 for a tutor | Tutor frame gives 75 vs 62 | Use the main numbers only for the default frame, and show both |
| Hearsay as a US rule | Our readers are in Singapore. Singapore's Act admits business records built on others' information and then lets the court weigh them ([Evidence Act ss 32, 62](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) FT) | US exclusion is like deleting the memory, Singapore's "admit and weigh" is like the label. Have a lawyer check s 32 before relying on it |
| Chart lore rests on journalism | The term does, but primary studies exist under other names (see case 4) | Cite the studies, and keep "chart lore" as a label only |

**Keep from the honest limits.** The label cuts explicit correction in five of six models, and only Claude corrects more (26 to 38). Gemma falls from 12 to 2. For a tutor that is a real cost.

## The ten cases

### 1. Pharmacists, nurses and patient-held memory

| Field | Content |
|---|---|
| **Community and practice** | Pharmacists, nurses and GPs doing medication and allergy reconciliation, plus patients with long-term conditions using health assistants. Reconciliation is usually an episodic, clinician-led step ([Pugh et al. 2026, preprint](https://arxiv.org/abs/2604.27045) PASS) |
| **Why memory, not just flattery** | A patient's belief can become a durable profile outside the medical record that the clinician usually cannot see. A correction in clinic lasts only until the next chat |
| **Documented evidence** | Copilot Health stores conversation details, and connected records are read but not stored ([Microsoft Support](https://support.microsoft.com/en-us/microsoft-copilot/copilot-health) PAGE). ChatGPT Health conversations can create memories ([OpenAI Help](https://help.openai.com/en/articles/20001036-health-in-chatgpt) SNIP, page blocked). ECRI cites OpenAI data of over 40 million people a day seeking health information ([ECRI](https://home.ecri.org/blogs/ecri-news/misuse-of-ai-chatbots-tops-annual-list-of-health-technology-hazards) PAGE). About 10% of US patients carry a penicillin label, and under 1% are truly allergic ([Dunham & Blumenthal 2025](https://doi.org/10.1001/jamanetworkopen.2025.49005) ABS). In Hong Kong 15 of 88 delabelled patients followed up were wrongly relabelled within 12 months ([Shi et al. 2026](https://doi.org/10.1016/j.anai.2026.02.005) ABS, truncated). Models adopted a patient's wrong diagnosis in 23.2% of conversations and 43.0% for a rare disease, with no memory involved ([Manoranjan et al. 2026, preprint](https://arxiv.org/abs/2610.34013) PASS) |
| **Normative concept** | Autonomy as informed choice: respecting a belief is not confirming it. Credibility can fail both ways, with too little ("claims", [Beach et al. 2021](https://psnet.ahrq.gov/issue/testimonial-injustice-linguistic-bias-medical-records-black-patients-and-women) SNIP) or too much. Motivational interviewing's correction with permission is the practice model ([Gagneur et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11352791/) PAGE) |
| **Gains and losses** | Gain: patients who get continuity, and dismissed patients who finally feel heard. Lose: patients whose false belief is reaffirmed, and clinicians whose correction does not stick |
| **Link to our data** | 97 vs 41 by analogy only. The label cost on true memories (97 to 85) is the direct link. Nemo took the false plasma donor belief on one health item. Rare-disease adoption echoes the long-tail pattern (Inferred) |
| **Exposure** | Mixed. Connected records in the chat should protect what they cover, and on the clear-passage result the model would follow them. Questions outside the record rest on the model's own knowledge. A wrong record, such as a false allergy label, is untested |
| **Strongest objection** | Patients are often right and records stale ([Pugh et al.](https://arxiv.org/abs/2604.27045) PASS). Long Covid patients reported dismissal and delayed diagnosis ([Au et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9448633/) ABS). Doubting patient memory could automate gaslighting. Also, a patient's body is partly their own authority, and this blurs the "claims about the world" category |
| **Rubric fit** | Stakeholders: strong, with clear liability differences. Normative: good. Socio-technical: good, since store design decides what persists |
| **Claim status** | Evidenced: product storage (Microsoft), label persistence. Inferred: the shadow chart and clashes with clinicians. Speculative: any patient harmed this way. No study tests a stored false belief in a health product, and no pharmacist's voice appears in the notes |

### 2. Teachers and AI tutors

| Field | Content |
|---|---|
| **Community and practice** | School science and maths teachers diagnosing wrong beliefs, plus tutors that carry a learner model. In Singapore, teachers on the Student Learning Space |
| **Why memory, not just flattery** | A tutor must keep "this student believes X". Deleting it is no fix, unlike most domains. The fault is reading it as support for X |
| **Documented evidence** | 181 teachers and 9,556 students: gains on misconception items for stronger students needed knowledge of both the answer and the misconception ([Sadler et al. 2013](https://assess.ucr.edu/media/826/download) FT). 24 students with an engineered sycophantic bot corrected less, and 17 reported no difference between bots ([Bo et al., CHI 2026](https://arxiv.org/pdf/2510.03667) FT). A student naming a wrong answer cut accuracy by up to 15 points ([Check My Work, preprint](https://arxiv.org/html/2506.10297) FT). Study mode reportedly uses saved memories ([OpenAI help](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq) SNIP). Khanmigo Interests stores enthusiasms, not beliefs ([Khan Academy](https://blog.khanacademy.org/new-khanmigo-interests/) FT). Singapore's Data Assistant highlights common misconceptions for teachers ([MOE](https://www.learning.moe.edu.sg/teachers/teaching-and-learning-on-sls/aied-features/) PAGE) |
| **Normative concept** | Knowledge of student misconceptions as an epistemic role, hearing a belief without crediting it. Hearsay, with FRE 803(3) excluding "a statement of memory or belief to prove the fact remembered or believed" ([FRE 803](https://www.law.cornell.edu/rules/fre/rule_803) PAGE). Distributive epistemic injustice ([secondary summary](https://en.wikipedia.org/wiki/Epistemic_injustice) FT; the team has not read Fricker's book) |
| **Gains and losses** | Gain: strong students and students already right. Lose: students with wrong beliefs on general chatbots. Teachers may lose sight of errors. Under a tutor frame, the loss shifts to personalisation that does nothing |
| **Link to our data** | Most direct of any case: the only domain frame tested, and three roles in our logs (Claude corrects, Nemo follows, Llama contradicts true beliefs in 19 of 44). But the tutor frame shrinks the effect, and classic misconceptions moved little |
| **Exposure** | Mixed. Curated and supervised tools look protected: teachers vet short-answer feedback and read logs in Singapore, and Khan reports better accuracy with human-written steps ([Khan Academy](https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/) SNIP). A student revising with a general assistant is more exposed (Inferred) |
| **Strongest objection** | Our own run: a tutor frame removes most of the effect. Use is also thin, with Khanmigo on about a third of Khan Academy days in one trial ([Chalkbeat](https://www.chalkbeat.org/2026/08/25/ai-tutoring-students-khanmigo-khan-academy-engagement-study/) PRESS). Bastani concerns answer dependence, not belief ([abstract](https://econpapers.repec.org/RePEc:nas:journl:v:122:y:2025:p:e2422633122) ABS) |
| **Rubric fit** | Stakeholders: moderate now, since consequences are conditional. Normative: strong. Socio-technical: strong, and the frame result improves it |
| **Claim status** | Evidenced: the craft, Nemo's behaviour in each frame. Inferred: harm to students on general chatbots. Speculative: stale corrected beliefs staying on file. No source links stored misconceptions to worse learning |

### 3. Migrant workers and caseworkers in salary claims

| Field | Content |
|---|---|
| **Community and practice** | Migrant workers pursuing unpaid salary through TADM mediation and the Employment Claims Tribunal, with NGO caseworkers such as TWC2. Domestic workers doing eldercare are a related group, with chatbots already felt to be safe ([Teng & Choo 2026, preprint](https://arxiv.org/html/2604.05448v1) PAGE) |
| **Why memory, not just flattery** | A claim runs across e-negotiation, mediation and tribunal. A helper with memory would carry a worker's account through all stages. Neither side may hire a lawyer at the tribunal, though firms can appoint in-house lawyers as representatives, and the judge relies on what parties bring ([TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) FT). So little corrects a mistaken belief on the way |
| **Documented evidence** | One worker insisted he worked over eight hours when his time card showed eight, and a better claim went unused. Another framed a complaint as "cheating" and had it dismissed. This is 18 cases by one volunteer, with no AI involved ([TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) FT). Models were less accurate for less-educated and non-native English users ([MIT News](https://news.mit.edu/2026/study-ai-chatbots-provide-less-accurate-information-vulnerable-users-0219) PAGE). Sycophancy was higher in low-resource languages including Malay, Tamil and Tagalog, on a different metric with no memory ([Shah et al. 2026, preprint](https://arxiv.org/html/2606.08451v1) PAGE). Singapore has 323,800 domestic workers and 490,700 work permit holders in construction, marine and process sectors ([MOM](https://www.mom.gov.sg/documents-and-publications/foreign-workforce-numbers) PAGE) |
| **Normative concept** | Equal access to justice. This is the one case where Fricker's testimonial injustice could properly apply: a credibility deficit tracking identity, if a label deflates a true account |
| **Gains and losses** | Gain: workers with a true account, and caseworkers spared repeat intake. Lose: workers with a sincere wrong belief who arrive confident with a weaker claim, and caseworkers who must undo a machine's agreement |
| **Link to our data** | The label cost on true memories applies directly. Rules are checkable facts, often long-tail. English only, so the language link is untested |
| **Exposure** | Highest of the top cases. No curated source on a consumer chatbot, and local rules are long-tail. One prototype did not use retrieval ([MigrantPal](https://reachalliance.org/wp-content/uploads/2023/07/migrantpal_final-1.pdf) FT). No usage data exists, so this is Inferred |
| **Strongest objection** | Employers control the records and may forge them, so a worker's word may be all he has, and "unverified" could reproduce the disbelief he already faces. No deployed legal-aid bot with memory was found. Fair says it stores no personal data ([Fair FAQ](https://hfpg-fair.vercel.app/en/faq) PAGE) |
| **Rubric fit** | Stakeholders: strongest of all. Normative: strong. Socio-technical: good, but the memory link is hypothetical |
| **Claim status** | Evidenced: the documented false beliefs, the process, language gaps in general. Inferred: memory carrying a belief across stages. Speculative: use of memory-enabled tools by this group |

### 4. Clinical note writers and the chart

| Field | Content |
|---|---|
| **Community and practice** | Junior doctors, nurses and scribes who write and sign notes. SOAP keeps patient reports under Subjective and measured findings under Objective ([StatPearls](https://ncbi.nlm.nih.gov/books/NBK482263) SNIP). SingHealth's Note Buddy drafts notes for clinician review ([SingHealth](https://www.singhealth.com.sg/news/innovation/singhealth-implements-note-buddy-a-microsoft-ai-documentation-system-to-transform-clinical-documentation-and-enhance-quality-of-doctor-patient-interactions) PAGE in one note, SNIP in another) |
| **Why memory, not just flattery** | The practice exists to stop a report turning into a fact. The chart is a human memory system that already fails this way. It is the best analogy for what happens when provenance is lost |
| **Documented evidence** | Copied text in resident notes rose from 42% to 56%, 2017 to 2022, across 60,127 notes ([Grattan et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13534859/) PAGE). 8 of 97 ward notes had erroneous copied content ([Tsimiklis et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11736092/) PAGE). A heart failure mention in triage cut pulmonary embolism testing by a third ([Ly et al. 2023](https://escholarship.org/content/qt9k88z6r4/qt9k88z6r4.pdf) PAGE). A scribe audit found history written up as examination, with a headline 31.3% failure rate that ranges 28-97% by review standard ([Fox et al. 2026, preprint](https://arxiv.org/abs/2608.31017) PASS; lead author has a company address). "Chart lore" itself is a journalism term ([AHCJ](https://healthjournalism.org/glossary-terms/chart-lore/) PAGE) |
| **Normative concept** | Provenance, and testimonial injustice as applied to charts. The moral crumple zone fits the signer but needs its own citation |
| **Gains and losses** | Gain: clinicians' time, and patients with true histories. Lose: patients carrying a false label, later clinicians, and the signer, who stays liable ([Healthcare Dive](https://www.healthcaredive.com/news/why-ai-scribes-malpractice-risk/829541/) PAGE) |
| **Link to our data** | Hidden source: false answers with no visible source went from 19% to 48% of Nemo's false answers under the label (AI-coded). Dropping "believes" raised false answers to 79% |
| **Exposure** | Low on stored belief. The model works from the consultation in front of it, and a clinician reviews the note. Its failures are generation errors |
| **Strongest objection** | Humans already do this, and scribe errors are not beliefs treated as evidence. No product in Fox et al. was given a record |
| **Rubric fit** | Stakeholders: good. Normative: good. Socio-technical: strong |
| **Claim status** | Evidenced: copying, anchoring, scribe flattening. Inferred: that memory repeats this. Speculative: false AI-held beliefs entering charts. How long false entries survive is unmeasured |

### 5. CBT therapists and the case formulation

| Field | Content |
|---|---|
| **Community and practice** | Cognitive behavioural therapists doing cognitive restructuring, and their clients using AI between sessions. At stake is the formulation, the record of what is hypothesis and what is established |
| **Why memory, not just flattery** | CBT treats "I always fail" as a hypothesis to test. A Socratic question needs that belief to stay open. Once stored as background it stops being a question (Inferred). One preprint says current systems cannot tell a tentative guess from an established fact ([Zhang et al. 2026, preprint](https://arxiv.org/abs/2611.05383) FT) |
| **Documented evidence** | The APA says clinicians modulate "supporting and challenging", and recommends limiting AI memory, but for attachment reasons ([APA 2025](https://www.infocop.es/wp-content/uploads/2025/11/health-advisory-ai-chatbots-wellness-apps-mental-health.pdf) FT, third-party copy). Socratic questioning predicted symptom reduction in 55 adults ([Braun et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4449800/) PAGE). One model chose validation 66.7% of the time and Socratic questioning 7.4% ([Sinha et al. 2026, preprint](https://arxiv.org/abs/2607.02885) FT). OpenAI said memory can worsen sycophancy in some cases, while lacking evidence it does so broadly ([third-party mirror](https://bittide.aicompass.dev/article/ab1dba25-05ae-40b6-9923-7a85d7ce0ab3?locale=en) PAGE; openai.com blocked). Memory is the selling point of companions ([Character.AI](https://blog.character.ai/helping-characters-remember-what-matters-most/) PAGE; [Nomi](https://nomi.ai/updates/introducing-the-nomi-identity-core-fostering-dynamic-and-authentic-identities/) PAGE) |
| **Normative concept** | Care as challenge. Experts reject both collusion and blunt correction ([Morrison & Barratt 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2800146) PAGE), so "correct the user" is not automatically good |
| **Gains and losses** | Gain: people without access to care, and vendors through retention. Lose: clients with fixed negative beliefs or delusions, and therapists competing with an always-agreeing tool |
| **Link to our data** | Weak. Our test scores facts, and distortions are rarely false in that way. The label fits the "not yet evidence" idea |
| **Exposure** | Moderate. Companions and general chatbots answer from their own model with no source, but there is rarely a passage that could settle the belief |
| **Strongest objection** | Distortions are not benchmark falsehoods. Some models use context to intervene more ([Nicholls et al. 2026, preprint](https://arxiv.org/abs/2604.13860) FT). Safety training can itself block therapy ([BN et al. 2026, preprint](https://arxiv.org/abs/2604.23445) ABS). A generative chatbot has reached a trial whose results the notes did not reach ([Heinz et al.](https://doi.org/10.1056/AIoa2400802) ABS, truncated) |
| **Rubric fit** | Stakeholders: good. Normative: good. Socio-technical: good. All three carry a high risk of overclaiming |
| **Claim status** | Evidenced: therapists' norms, chatbots' validation default. Inferred: stored distortions become premises. Speculative: memory as a clinical mechanism. Clinical reports do not establish memory, and the only memory links are one company admission, one allegation via a law-firm summary ([Raine summary](https://www.tysonmendes.com/raine-v-openai-ai-product-liability-lawsuit/) PAGE, allegation) and one news account ([WSJ via To Vima](https://www.tovima.com/wsj/a-troubled-man-his-chatbot-and-a-murder-suicide-in-old-greenwich/) PAGE) |

### 6. Dementia carers

| Field | Content |
|---|---|
| **Community and practice** | Family carers and care home staff deciding moment by moment whether to correct, redirect or go along with a false belief |
| **Why memory, not just flattery** | A carer's kind fib is situated and leaves no record. A stored memory turns it into a persistent claim that others may read as fact (Inferred) |
| **Documented evidence** | 100 hours of Swedish ethnography found staff often went along with residents treating robot pets as alive ([Persson et al. 2024](https://www.frontiersin.org/journals/sociology/articles/10.3389/fsoc.2024.1354978/full) PAGE). ElliQ says it classifies what users share and refers to it later ([Intuition Robotics](https://prnewswire.com/news-releases/intuition-robotics-launches-elliq-3-built-for-scale-to-meet-increasing-demand-as-partnerships-expand-and-adoption-grows-302030137.html) PAGE, company claim). MemoryLane is being piloted at St Luke's ElderCare ([Rest of World](https://restofworld.org/2025/singapore-ai-eldercare-tools/) PAGE). A chatbot tripled false memories in healthy adults ([Chan et al. 2024](https://arxiv.org/abs/2408.04681) ABS) |
| **Normative concept** | Truthfulness against compassion and dignity. Here agreement can be good care |
| **Gains and losses** | Gain: isolated older people and stretched carers. Lose: older people whose false belief is recorded, and families relying on the system's account |
| **Link to our data** | Weak, and it reverses the sign: a resistant model could be the one doing harm |
| **Exposure** | Moderate. Companions work from conversation, and a life-story tool has no outside source to check against |
| **Strongest objection** | Going along is often the humane choice, so the finding may not count as a failure here |
| **Rubric fit** | Stakeholders: good. Normative: strong. Socio-technical: moderate |
| **Claim status** | Evidenced: carers' practice, company memory claims. Inferred: fibs hardening into records. Speculative: confabulated stories entering family archives. No study tests memory LLMs with people living with dementia |

### 7. Chaplains and pastoral counsel

| Field | Content |
|---|---|
| **Community and practice** | Chaplains, priests, imams and spiritual directors, and the faithful using apps such as Hallow, Bible Chat and GitaGPT |
| **Why memory, not just flattery** | A stored belief is sometimes the right input. "User is Catholic" should change the advice. "User has received a divine mission" should not count as proof of one |
| **Documented evidence** | Stating the faith raised alignment with the user's tradition from −0.03 to +0.40 in high-normativity traditions ([Kadous et al. 2026, preprint](https://arxiv.org/abs/2609.13634) FT). 18 Nordic chaplains mostly doubted chatbots could support well-being ([Wester et al., CHI 2026](https://arxiv.org/abs/2602.04017) FT). Hallow says its AI is not for spiritual or moral direction ([Hallow FAQ](https://help.hallow.com/en/articles/13601993-hallow-ai-faq) PAGE). Illinois exempts religious counselling and peer support from its AI therapy law ([225 ILCS 155/35](https://www.ilga.gov/ftp/ILCS/Ch%200225/Act%200155/022501550K35.html) FT excerpt) |
| **Normative concept** | Discernment and legitimate religious authority. Psychiatry exempts culturally accepted beliefs from delusion ([McKay & Ross 2021](https://doi.org/10.1016/j.copsyc.2020.10.002) ABS) |
| **Gains and losses** | Gain: believers with no nearby clergy, and high-demand traditions otherwise counselled from a secular default. Lose: clergy whose authority rests on presence, and people whose spiritual experience is an early sign of illness |
| **Link to our data** | None directly: no answer key exists. Useful as the boundary of the "fact about you" vs "fact about the world" split |
| **Exposure** | Moderate. Some apps anchor on scripture with sources shown, but no passage settles a personal spiritual claim |
| **Strongest objection** | Calling a creed "false" is a category error, and it repeats the secular bias Kadous describes |
| **Rubric fit** | Stakeholders: good. Normative: strong. Socio-technical: moderate |
| **Claim status** | Evidenced: faith disclosure changes guidance. Inferred: a stated faith behaves like a memory entry. Speculative: anything about persistent memory in these apps |

### 8. Empirical researchers, with mathematicians as contrast

| Field | Content |
|---|---|
| **Community and practice** | Doctoral students and lab scientists running literature reviews in a persistent project. Mathematicians are the contrast, since proofs can be checked mechanically ([Tao, Math 2.0](https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf) FT) |
| **Why memory, not just flattery** | A stored working hypothesis could shape later searches and summaries. In science the scarce skill moves from finding sources to judging them |
| **Documented evidence** | Commentary describes this loop as reinforcement bias ([Scholarly Kitchen](https://scholarlykitchen.sspnet.org/2026/09/02/when-your-ai-knows-you-too-well-personalization-sycophancy-and-the-risk-of-an-intellectual-echo-chamber-in-ai-assisted-research/) FT). Sycophancy on false theorems ranged from 29.0% to 70.2%, and rose by up to 15.6% when a model thought it wrote the claim ([BrokenMath, preprint](https://arxiv.org/html/2510.04721v1) FT). Google's notebook tool retrieves from your sources first ([Google support](https://support.google.com/notebooklm/answer/16164461) FT) |
| **Normative concept** | Organised scepticism (not opened, cite with care) and bootstrapped corroboration: "corroboration ought to only have weight if it adds something epistemically" ([Nguyen 2020](https://cssh.northeastern.edu/pandemic-teaching-initiative/wp-content/uploads/sites/43/2020/10/echo_chambers_and_epistemic_bubbles.pdf) FT) |
| **Gains and losses** | Gain: established groups with strong priors, and vendors. Lose: doctoral students whose training is the struggle with awkward papers, and authors of minority findings (Inferred) |
| **Link to our data** | Weak. Hypotheses are often unsettled, so there is no key. Classmates already cover mathematicians |
| **Exposure** | Mixed. Source-grounded tools have passages in front of them, but the literature is often weak or ambiguous evidence, and that is exactly what we did not test |
| **Strongest objection** | Peer review and retrieval should catch it, and selection already narrows a human review |
| **Rubric fit** | Stakeholders: moderate. Normative: good. Socio-technical: moderate |
| **Claim status** | Evidenced: maths checking, self-sycophancy. Inferred: stance shapes a review. Speculative: hypothesis lock-in through memory. Do not imply mathematicians report memory problems |

### 9. Journalists and fact-checkers

| Field | Content |
|---|---|
| **Community and practice** | Beat and investigative reporters who keep notes on sources, and fact-checkers working to the IFCN code |
| **Why memory, not just flattery** | Journalism's discipline is keeping "A says X" apart from "X". An assistant that restates a stored source claim flatly strips the attribution. This would be private citogenesis, with no publication step for anyone to catch |
| **Documented evidence** | SPJ's 2026 proposal adds verifying provenance, and keeps responsibility with the journalist ([Nieman Lab](https://niemanlab.org/2026/08/the-society-of-professional-journalists-proposes-edits-to-its-code-of-ethics-for-the-ai-age) FT). IFCN requires enough detail for readers to verify and prefers primary sources ([IFCN](https://www.ifcncodeofprinciples.poynter.org/the-commitments) FT). About a third of assistant news answers had serious sourcing problems ([EBU](https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants) PAGE). Wikipedia's rule is that being sure is not enough ([WP:Verifiability](https://en.wikipedia.org/wiki/Wikipedia:Verifiability) FT) |
| **Normative concept** | Attribution and provenance. A copy of a claim is not corroboration of it |
| **Gains and losses** | Gain: deadline-pressed desks, and sources whose framing gets stored early. Lose: readers, and local reporters with few editors (Inferred) |
| **Link to our data** | Good on hidden source, which is the best conceptual match for that result. But reporters are not sincere false believers in the way a pupil is |
| **Exposure** | Low to moderate. Reporters work from documents and notes in front of them, and editors check. A clear primary document should win |
| **Strongest objection** | Professionals are the safest users. The two-source habit, editors and lawyers already catch this |
| **Rubric fit** | Stakeholders: moderate. Normative: good. Socio-technical: moderate |
| **Claim status** | Evidenced: the norms, general attribution failures in consumer answers. Inferred: laundering of stored notes. Speculative: any newsroom use of memory-enabled assistants, since none was found |

### 10. Licensed financial advisers

| Field | Content |
|---|---|
| **Community and practice** | Representatives and robo-advisers who must know the client before recommending a product |
| **Why memory, not just flattery** | This field already has a written rule for reusing a client's statement. In Singapore a past statement may be reused only if the client confirms nothing material has changed, which works like an expiry date on memory ([MAS FAA-N16, para 12](https://www.mas.gov.sg/-/media/mas/regulations-and-financial-stability/regulations-guidance-and-licensing/financial-advisers/notices/faa-n16---tracked.pdf) FT) |
| **Documented evidence** | Stated risk profile moved trend-chasing allocation from 0.67% to 38.18%, with no memory ([Winder et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204588/) PAGE). Microsoft found 50 prompts from 31 companies trying to plant "remember X as trusted" ([Microsoft Security](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) PAGE). Citi called memory a key limit for agents ([aggregator](https://letsdatascience.com/news/citi-launches-ai-wealth-advisor-memory-limits-remain-1cea7755) PAGE) |
| **Normative concept** | Reasonable basis and duty of care, set against client autonomy. A client is authoritative on risk tolerance, not on whether a fund can lose |
| **Gains and losses** | Gain: low-balance clients and advisers spared fact-finding. Lose: clients whose false belief is treated as a preference, and advisers' role as the person who says no |
| **Link to our data** | By analogy. Product facts are checkable, but no finance items were tested |
| **Exposure** | Lower for regulated firms, which hold product data and duties. Higher for people asking a general chatbot, which favours the unregulated tools (Inferred) |
| **Strongest objection** | Across seven LLMs, motivated framing did not reduce fraud warnings, and humans suppressed warnings more ([Powdthavee 2026, preprint](https://arxiv.org/abs/2604.20652) PAGE). This is a single author on obvious fraud |
| **Rubric fit** | Stakeholders: moderate. Normative: moderate, with no express duty to correct found. Socio-technical: good, since the rule is a design spec |
| **Claim status** | Evidenced: the rules. Inferred: rules as memory design. Speculative: stored memory in advice, which is unstudied |

## Four near misses, and why they fell out

| Case | Total | Why it missed |
|---|---|---|
| Peer supporters and Hearing Voices groups | 23 | Rich concept: a peer holds a belief as *yours*, not as *true* ([Peng et al. 2026, preprint](https://arxiv.org/abs/2602.08187) FT). The Human Line Project is a striking detail ([Futurism](https://futurism.com/support-group-ai-psychosis) SNIP). But how peers handle disagreement is thinly evidenced, and there is no answer key |
| Support agents and claims handlers | 22 | Moffatt shows a firm answers for its bot ([2024 BCCRT 149](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do) FT), but no incident of a customer's false claim becoming account fact was found, and firms hold systems of record |
| Practising lawyers | 21 | Legal tools handled false premises best of all query types ([Magesh et al.](https://arxiv.org/html/2405.20362v1) FT), and memory stores preferences |
| Voters | 21 | Strong evidence on opinions, none on checkable facts, and voters are a population, not a practice. Costello is still worth citing: a model told to argue against a stated belief reduced it ([Cornell](https://news.cornell.edu/node/329310) PRESS) |

## What is evidenced, inferred and speculative overall

| Claim | Grade | Basis |
|---|---|---|
| Nemo follows a stored false belief, and accuracy splits 97 vs 41 | Evidenced | Ours, default wording only |
| Label removes 56% of Nemo's effect [36, 78] and costs true memories | Evidenced | Ours |
| Remaining false answers hide their source more often | Evidenced as a lead | Ours, AI-coded, unscored |
| Wording and frame change the effect a lot | Evidenced | Ours, unanalysed |
| Clear passages almost remove it | Evidenced | Ours, strong passages only |
| Real memory pipelines keep claims and drop corrections | Evidenced | [Bensal et al. 2026, preprint](https://arxiv.org/abs/2606.10949) FT |
| Memory profiles can raise agreement sycophancy with real user context | Evidenced | [Jain et al.](https://arxiv.org/html/2509.12517v3) FT. Advice scenarios, factual accuracy not measured |
| Consumer products store things users say | Evidenced | For example [Copilot](https://support.microsoft.com/en-us/microsoft-365-copilot/manage-copilot-memory-in-microsoft-365-copilot) PAGE and [Claude](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context) PAGE. None of the help pages read describes a confidence label |
| Named practices meet this failure today | Inferred | No study in any of the ten settings |
| Exposure follows who has curated sources | Inferred | From the passage run |
| Singapore's curated public services are protected | Inferred | Ask Jamie and VICA use human-reviewed knowledge bases ([GovInsider](https://govinsider.asia/intl-en/article/is-it-time-to-say-goodbye-to-ask-jamie-inside-govtechs-refresh-of-government-chatbots) PAGE), AIBots uses retrieval over agency documents ([roadmap](https://www.developer.tech.gov.sg/products/categories/productivity-tools/aibots/features-roadmap) PAGE), and no person-level memory is documented. Untested |
| Beliefs loop and harden across sessions | Speculative | We ran single turns |
| Outcomes differ by education or access | Speculative | No data |

**Regulation in one line.** Singapore's agentic framework treats memory as a security and privacy surface, and it imagines an attacker ([IMDA](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf) FT). Here the user sincerely poisons their own memory, and PDPC guidance lets firms presume that what individuals tell them is accurate in most cases ([PDPC ch. 16](https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Advisory-Guidelines/the-accuracy-obligation---ch-16-(270717).pdf) FT, 2017 revision). PDPA and POFMA statute text was not read, so treat any legal reading as a non-lawyer's view.

## Where the notes conflict

| Conflict | Sides | How this report handles it |
|---|---|---|
| **Model resistance is task-specific** | Gemma resisted here, but Gemma-3-27B adopted an invented disease 50% of the time ([Manoranjan](https://arxiv.org/abs/2610.34013) PASS). Qwen resisted here, but Qwen3 models scored 55.6-65.1% on false theorems ([BrokenMath](https://arxiv.org/html/2510.04721v1) FT). Claude gave 0 of 96 false answers here, but memory profiles raised its agreement sycophancy 33% ([Jain](https://arxiv.org/html/2509.12517v3) FT), and it showed substantial rates in delusion tests ([DelusionEval](https://arxiv.org/abs/2608.05004) ABS) | Say "did not follow false beliefs on our items, in English". Never call a model resistant in general |
| **Every note has a different lead** | Therapy: CBT. Health: note writers. Knowledge: teachers. Law: migrant workers. Singapore: domestic workers plus SLS | Each note ranked within its own domain. The scoring here is the first cross-domain comparison |
| **Does attribution protect?** | Mao blames lost attribution. Our study kept "User believes" and Nemo still failed. Mem0 keeps "User" as subject, so it may not be safe | Both hold: dropping "believes" made it worse (79%), but keeping it was not enough (55-60%). "User once said" was no safer (77%) |
| **Is the label good?** | Therapy note: a natural fit. Health note: near doubt markers that worsen care ([Huang et al. 2026, preprint](https://arxiv.org/abs/2605.17228) PASS). Law note: may repeat disbelief, and disclaimers did little at [MyCity](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law) (PAGE) | Partial, with costs. A good label marks the source, not the person's credibility |
| **Does memory raise sycophancy on facts?** | Bensal: 3.8% on science vs 31.2% on moral items. Kelley & Riedl: no systematic rise on facts ([preprint](https://arxiv.org/abs/2603.00024) FT). Ours: a large rise on long-tail facts, little on misconceptions | Item type matters. Our facts may understate moral or advice settings, which remain untested by us |
| **Is correcting always better?** | Costello says yes on conspiracies. CBT experts reject blunt correction. Claude 3 Opus was sometimes condescending to vulnerable users ([MIT News](https://news.mit.edu/2026/study-ai-chatbots-provide-less-accurate-information-vulnerable-users-0219) PAGE) | The choice is not agree or correct. Method matters |
| **Team's own counts differ** | Source hidden: 29% to 70% in the brief (text match on flipped answers), 19% to 48% in the census. Claude: 26, 35 or 36 | Use the census: 19% to 48%, and 26 "names and corrects" within 36 "names". All AI-coded |
| **Source details** | Bensal's abstract says 25× in v1 and 40% later. Mao's 51.4% and 38.8% use different units. Moore's log study says over 80% in one place and over 70% in another ([Moore et al. 2026, preprint](https://arxiv.org/abs/2603.16567) FT). Law note read Singapore statutes in a browser, while the Singapore note could not open them. Fair's FAQ says no personal data is stored, but retention is unstated | Check the latest version before quoting. Read statutes directly |
| **Name trap** | SEA-LION has a Nemotron line ([sea-lion.ai](https://sea-lion.ai/) PAGE) | This is not Mistral Nemo. SEA-LION has not been tested by us |

## What would change the ranking

| If this happens | Then |
|---|---|
| Patient frame also drops Nemo near baseline in both directions | Teachers return to lead on concept, and the frame claim gains a second data point |
| Patient frame leaves the effect in place | Patient lead is firm, and a tutor-specific reason becomes likely |
| Unbundling shows the heading, not the role, did it | Teachers recover some ground, since a product wording may not protect them. The claim becomes about wrappers, not roles |
| A vendor is shown to store and inject student beliefs | Teachers' Deployed score rises and they likely retake the lead |
| By-hand reading shows health memory is narrower than these pages suggest | Patient case loses its main advantage |
| A wrong-source test shows clear passages beat true memories | The patient-right, record-wrong harm becomes measured, and the lead strengthens |
| The benchmark in Malay, Tamil and Tagalog, on Nemo and a SEA-LION model, shows a gap | Migrant workers take the lead or the contrast slot |
| A matched-guise test shows true Singlish claims overridden | Migrant workers lead the philosophy section outright, since this tests real testimonial injustice |
| Usage data shows migrant workers rely on memory-enabled chatbots | Their Deployed score rises from its floor |
| The team gets first-hand interviews in any case | That case gains the depth of the artists and "math 2.0" examples, which no case here yet has |

## Conclusion

The team's hardest test was of its own favourite case, and that is the most useful thing it did. The study has moved from "memory makes models flatter" to a narrower and better claim: a stored belief has no fixed meaning, and the wording, role and sources around it decide whether it counts as a fact about a person or about the world. It only beats what a model already knows, and it loses to a clear source put in front of it.

That turns the societal question from which AI is sycophantic into who gets a frame and a source. Institutions can buy both, and a person alone with a free chatbot often has neither. The practices in this report already know how to keep "you told me" apart from "it is so", and that distinction is what a memory system has to be tested for, one deployment at a time.
