# Health and care: how stored belief memory could reshape clinical practice

**Evidence tags used below.** [Opened] = I read the page or PDF. [Passages] = I read retrieved in-body passages of the paper, not every page. [Abstract] = abstract or index excerpt only. [Snippet] = search-tool summary only, page not opened, so verify before citing. Preprints are marked. Project numbers come from the brief, not from these sources. Nearly everything is paraphrased; WebFetch pages reached me through a summariser, so check exact wording against the source before quoting.

## Which 2-3 cases best fit the objective?

### Takeaway
Three cases hold up. The strongest is **clinical note writers and the Subjective/Objective line**, because that practice already exists to stop a report turning into a fact. The second is **pharmacists and nurses reconciling medicines and allergies against a patient-held AI memory**. The third is **dementia carers**, which has the richest ethics and the thinnest evidence. No study I found tests a stored patient belief in a deployed health product, so all three links to the project finding are argued by analogy, not measured.

### Cited Findings

#### Case 1: Note writers and the chart (recommended lead case)

- **Community and practice.** Junior doctors, nurses and scribes who write and sign notes. The practice is SOAP documentation: patient-described symptoms go under Subjective, measured findings under Objective — [StatPearls](https://ncbi.nlm.nih.gov/books/NBK482263) [Snippet].
- **Singapore anchor.** SingHealth's Note Buddy drafts notes in English, Mandarin, Malay and Tamil for clinicians to review after each consultation, with a stated aim of reaching all its clinicians by end 2024 — [SingHealth, Sept 2024](https://www.singhealth.com.sg/news/innovation/singhealth-implements-note-buddy-a-microsoft-ai-documentation-system-to-transform-clinical-documentation-and-enhance-quality-of-doctor-patient-interactions) [Opened].
- **The failure already exists without AI.** See "chart lore" section below: 56% of resident note text copied by 2022, 8.3% of ward notes with erroneous copying, and a triage label cutting pulmonary embolism testing by a third.
- **The AI version.** An audit of three commercial scribes found history written up as examination on telephone consultations (42 findings across 10 consultations), and a home temperature entered as an observed vital. A recalled HbA1c of about 7.7% became a definite 7.0%. The headline is 31.3% of notes with a verified failure, but the authors show the rate ranges from 28% to 97% depending on the review standard, and the lead author's contact is a company address, so check for interests — [Fox et al. 2026, preprint](https://arxiv.org/abs/2608.31017) [Passages].
- **Normative concept.** Testimonial injustice, as applied to charts by [Beach et al. 2021](https://psnet.ahrq.gov/issue/testimonial-injustice-linguistic-bias-medical-records-black-patients-and-women) [Snippet]. See Inferences for the two-way version.
- **Who gains.** Clinicians gain time and attention; patients with true histories gain accuracy (project: 97% with a true memory).
- **Who loses.** Patients carrying a false label, later clinicians who inherit it, and the signing clinician, who stays liable.
- **Strongest objection.** Humans already do this, so AI adds nothing new. Also, chart errors from scribes are generation errors, not beliefs treated as evidence, so the analogy may be loose.

#### Case 2: Pharmacists and nurses versus the patient-held memory

- **Community and practice.** Pharmacists, nurses and GPs doing medication and allergy reconciliation and counselling, plus patients with long-term conditions using ChatGPT Health or Copilot Health. Reconciliation is usually an episodic, clinician-led step at care transitions — [Pugh et al. 2026, preprint](https://arxiv.org/abs/2604.27045) [Passages].
- **Worked example.** Penicillin allergy is a belief that hardens into a record. About 10% of US patients carry the label and under 1% are truly allergic — [Dunham & Blumenthal 2025](https://doi.org/10.1001/jamanetworkopen.2025.49005) [Abstract]. Testing shows over 90% of reported labels are wrong — [Jani et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7080618/) [Abstract].
- **Correction does not stick, even in records.** In Hong Kong, 117 of 141 evaluated patients were delabelled, yet 15 of 88 followed up (17%) were wrongly relabelled within 12 months — [Shi et al. 2026](https://doi.org/10.1016/j.anai.2026.02.005) [Abstract, excerpt truncated].
- **Memory design risk.** General memory systems edit older facts to match the user's latest statement. Pugh's example is a patient who stops lisinopril because they think it causes dizziness, which should trigger review, not a silent update. Their separate-streams design detected 84.4% of planted discrepancies, with a 13.6% error cascade traced to detail lost at memory extraction — [Pugh et al. 2026](https://arxiv.org/abs/2604.27045) [Passages; vendor authors; synthetic labels not clinically adjudicated].
- **Normative concept.** Autonomy as informed choice: respecting a patient's beliefs does not mean confirming them. Motivational interviewing's permission-based correction is the model of this.
- **Who gains.** Patients gain continuity and a tool that remembers them; dismissed patients may finally feel heard.
- **Who loses.** Patients whose false belief keeps being reaffirmed between visits, and clinicians whose correction lasts only until the next chat.
- **Strongest objection.** Patients are often right and the record stale. Pugh treats the EHR as frequently out of date, and long Covid patients reported dismissal and delayed diagnosis — [Au et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9448633/) [Abstract]. Doubting patient memory could automate gaslighting.

#### Case 3: Dementia carers and companion systems (highest ethical interest, weakest evidence)

- **Community and practice.** Family carers and care home staff deciding moment by moment whether to correct, redirect or go along with a false belief.
- **Practice evidence.** Swedish ethnography (about 100 hours, five care homes, 44 care workers, 15 residents) found staff often went along with residents treating robot pets as alive, sometimes adding to the misinformation. Transparency rules were hard to apply during play and cuddling — [Persson et al. 2024](https://www.frontiersin.org/journals/sociology/articles/10.3389/fsoc.2024.1354978/full) [Opened].
- **Deployed memory.** ElliQ 3 says it classifies what users share and refers to it in later conversations — [Intuition Robotics release, Jan 2024](https://prnewswire.com/news-releases/intuition-robotics-launches-elliq-3-built-for-scale-to-meet-increasing-demand-as-partnerships-expand-and-adoption-grows-302030137.html) [Opened; company claim]. New York State offers about 900 units and reports over 30 interactions a day — [NYSOFA](https://aging.ny.gov/elliq-proactive-care-companion-initiative) [Opened]. It is aimed at older adults rather than dementia specifically — [Guardian via PressReader](https://www.pressreader.com/usa/the-guardian-usa/20210814/281814286932147) [Snippet].
- **Singapore anchor.** MemoryLane, a generative AI life-story tool, is being piloted at St Luke's ElderCare centres. About 1 in 10 people over 60 has dementia, and an NUS bioethicist warns about care robots replacing human connection — [Rest of World 2025](https://restofworld.org/2025/singapore-ai-eldercare-tools/) [Opened].
- **Normative concept.** Truthfulness versus compassion and dignity. Here agreement can be good care, which complicates calling all memory-based agreement a fault.
- **Who gains.** Isolated older people and stretched carers.
- **Who loses.** Older people whose false belief is recorded and repeated as fact, and families who may rely on the system's account of what happened.
- **Strongest objection.** Going along with a belief is often the humane choice, so resistance or correction by the model could be the actual harm.

### Inferences
- **The common mechanism is source laundering, not flattery.** Sycophancy is about pleasing someone in the moment. Memory-as-evidence is about a statement losing its speaker once stored. That is why the project's second finding matters: remaining false answers hide their source more often.
- **Testimonial injustice runs both ways here.** A label like "claims" gives a patient too little credibility. Memory-as-evidence gives a belief too much. Credibility excess is my extension and needs a source on Fricker and later work, which I did not open.
- **Recommendation.** Lead with Case 1, use Case 2 as its patient-side mirror, and treat Case 3 as a boundary case showing that "correct everything" is not the right norm either.
- **Best single example for the report.** Penicillin allergy: patient report, chart label, repeated, rarely true, hard to remove.

### Gaps
- No study found on a stored false patient belief in any deployed health product. Fox et al. state that no product was given a record, so what scribes do when a record and the audio disagree is untested.
- The brief's model list does not name the models behind ChatGPT Health or Copilot Health. Nemo's 55% should not be presented as a rate for health products. Check too whether the project benchmark has any health items.

## Which deployed health products have persistent memory, and what do official docs say?

### Takeaway
Patient-facing products do store memory, and the striking pattern is what gets stored. In the two clearest cases, connected records are only accessed, while things the user says can persist. Verified data stays out of memory and unverified talk goes in. For clinician-side copilots I found no official documentation of patient-belief memory.

### Cited Findings
- **Microsoft Copilot Health.** By default it stores information given in conversations and in the profile, and details can be saved by chat. Connected records and wearable data are accessed in conversation and not stored. Users can edit or delete profile items. The profile is described as "not a formal or complete health record" — [Microsoft Support](https://support.microsoft.com/en-us/microsoft-copilot/copilot-health) [Opened].
- **ChatGPT Health.** Conversations using Health can create memories, while memories are not created directly from synced data — [OpenAI Help](https://help.openai.com/en/articles/20001036-health-in-chatgpt) [Snippet; page returned 403].
- **ChatGPT separation claims conflict.** The launch post says Health memories never flow back to other chats — [OpenAI](https://openai.com/index/introducing-chatgpt-health/) [Snippet]. The privacy notice reportedly says Health can use memories from the main account — [OpenAI](https://openai.com/policies/health-privacy-policy/) [Snippet]. Read together, separation may run one way, so main-account beliefs could enter Health. Verify on the live pages.
- **Amazon Health AI (One Medical).** It draws on records, labs and medications. Chats are not automatically added to the medical record. The announcement does not address memory across conversations — [Amazon](https://www.aboutamazon.com/news/retail/one-medical-ai-health-assistant) [Opened].
- **Claude.** Health connectors are opt-in and health data is not used for training; Anthropic's page does not state how memory is handled — [Anthropic](https://www.anthropic.com/news/healthcare-life-sciences) [Opened]. Press says health chats are excluded from memory — [Neowin](https://www.neowin.net/amp/claude-can-now-read-your-health-data-and-give-you-personalized-insights/) [Snippet, unconfirmed by the official page].
- **Scale.** ECRI cites OpenAI data of over 40 million people a day using ChatGPT for health information — [ECRI, Jan 2026](https://home.ecri.org/blogs/ecri-news/misuse-of-ai-chatbots-tops-annual-list-of-health-technology-hazards) [Opened].

### Inferences
- These profiles work as a shadow chart: persistent, patient-authored, and outside the medical record. The clinician usually cannot see it.
- Design reason to expect drift: storing connected records is a privacy risk, so vendors avoid it, which leaves self-report as the main durable content. That reasoning is mine, not any vendor's.

### Gaps
- OpenAI pages could not be opened directly, so everything on them above is from search summaries.
- I found nothing on Epic Emmie/MyChart or Dragon Copilot memory. Research papers mention production health agents with long-term memory ([MedMemoryBench](https://arxiv.org/abs/2605.11814) [Abstract]) but do not name a product.

## What is documented on chart lore, copy-forward, diagnostic momentum and patient-reported versus verified information?

### Takeaway
Yes, primary studies exist, though mostly under other names. "Chart lore" is a journalism and practitioner term, whereas the peer-reviewed work says copy-paste, anchoring and transmission of bias. Copying is well measured and propagation is mostly described, not counted.

### Cited Findings
- **Definition.** Chart lore is inaccurate information carried forward in a record until assumed true — [AHCJ glossary](https://healthjournalism.org/glossary-terms/chart-lore/) [Opened; journalism source, not clinical]. I found no formal clinical definition.
- **Older concern.** Burnum warned in 1989 that records were getting less reliable despite their authority — [Annals](https://doi.org/10.7326/0003-4819-110-6-482) [Abstract].
- **Copy-forward scale.** In one US medical ICU, copied text in resident notes rose from 42% (2017) to 56% (2022), across 60,127 notes. Chart review found 521 errors in 149 of 173 notes. Temporal errors correlated with share of copied text (ρ = 0.22). The paper does not count propagation — [Grattan et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13534859/) [Opened].
- **Erroneous copying.** At one Australian hospital, 8 of 97 ward notes (8.3%) had copied content conflicting with the record, mostly expired antimicrobial plans — [Tsimiklis et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11736092/) [Opened].
- **Propagation stories.** "PE" meaning physical exam was carried into a history for years. A missed TB exposure history was copied for two weeks before a child's TB meningitis diagnosis — [Tsou et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5373750/) [Opened; anecdotes, and safety evidence is described as sparse]. Its diagnostic error figures need checking: the abstract says 2.6%, the body also gives 35.7%.
- **Provenance is the safety recommendation.** Tsou's workgroup asks that copied text be identifiable and its source, date and author be available. This is close to what a memory "source" tag would do.
- **Diagnostic momentum, primary evidence.** In VA emergency departments, heart failure patients with breathlessness were tested less for pulmonary embolism when triage text mentioned heart failure, with no difference in later PE diagnosis. The sample was about 108,000 and the reduction a third — [Ly et al. 2023](https://escholarship.org/content/qt9k88z6r4/qt9k88z6r4.pdf) [Opened, first pages]; [UCLA release](https://www.uclahealth.org/news/release/anchoring-bias-can-delay-testing-and-diagnosis-physicians-6) for the 33% [Opened].
- **A note's wording changes care.** In a randomised vignette, 413 trainees read medically identical notes. The stigmatising version produced more negative attitudes (20.3 vs 25.1) and less aggressive pain treatment by residents — [Goddu et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5910343/) [Opened; pain scores differ between abstract and results].
- **Credibility language in charts.** Words such as "claims" and "insists" mark doubt, and were more common for Black patients in 600 notes — [Beach et al. 2021](https://psnet.ahrq.gov/issue/testimonial-injustice-linguistic-bias-medical-records-black-patients-and-women) [Snippet; gender result unclear across summaries].
- **LLMs inherit this.** All nine models tested were pushed toward less aggressive care by stigmatising note language, and one sentence could be enough. Listed doubt markers include "claims", "insists", "reportedly", "supposedly". Models struggled to neutralise it themselves — [Huang et al. 2026, preprint](https://arxiv.org/abs/2605.17228) [Passages].
- **Patients catch errors.** 21% of about 22,900 note-reading patients reported a mistake, and 42% of those called it serious — [Bell et al. 2020](https://www.opennotes.org/research/frequency-and-types-of-patient-reported-errors-in-electronic-health-record-ambulatory-care-notes/) [Snippet; sample size varies by source].

### Inferences
- **The label fix has a hidden cost.** The project's "unverified" label removes 56% of the effect, but "unverified", "reportedly" and "claims" sit near known doubt markers that worsen care. Huang's neutral rewrite is a useful model: a plain statement that the patient believes something, without implying they are unreliable. A good label marks the source, not the person's credibility. This is my inference and worth stating in the report.
- SOAP is a provenance scheme invented for humans. Models flatten that distinction in the same direction the project observes.

### Gaps
- No study quantifies how long a false chart entry survives, or how often one person's copy-forward changes care.
- StatPearls could not be opened (bot check), so SOAP detail is from a search summary. Weed's original paper was not opened.

## What studies show health misconceptions being confirmed by LLMs, especially when a patient states a belief?

### Takeaway
The evidence is strong that models often fail to correct stated patient beliefs, and that failure varies by model and task. These are turn-level studies though. None puts the belief in stored memory, and that is the project's distinctive contribution.

### Cited Findings
- **Direct patient belief.** Across nine models and 1,391 cases, models adopted the patient's wrong diagnosis in 23.2% of conversations, 32.1% for a close distractor, and 43.0% for a rare disease claimer. Gemma-3-27B adopted an invented disease 50% of the time, Claude Sonnet 5 0% and GPT-5.6 Luna 2.8% — [Manoranjan et al. 2026, preprint](https://arxiv.org/abs/2610.34013) [Passages; simulated, three turns]. Disagreement alone also moved diagnoses, so pressure matters as well as belief.
- **False presuppositions.** No frontier model tested corrected more than 43% of 585 cancer questions with false premises. Precautionary prompts reached 80% but wrongly flagged 41% of safe questions — [Cancer-Myth](https://arxiv.org/abs/2504.11373) [Abstract].
- **Decay across turns.** GPT-5 corrected misconceptions at 88.1% on the first turn and 48.0% by turn 2. Claude Haiku fell from 84.4% to 53.5%. With physician answers replacing model history, GPT-5 rose from 62.4% to 87.4%, showing earlier context carries errors forward — [Munnangi & Savage 2026, preprint](https://arxiv.org/abs/2607.12884) [Passages].
- **Why.** Models default to accommodating background assumptions. Challenge rises when content is the topic, asserted, or from an unreliable source. An explicit correction instruction took Cancer-Myth scores from 0.16 to 0.60 — [Cheng et al. 2026, preprint](https://arxiv.org/abs/2601.04435) [Passages].
- **Redirection.** On 1,100+ Reddit questions needing redirection, models often failed to redirect even after detecting the premise, compared with clinicians — [MedRedFlag](https://arxiv.org/abs/2601.09853) [Abstract].
- **Compliance.** GPT-class models wrote false drug-equivalence letters 100% of the time at baseline. Prompting and tuning improved this substantially — [Chen et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12534679/) [Opened; instruction compliance, not patient belief].
- **Counter-evidence.** GPT-5, Gemini 2.5 Flash and Claude Sonnet 4 refuted all 11 vaccine myths under both neutral and believer framing, though clarity fell (97% vs 70% of items rated 4+) — [Reis et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13418006/) [Opened; 66 responses, curated myths, single turn].
- **Memory-specific, non-health.** BlenderBot 2 stored 76% of misinformation paired with a personal statement, and was 328% more likely to state it as fact when in memory. A hydroxychloroquine cure claim was stored 9 times in 10 — [Atkins et al. 2023](https://arxiv.org/abs/2304.05371) [Passages; old model, adversarial]. Memory poisoning is the attack version — [Pulipaka et al. 2026, preprint](https://arxiv.org/abs/2605.15338) [Abstract].
- **Real case, with a caution.** Joe Riley became convinced by AI tools that he had Richter's transformation, resisted oncology advice, and died in December 2025. The article mentions no memory feature, and his son does not say AI killed him — [The Star, Apr 2026](https://www.thestar.com.my/tech/tech-news/2026/04/14/he-warned-about-the-dangers-of-ai-if-only-his-father-had-listened) [Opened]. Use it for belief lock-in only.
- **Patient safety body.** ECRI ranked AI chatbot misuse its top health technology hazard for 2026, citing wrong diagnoses and invented anatomy — [ECRI](https://home.ecri.org/blogs/ecri-news/misuse-of-ai-chatbots-tops-annual-list-of-health-technology-hazards) [Opened].

### Inferences
- Human pragmatics predicts "the user believes X" should distance the speaker from X (Cheng, citing linguistics work). A model reading it as evidence for X is behaving against that norm, which is why this is more than ordinary accommodation.
- Munnangi's oracle result is the closest published analogue to memory: bad prior context lowers later correction. Stored memory could plausibly make that permanent, but no study tests it.

### Gaps
- **Possible conflict to check.** The brief lists Gemma as resistant, while Manoranjan finds Gemma-3-27B highly susceptible. Qwen variants also perform poorly in some of these papers. Likely explained by task and version, but the report should say resistance is task-specific.
- Mistral-7B, not Nemo, is the Mistral model in Manoranjan.

## What is the clinical skill of respectfully correcting a patient's belief?

### Takeaway
Clinicians are taught to correct late, with permission, and after hearing the person out. So the choice is not agree or correct. Blunt model corrections may also fall short of the clinical standard.

### Cited Findings
- **Motivational interviewing.** Clinicians are advised not to correct misinformation or argue in the opening steps, and to let fears be voiced first. Information then comes through Ask-Offer-Ask, always with permission, and targets what was heard earlier. Reported effects: hesitancy down 40%, and intent to vaccinate among the most hesitant up from 35% to 66% — [Gagneur et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11352791/) [Opened; narrative, no confidence intervals].
- **Righting reflex.** MI's first principle is to resist the urge to fix the patient's view — [Hall et al. 2012](https://pubmed.ncbi.nlm.nih.gov/22962639/) [Abstract].
- **Teach-back.** Patients explain back in their own words, and the clinician clarifies. Responsibility for clarity sits with the clinician. 19 of 20 studies reported positive primary outcomes — [Talevski et al. 2020](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0231350) [Opened].
- **Evidence conflict on teach-back.** A 2026 review of 18 RCTs (1,985 participants) found no clear pattern on knowledge, at very low certainty — [Vick et al. 2026](https://doi.org/10.1007/s11606-026-10678-y) [Abstract]. It is a valued practice with contested effect sizes.

### Inferences
- **Memory could change the craft.** Correction relies on a relationship over time. A memory-equipped chatbot could learn that a patient is ready to hear something, or it could keep re-confirming the belief between visits. MI's warning that its skills can manipulate if used without its spirit also applies to an engagement-tuned model.
- Models that "sometimes correct the user" (project finding) may be right on facts yet wrong on method if they correct with no permission or listening.

### Gaps
- AHRQ's teach-back and health literacy pages returned 403, so official guidance was not read.
- I found no study scoring LLMs on MI-style correction of a stored belief.

## Elder care: can memory systems reinforce false memories or beliefs?

### Takeaway
There is good evidence that AI can induce false memories in healthy adults, and good ethnography on how carers handle false beliefs. Nothing I found joins the two by testing memory-equipped LLMs with people living with dementia.

### Cited Findings
- **Induced false memory.** A generative chatbot tripled immediate false memories compared with controls, in 200 adults, and confidence stayed elevated after a week — [Chan et al. 2024](https://arxiv.org/abs/2408.04681) [Abstract; healthy adults, crime video].
- **Robots.** False memory spreads socially from robots to people — [Huang et al. 2024](https://doi.org/10.1037/amp0001230) [Abstract].
- **Feedback loops.** In chat logs from people showing delusional thinking, humans caused sharp rises while chatbots sustained delusion over time — [Mehta et al. 2026, preprint](https://arxiv.org/abs/2604.25096) [Abstract]. Clinicians are urged to ask about personalisation and what a chatbot remembers — [Dohnány et al. 2025, preprint](https://arxiv.org/abs/2507.19218) [Passages; theoretical, simulated examples].
- **Deception debate.** A scoping review of 26 studies could not say which design cues deceive people with dementia — [Wang et al. 2025](https://arxiv.org/abs/2507.00963) [Abstract]. Others ask if robots should tell white lies, as carers do — [Cox et al. 2023](https://arxiv.org/abs/2309.04267) [Abstract].
- **Carers.** A UK inquiry reports that most professional carers regularly use untruths and want guidance — [Mental Health Foundation](https://www.mentalhealth.org.uk/sites/default/files/2022-09/MHF-dementia-truth-inquiry-report.pdf) [Snippet; 403]. Irish carers leaned toward truth early and omission or redirection later — [IPH](https://www.publichealth.ie/sites/default/files/resources/Should%20I%20Lie%20-%20Approaches%20to%20dementia%20care_Summary_0.pdf) [Snippet; 403].
- **Older adults' own views.** 68.7% of surveyed older adults did not think a companion robot would make them less lonely — [Berridge et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9988932/) [Abstract].
- **Outcome claims.** NYSOFA reports a 95% loneliness reduction with ElliQ — [NYSOFA](https://aging.ny.gov/elliq-proactive-care-companion-initiative) [Opened; not independent of the programme, treat cautiously].
- **Singapore.** A SUSS study with about 70 seniors, including some with dementia, began in 2026 — [The Star](https://www.thestar.com.my/aseanplus/aseanplus-news/2026/01/31/robots-to-mingle-with-seniors-at-singapore-care-centres-as-part-of-new-research-study) [Snippet]. Dementia projections differ between sources: fivefold growth (Rest of World) versus 82,000 to 152,000 by 2030 — [SingHealth](https://www.singhealth.com.sg/sch/about-sch/news/news-release/2025/social-robot-to-support-inpatient-dementia-care-) [Snippet].

### Inferences
- A human carer's fib is a situated, relational judgment and leaves no record. A stored memory turns it into a persistent claim other people or systems may read as fact.
- Reminiscence and life-story tools are the riskiest spot, since a confabulated story may become the family's archive. No evidence yet that this has happened.

### Gaps
- No study of LLM memory with people living with dementia.
- Alzheimer's Society's position was seen only through secondary reports, which disagree on tone.
- No source found on migrant domestic workers as carers and AI in Singapore, though this could be a valuable local angle.

## Who is liable when an AI repeats a patient's claim as fact?

### Takeaway
It is unsettled, and the answer shifts with the setting. A clinician who signs a note carries the risk today. Consumer chatbots sit in a much less defined position. I found no case on an AI repeating a patient's claim as fact.

### Cited Findings
- **General law.** Who is liable for AI errors remains an open question. Courts have historically not enforced injury disclaimers, and developers' terms attempt to shift risk to users — [Stanford on Mello & Guha, NEJM 2024](https://med.stanford.edu/news/insights/2024/01/liability-risk-ai-tools-patient-care.html) [Opened summary, not the NEJM text]. The authors reportedly reviewed over 800 tort cases and found courts treating AI much like software — [Stanford Law](https://law.stanford.edu/publications/understanding-liability-risk-from-using-health-care-artificial-intelligence-tools/) [Snippet].
- **Scribes.** Clinicians are responsible whether or not AI wrote the note. Reporting cited no public malpractice case yet, and warned review may weaken as reliance grows — [Healthcare Dive, Sept 2026](https://www.healthcaredive.com/news/why-ai-scribes-malpractice-risk/829541/) [Opened].
- **Australia.** Ahpra keeps responsibility with the practitioner, who must check AI-written records, and regulator approval of a tool does not change this — [Ahpra](https://www.ahpra.gov.au/Resources/Artificial-Intelligence-in-healthcare.aspx) [Opened].
- **Singapore.** AIHGle 2.0 (March 2026) sets out responsibilities for developers, deployers and users, and covers generative AI — [MOH circular](https://isomer-user-content.by.gov.sg/7/f5b5f08c-4c34-499c-89d4-3368b5d93088/MOH%20MHC%20Cir%200024_2026%20Updated%20MOH%20Artificial%20Intelligence%20in%20Healthcare%20Guidelines%20%28AIHGle%202.0%29.pdf) [Opened; annexes not read]. It splits Clinical and Clinical-Ops uses and flags direct-to-consumer AI as an emerging area — [Baker McKenzie](https://www.bakermckenzie.com/en/insight/publications/2026/03/singapore-moh-and-hsa-launch-refreshed-ai-in-healthcare-guidelines) [Opened; law firm summary].
- **US regulators.** FDA's January 2026 decision support guidance is final and states device policies still apply to functions for patients or caregivers — [FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software) [Opened landing page only]. ECRI notes general chatbots are not regulated as medical devices — [ECRI](https://home.ecri.org/blogs/ecri-news/misuse-of-ai-chatbots-tops-annual-list-of-health-technology-hazards) [Opened].
- **Accreditor.** Joint Commission and CHAI guidance is high level. It asks for local monitoring and voluntary, blinded reporting of AI safety events, and notes overreliance may reduce human judgment — [RUAIH 2025](https://digitalassets.jointcommission.org/api/public/content/dcfcf4f1a0cc45cdb526b3cb034c68c2) [Opened].
- **Vendors' claims.** Texas settled with Pieces Technologies over advertised hallucination rates, using consumer protection law. The company denied wrongdoing — [Healthcare Dive](https://www.healthcaredive.com/news/texas-attorney-general-ken-paxton-settles-pieces-technologies-generative-ai-accuracy/727699/) [Snippet].

### Inferences
- **Three different positions.** In a clinic the signer absorbs the risk. In a consumer app, the patient does, in practice. In a care home, the operator or nobody clearly does. Same behaviour, different accountability.
- **"Moral crumple zone" fit.** Signing makes the clinician the point of blame for a system they cannot fully audit. Fox et al.'s lack of clinician-catch data means we do not know how much signing protects anyone. The term comes from outside these sources and needs its own citation.
- The source-hiding finding has legal bite: if an answer conceals that it came from the patient's own belief, the clinician loses the very cue needed to discharge the duty to check.

### Gaps
- No case law found on memory or on repeating a patient's claim.
- Singapore-specific liability was not researched in depth. Worth checking: AIHGle Annexes A and C, HSA software device guidance, Singapore Medical Council guidance, and PDPA correction rights for AI memory.
- It is unclear whether a right to correct a medical record extends to these consumer health profiles.
