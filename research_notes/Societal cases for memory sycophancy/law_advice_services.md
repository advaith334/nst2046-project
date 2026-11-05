# Memory as evidence in law, legal aid, financial advice and customer service

How to read the source tags:

- **[read]**: I read the source text myself (statute, decision, PDF text or paper passage).
- **[opened]**: I opened the page, but its content reached me through a fetch summariser. Check the wording before quoting it.
- **[snippet]**: search-result summary only. The page was not opened. Open it before citing it in the report.

Scope caveat: the group's finding (Mistral Nemo 15% to 55% false answers; 97% vs 41% accuracy; "unverified" label removes 56% of the effect; remaining false answers hide their source more often; Claude, Gemma and Qwen resist) comes from the brief. None of the sources below test stored memory in a legal, financial or service setting. Every link from them to memory is my inference, and it is marked as one.

## Objective: which 2-3 cases should the report use?

### Takeaway
Use three cases, in this order: (1) migrant workers bringing salary claims in Singapore, (2) licensed financial advisers and retail clients, (3) support agents and claims handlers, as a shorter case. Hearsay works as the shared concept across all three. Practising lawyers are a weak stand-alone case, because their tools resist false premises well and their memory products store preferences rather than beliefs.

### Cited Findings

#### Case 1: Migrant workers and their caseworkers in Singapore's salary-claim system (recommended lead)

**Community and practice.** Migrant workers pursuing unpaid salary through TADM mediation and the Employment Claims Tribunal (ECT), with NGO caseworkers such as TWC2 alongside them.

**Why memory-as-evidence matters here, not just sycophancy**
- The process runs over several stages: e-negotiation, mediation, then the ECT, with a one-year limit on claims — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read]. A helper with memory would carry a worker's account across all of them (inference).
- Neither side may hire a lawyer for the ECT, so the worker presents his own case. The report notes companies can still appoint in-house lawyers as representatives — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read].
- The judge relies on the evidence the parties bring and does not investigate on his own initiative — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read]. So nobody downstream reliably corrects a mistaken belief before it reaches the tribunal (inference).
- The false belief is documented, not hypothetical. One worker kept insisting he worked over eight hours when his time card showed eight, and a better claim (unpaid basic salary) went unused — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read].
- Another worker framed a complaint as "cheating" and had it dismissed, when an unlicensed-agency complaint would have fitted — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read].

**Documented evidence**
- TWC2's study covers 18 cases plus interviews and is by one volunteer, so treat it as qualitative. It does not mention AI — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read].
- Fair is a free legal-information chatbot for migrant workers from Hack for Public Good, in English, Bengali, Burmese and Chinese. It is described as a work in progress, and says it stores no personal data — [Fair FAQ](https://hfpg-fair.vercel.app/en/faq) [opened]; [Hack for Public Good](https://hack.gov.sg/2025/fair) [opened].
- Dahl et al. name people with mistaken premises as a higher-risk group, and say the risks are highest for those who would gain most — [Large Legal Fictions](https://arxiv.org/html/2401.01301) [opened].
- GPT-4, Claude 3 Opus and Llama 3 were less accurate for users described as less educated or non-native English speakers. The MIT article warns that memory features risk treating such groups differently, but the study did not test memory — [MIT News](https://news.mit.edu/2026/study-ai-chatbots-provide-less-accurate-information-vulnerable-users-0219) [opened].

**Normative concept.** Equal access to justice, tested through credibility: whose word counts, and who decides. Epistemic injustice (Fricker) is the natural frame, but I did not open a source for it.

**Who gains and who loses**
- Gains: workers with a true account that a memory helper reinforces (the 97% side of the finding), and caseworkers relieved of repeat intake.
- Loses: workers with a sincere but wrong belief, who walk into the ECT with confidence and a weaker claim.
- Also exposed: caseworkers, who must then undo a machine's agreement. Dutch lawyers report this pattern with clients who have already acted on chatbot advice — [NL Times](https://nltimes.nl/node/86722) [snippet].

**Strongest objection.** Employers control payslips and time records, and may even forge them — [TWC2 2026](https://twc2.org.sg/wp-content/uploads/2026/02/barriers_to_entry_2026april_pv9.pdf) [read]. A worker's word may be all he has, so a bot that marks his account "unverified" could reproduce the disbelief he already faces. A correcting model is not automatically better either: Claude 3 Opus refused more often for these users and was sometimes condescending — [MIT News](https://news.mit.edu/2026/study-ai-chatbots-provide-less-accurate-information-vulnerable-users-0219) [opened]. A separate objection: I found no deployed legal-aid bot with memory.

#### Case 2: Licensed financial advisers and retail clients

**Community and practice.** Representatives and robo-advisers who must know the client before recommending a product.

**Why memory-as-evidence matters here.** This field already has a written rule for when a client's statement may be relied on, so the memory question has a ready legal answer.
- In Singapore, a past client statement may be reused only if the client confirms at transaction time that nothing material has changed — [MAS FAA-N16, para 12](https://www.mas.gov.sg/-/media/mas/regulations-and-financial-stability/regulations-guidance-and-licensing/financial-advisers/notices/faa-n16---tracked.pdf) [read]. That works like an expiry date on memory (inference).
- A fully automated platform that skips some questions must detect inconsistent answers and resolve them before recommending — [FAA-N16, para 11A](https://www.mas.gov.sg/-/media/mas/regulations-and-financial-stability/regulations-guidance-and-licensing/financial-advisers/notices/faa-n16---tracked.pdf) [read].
- In the EU, firms may rely on client information unless they know, or ought to know, it is manifestly out of date, inaccurate or incomplete — [Reg 2017/565, Art 55(3)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32017R0565) [read].
- The law separates what the client is authoritative on from what they are not. A client's risk tolerance is evidence about the client. "This fund cannot lose" is not evidence about the fund (my reading of the rules above).

**Documented evidence**
- Stated profile changes advice strongly: trend-chasing allocation was as low as 0.67% for low-risk users and 38.18% for high-risk users on ChatGPT and Copilot. This was a stated prompt, not stored memory — [Biased Echoes](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204588/) [opened].
- Client memory is arriving in the field: Citi unveiled Citi Sky, and its wealth technology head called memory a key limit for agents — [Let's Data Science, citing Business Insider](https://letsdatascience.com/news/citi-launches-ai-wealth-advisor-memory-limits-remain-1cea7755) [opened; aggregator].
- Memory is already being poisoned commercially. Microsoft found 50 prompts from 31 companies in 14 industries, including finance, trying to implant "remember X as trusted" instructions — [Microsoft Security](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) [opened].

**Normative concept.** Reasonable basis and duty of care, set against client autonomy: respecting what the client wants is not the same as accepting what the client thinks is true.

**Who gains and who loses**
- Gains: low-balance clients who could not afford an adviser, and advisers relieved of repeated fact-finding.
- Loses: clients whose false belief about a product is treated as a preference. Advisers also lose some role as the person who says no.
- Regulated firms carry duties that general chatbots do not. That gap favours the unregulated tools people already use (inference).

**Strongest objection.** A preregistered preprint found that motivated investor framing did not reduce LLM fraud warnings across seven models, and humans suppressed warnings two to four times more — [Powdthavee 2026](https://arxiv.org/abs/2604.20652) [opened]. On that evidence an LLM may be a better sceptic than a person. Reply: it is a single-author preprint testing in-session framing on obvious fraud, not stored memory or subtle product beliefs.

#### Case 3: Support agents and claims handlers (short case)

**Community and practice.** Front-line support staff, AI service agents and insurance claims handlers who keep the account or claim file.

**Why memory-as-evidence matters here.** A customer's claim ("you promised a refund") can move from something said to something on file. Evidence law has a precise name for this problem, and Moffatt shows the firm owns what its bot then says.

**Documented evidence**
- When an outsider gives information to a record-keeper, accurate recording does not cure it. The informant must also act in the regular course. Johnson v. Lutz is the leading case — [FRE 803, Advisory Committee note](https://www.law.cornell.edu/rules/fre/rule_803) [opened].
- Moffatt: Air Canada was liable for its chatbot's wrong bereavement-fare statement, with damages of $650.88. The tribunal called the argument that the bot was a separate entity a "remarkable submission" — [2024 BCCRT 149, paras 27-28, 40](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do) [read].
- Vendors now sell cross-session customer memory, including Sierra and Twilio — [Sierra](https://sierra.ai/fr/blog/agent-os-2-0) [snippet; vendor]; [Twilio](https://static0.twilio.com/docs/conversations/memory) [snippet; vendor].

**Normative concept.** Record integrity and attribution: a record should show who said a thing and on what basis.

**Who gains and who loses**
- Gains: honest customers who no longer repeat themselves, and firms cutting service costs.
- Loses: customers who cannot see or correct what is on file, and support staff who inherit disputes.
- Firms can lose too: if the bot repeats a customer's claim as fact, that may become the firm's own representation under Moffatt (inference).

**Strongest objection.** I found no documented case of a customer's false claim being stored and repeated as account fact. Moffatt runs the other way: the company's bot was wrong, not the customer. Firms also hold systems of record that can override memory. This case rests on mechanism, so keep it short.

#### Why not practising lawyers as a stand-alone case
- Legal research tools handled false premises best of all query types — [Magesh et al.](https://arxiv.org/html/2405.20362v1) [read]. That is the awkward result for a story about lawyers.
- Harvey Memory stores working preferences, shows a confirmation card and cites a memory when it shapes an answer — [Harvey](https://www.harvey.ai/en-US/blog/memory-is-here-harvey-personalized) [opened; vendor]. That is close to the source visibility the finding says is lost.

### Inferences
- All three cases share one failure: a statement valid as evidence of what someone believes gets used as evidence that the belief is true.
- Memory differs from ordinary sycophancy in four ways: it persists across sessions, the user no longer sees the premise, a later reader may not know its source, and first-person belief turns into a third-person "fact".
- The ranking reflects a trade-off. Case 1 has the highest stakes and local relevance. Case 2 has the best doctrinal fit. Case 3 has the cleanest mechanism and the weakest evidence.
- Resistance varies by model, so deployment matters. Cheap open models are plausible for under-funded legal aid, but I found no source on which models such projects use.

### Gaps
- No study found that tests memory-as-evidence with legal, financial or service prompts. The group's finding would need to be replicated on such items before claiming domain effects.
- No source found on any deployed legal-aid, immigrant-advice or claims tool that keeps long-term memory of user beliefs.
- Consumer chatbots with memory are probably the real exposure for these groups, but I found no reliable usage data for migrant workers.

## Law: hearsay, Singapore's Evidence Act, a lawyer's duty, and false-premise studies

### Takeaway
Hearsay gives the report its cleanest concept: US law says a statement of belief cannot prove the fact believed, while Singapore's approach is closer to "admit, then weigh". Lawyers owe duties that amount to correcting a client's mistake, though I found no rule stating it that way. False-premise evidence is mixed: general models accepted false premises often, while legal research tools handled them well.

### Cited Findings

**US hearsay**
- Hearsay is a statement made outside the current hearing and offered to prove the truth of what it asserts — [FRE 801(c)](https://www.law.cornell.edu/rules/fre/rule_801) [opened].
- If a statement matters only because it was made, no truth issue arises and it is not hearsay — [FRE 801, Advisory Committee note](https://www.law.cornell.edu/rules/fre/rule_801) [opened].
- Rule 803(3) admits a then-existing state of mind, but excludes "a statement of memory or belief to prove the fact remembered or believed" — [FRE 803(3)](https://www.law.cornell.edu/rules/fre/rule_803) [opened].
- The Committee calls that exclusion necessary to avoid the "virtual destruction of the hearsay rule", citing Shepard v. United States — [FRE 803 note](https://www.law.cornell.edu/rules/fre/rule_803) [opened]. I did not open Shepard.

**Singapore Evidence Act 1893**
- Facts showing a state of mind are relevant when that state of mind is in issue or relevant — [s 14](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) [read].
- Oral evidence must be direct: a witness who perceived the fact, or for an opinion, the person who holds it — [s 62](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) [read].
- Statements made in the ordinary course of business are relevant, expressly including records compiled from information supplied by other persons — [s 32(1)(b)](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) [read]. This appears wider than the US position on outside informants.
- A court may still treat such a statement as not relevant in the interests of justice, and it assigns whatever weight it sees fit — [s 32(3), (5)](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) [read].
- Courts presume that a device which ordinarily produces an electronic record accurately did so on the occasion in question — [s 116A](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) [read].
- A party's statement can be an admission, defined by the inference it suggests about a fact in issue — [ss 17-18](https://sso.agc.gov.sg/Act/EA1893?WholeDoc=1) [read].

**A lawyer's duties**
- Singapore: a practitioner must tell the client all known information that may reasonably affect their interests, act competently, and advise on time — [PCR 2015, r 5(2)(b), (c), (h)](https://sso.agc.gov.sg/SL/LPA1966-S706-2015?WholeDoc=1) [read].
- Practitioners must also keep contemporaneous records of both instructions received and advice given — [r 5(2)(k)](https://sso.agc.gov.sg/SL/LPA1966-S706-2015?WholeDoc=1) [read].
- They must not knowingly mislead a court or present evidence known to be false — [r 9](https://sso.agc.gov.sg/SL/LPA1966-S706-2015?WholeDoc=1) [read].
- They must exercise professional judgment over their advice, and as far as able, prevent a client giving false evidence — [r 10](https://sso.agc.gov.sg/SL/LPA1966-S706-2015?WholeDoc=1) [read].
- There is a tension: practitioners must also follow lawful, proper and reasonable instructions — [r 5(2)(i)](https://sso.agc.gov.sg/SL/LPA1966-S706-2015?WholeDoc=1) [read].
- US: Rule 2.1 requires independent judgment and candid advice, even if unwelcome. Advice is generally not expected until asked, but Rule 1.4 may require action where a course risks substantial adverse consequences — [DC Rule 2.1 and comments](https://dcbar.org/for-lawyers/legal-ethics/rules-of-professional-conduct/counselor/advisor) [opened; the DC version, as the ABA page blocked access].

**False-premise studies**
- Dahl et al. counted uncritical answers to false premises as hallucinations — [Large Legal Fictions](https://arxiv.org/html/2401.01301) [opened]. These are older models, and the premise sat in the question rather than in memory:

| Model | False dissent (SCOTUS) | False overruling (SCOTUS) |
|---|---|---|
| GPT-3.5 | 0.338 | 0.821 |
| PaLM 2 | 0.990 | 1.000 |
| Llama 2 | 0.000 | 0.027 |

- Llama 2's low score is misleading: it often denied that the case or justice existed — [Large Legal Fictions](https://arxiv.org/html/2401.01301) [opened].
- Lexis+ AI was accurate on 65% of queries and Westlaw AI-Assisted Research on about 41-42%. Accuracy was highest on false-premise queries — [Magesh et al.](https://arxiv.org/html/2405.20362v1) [read].
- Lexis+ AI, Westlaw's tool and GPT-4 often corrected the false premise. Yet Ask Practical Law AI failed in one worked example — [Magesh et al.](https://arxiv.org/html/2405.20362v1) [read].
- Magesh et al. only had 22 false-premise queries, and warn this bias poses particular risk for pro se and lay users — [Magesh et al.](https://arxiv.org/html/2405.20362v1) [read].

**Courts and chat records**
- Judge Rakoff held that documents a defendant made with Claude were covered by neither attorney-client privilege nor work product. The FBI had seized them — [Lawfare on Heppner](https://www.lawfaremedia.org/article/ai-and-privilege-after-united-states-v.-heppner) [opened; secondary].
- Commentators differ on how far it reaches, and Warner v. Gilbarco reportedly went the other way on work product — [Wilson Elser](https://www.wilsonelser.com/publications/divergent-two-federal-courts-chart-seemingly-opposite-paths-on-work-product-protection-for-ai-generated-materials) [snippet].
- A Singapore lawyer was reportedly ordered to pay costs personally for citing an AI-generated fictitious case — [Tajudin [2025] SGHCR 33](https://www.elitigation.sg/gd/s/2025_SGHCR_33) [snippet]. MinLaw's final, non-binding guide reportedly came out on 6 March 2026 — [MinLaw Guide](https://www.mlaw.gov.sg/files/Final_Ver__Guide_for_using_Generative_AI_in_the_Legal_Sector.pdf) [snippet].

### Inferences
- "User believes X" is the machine version of a state-of-mind statement. It is good evidence of the belief and no evidence of X. Models that fail treat it as the second.
- US-style exclusion resembles deleting the memory. Singapore-style "admit and weigh" resembles the "unverified" label.
- Weighing only works if the reader can see the source. The group's finding that remaining false answers hide their source more often is therefore the key weakness of the label fix: the weigher has lost what it needs.
- Section 116A supplies a useful distinction: a stored memory may be accurately recorded and still be false.
- Rule 5(2)(k) already separates instructions from advice, a human model for separating "what the client says" from "what is so" (my reading).
- Memory can also be evidence in the literal sense. A false belief saved in a consumer tool may be disclosable and could be used against its author as an admission. This is my extrapolation from Heppner and ss 17-18, and no case on stored memory was found.
- The hearsay analogy is a concept, not a legal rule for AI. Those rules govern courts, not chatbots.

### Gaps
- No rule, ethics opinion or case found stating a duty to correct a client's mistaken belief in those words. It is derived from the duties above.
- I found no opinion on clients arriving with mistaken AI-formed beliefs. Reports are anecdotal — [NL Times](https://nltimes.nl/node/86722) [snippet]; [New Law Journal](https://www.newlawjournal.co.uk/content/stop-asking-chatbots--say-solicitors) [snippet].
- Search summaries mentioned a 56% chatbot legal-advice survey (law-firm commissioned) and a Southampton experiment on 288 people favouring ChatGPT advice. Neither was opened or tied to a clear URL, so verify them first.
- Whether s 32(1)(b) would reach a customer's statement in an AI memory needs a Singapore lawyer's view. No case was found. I also read the Rakoff opinion only through commentary.

## Access to justice: legal-aid chatbots, immigrants and migrant workers

### Takeaway
The need is large and the tools exist, but I found no deployed legal-aid chatbot with long-term memory. The evidence supports a warning about an emerging risk, not a report of harm.

### Cited Findings
- US low-income households got no or insufficient legal help for 92% of problems that substantially affected them, and 74% had a civil legal problem in the past year (2021 survey) — [LSC Justice Gap](https://justicegap.lsc.gov/the-report/executive-summary/) [opened]. I found no Singapore equivalent.
- Singapore's Small Claims Tribunals use a Harvey-built tool that summarises each side's positions, evidence and disputed issues, for magistrates and self-represented persons. It is designed not to give case-specific legal advice — [Singapore Courts](https://www.judiciary.gov.sg/news-and-resources/news/news-details/media-release--new-generative-ai-powered-case-summarisation-tool-to-help-small-claims-tribunals-users) [opened].
- The release does not address chat history or memory — [Singapore Courts](https://www.judiciary.gov.sg/news-and-resources/news/news-details/media-release--new-generative-ai-powered-case-summarisation-tool-to-help-small-claims-tribunals-users) [opened]. Launch to self-represented users is reported inconsistently, as November or 2 December 2025 [snippet].
- Self-represented persons must themselves ensure what they give the court is verified and accurate — [Registrar's Circular 1 of 2024](https://judiciary.gov.sg/docs/default-source/circulars/2024/registrar's_circular_no_1_2024_supreme_court) [snippet].
- NYC's MyCity chatbot wrongly said employers could take tips and landlords could refuse housing vouchers. Queries in other languages produced similar errors, and it carried disclaimers — [The Markup](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law) [opened]. This is a wrong-model error, not a user belief. The new mayor reportedly planned to shut it down — [The Markup 2026](https://themarkup.org/artificial-intelligence/2026/01/30/mamdani-to-kill-the-nyc-ai-chatbot-we-caught-telling-businesses-to-break-the-law) [snippet].
- The FTC's final order required DoNotPay to pay $193,000 and barred claims that it performs like a lawyer without evidence — [FTC](https://www.ftc.gov/node/87474) [snippet].
- Asylum tools found: ACME, a research prototype with small expert validation — [arXiv](https://arxiv.org/html/2407.09197v3) [snippet].
- In one UK case, a claim had been refused because the accounts were inconsistent, and the appeal then relied on AI-assisted research by a barrister — [inkl](https://www.inkl.com/news/judge-blasts-lawyer-for-using-ai-after-he-cited-entirely-fictitious-cases-in-asylum-appeal) [snippet].
- In Y (China), a barrister was referred to the regulator for citing a ChatGPT-generated decision — [Local Government Lawyer](https://www.localgovernmentlawyer.co.uk/litigation-and-enforcement/400-litigation-news/62258-barrister-referred-to-bar-standards-board-for-using-false-ai-derived-precedents-in-court) [snippet].

### Inferences
- Summarising case documents is safer than remembering beliefs, because the source is a filed document and not the user's unexamined view.
- Asylum is a sharp variant. Credibility often turns on consistency, so a helper that remembers and repeats a wrong detail could harm a claim. This is a plausible extension, and I found no recorded instance.
- Disclaimers appear to have done little at MyCity, which suggests caution about labels as a sole fix for low-literacy users.

### Gaps
- No evidence found of an immigrant or asylum seeker harmed by their own AI use. The UK cases involve barristers.
- No source on regulated immigration advice and chatbots. I did not search this far, so the perimeter question is open.
- No outcome evaluation of Fair or similar tools was found. Fair's FAQ does not say whether chats are retained.

## Financial advice: suitability, KYC, regulators and stored profiles

### Takeaway
A stated profile clearly changes LLM advice, and rules already limit reliance on client statements. Regulators are working on AI governance and disclaimers rather than memory. I found no express duty to correct a client's misconception, and the best experiment cuts against the worry.

### Cited Findings

**Duties**
- Singapore: advisers must have a reasonable basis for a recommendation, giving due consideration to objectives, financial situation and needs — [FAA-N16, para 8](https://www.mas.gov.sg/-/media/mas/regulations-and-financial-stability/regulations-guidance-and-licensing/financial-advisers/notices/faa-n16---tracked.pdf) [read; a tracked-changes copy of the notice].
- Advisers must also warn clients in writing that inaccurate information may affect suitability — [FAA-N16, para 14](https://www.mas.gov.sg/-/media/mas/regulations-and-financial-stability/regulations-guidance-and-licensing/financial-advisers/notices/faa-n16---tracked.pdf) [read].
- US: advisers must reasonably inquire into a retail client's profile and generally update it, and the same fiduciary duty covers robo-advisers — [SEC IA-5248](https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf) [read].
- It is generally reasonable to rely on client information, and an adviser misled by the client should not be held at fault — [SEC IA-5248, fn 36](https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf) [read]. Knowing of events that make the profile inaccurate can trigger a fresh inquiry — [SEC IA-5248](https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf) [read].
- EU: firms must take reasonable steps to make client information reliable, including checking for obvious inaccuracies, and must keep information current in ongoing relationships — [Reg 2017/565, Art 54(7)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32017R0565) [read; the 2017 base text, later amendments not checked].

**Regulators on AI**
- MAS issued AI risk management guidelines on 7 October 2026, effective 7 October 2027. They cover all institutions and AI forms, and third-party AI stays the institution's responsibility. Agentic guidance consultation is planned for 2027 — [MAS](https://www.mas.gov.sg/news/media-releases/2026/mas-sets-out-supervisory-expectations-on-responsible-ai-adoption-by-financial-institutions) [opened]. I did not read the full PDF, so I cannot say whether memory is covered.
- FCA: not widening its remit over AI providers, but urging them to warn of the limits of AI advice, and folding six of seven Mills Review recommendations into its work — [MLex, 19 Oct 2026](https://www.mlex.com/mlex/articles/2539389) [opened; short item].
- The Mills Review reportedly drew on a survey of over 5,000 UK consumers — [PwC](https://www.pwc.co.uk/industries/financial-services/understanding-regulatory-developments/fca-commissioned-review-sets-seven-point-ai-agenda-for-retail-finance.html) [snippet]. The SCL write-up blocked access.
- SEC: withdrew its predictive data analytics proposal in June 2025, so general fiduciary standards remain — [National Law Review](https://natlawreview.com/article/sec-formally-withdraws-fourteen-rule-proposals) [snippet].

**Evidence on LLM behaviour**
- Biased Echoes: 270 prompts across three LLMs by age and risk. Portfolios had over 93% US equities against a 59% benchmark, and all five risk types were elevated — [Winder et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204588/) [opened].
- Those biases appeared across profiles and are attributed to training data, not to user statements. Debiasing prompts only partly helped, and about 95% of answers had disclaimers — [Winder et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204588/) [opened].
- Powdthavee: 3,360 AI conversations with seven LLMs against 1,201 humans. No LLM endorsed fraud at baseline, while humans did at 13-14%. Reversal occurred in under 3 per 1,000 observations — [arXiv 2604.20652](https://arxiv.org/abs/2604.20652) [opened; preprint].
- An AI client file combining live feeds and meeting transcripts is being sold to wealth managers — [FinTech Global](https://fintech.global/?p=245482) [snippet; vendor].

### Inferences
- Answer to "does a stored risk profile affect advice?": a stated one does. The stored version is untested but likely to act similarly, since the model sees the same text.
- The rules treat client input as reliable until there is reason to doubt it. Memory-as-evidence reverses the logic: repetition raises trust where the rules ask for doubt.
- FAA-N16's confirmation rule and inconsistency check could be design requirements for any memory-enabled adviser.
- Powdthavee and the group's finding can both hold: outright fraud is an easy test, while the group's result is model-specific. Whether Mistral Nemo-class models were included is unknown.

### Gaps
- No rule found stating a fiduciary duty to correct a client's misconception. The closest are the reasonable basis, reasonable belief and reliability duties.
- No study found on stored memory in financial advice, or on advice from a false belief about a product.
- FCA Handbook rules (COBS) were not checked. The Biased Echoes finding is a fetched summary, and the Mills Review was not opened.

## Customer service: Moffatt, support memory and repeated customer claims

### Takeaway
Moffatt settles who answers for a bot's words, but not the scenario in the brief. Memory products exist. A customer's false claim becoming account fact is, on what I found, a demonstrated mechanism rather than a documented incident.

### Cited Findings
- Moffatt: the tribunal held that a firm answers for its website's content, whether from a static page or a chatbot, and that a customer need not cross-check one page against another — [2024 BCCRT 149, paras 27-28](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do) [read].
- The claimant reasonably relied on the bot, and the firm failed to take reasonable care — [2024 BCCRT 149, paras 25-29](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do) [read]. It is a small-claims tribunal decision, not binding precedent elsewhere (my characterisation).
- Sierra describes a data layer for customer continuity across sessions — [Sierra](https://sierra.ai/fr/blog/agent-os-2-0) [snippet; vendor]. Twilio sells memory of history, preferences and open issues — [Twilio](https://static0.twilio.com/docs/conversations/memory) [snippet; vendor].
- A Neo4j guide says Agentforce lacks a universal memory hook, so cross-conversation memory is usually custom-built — [Neo4j](https://neo4j.com/labs/genai-ecosystem/genai-frameworks/salesforce-agentforce-memory/) [snippet]. Intercom's position is unknown.
- Microsoft reports assistants treat injected text as legitimate user preferences, and Copilot shows memory as saved facts that persist — [Microsoft Security](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) [opened].
- A blog describes a support agent storing "refund approved" and recalling it on other tickets, with 47 refunds and only 11 approved — [dev.to](https://dev.to/mjmirza/agent-memory-poisoning-the-4-stage-enterprise-damage-chain-20fi) [snippet]. It is unverified and may be illustrative. Do not cite it as fact.

### Inferences
- Moffatt plus memory yields a new liability path: a customer says "you promised", the bot stores it, a later session repeats it as fact, and the statement is now the firm's. This has not been tested in any case found.
- The risk also has a deliberate form. Customers who learn that claims stick could plant them, which is ordinary fraud with a new tool.
- The fix is familiar: write memory only against the system of record, and keep customer statements labelled as customer statements.

### Gaps
- No documented incident of a customer's false claim becoming an account fact was found.
- No independent evidence on how vendors separate customer statements from verified facts. Most sources are vendor pages, and none were opened.

## Insurance and benefits: when a stored claim becomes a record

### Takeaway
This is the weakest strand. The legal concept is strong, but I found no evidence of a stored claim hardening into a record in AI claims handling. Fold it into Case 3 rather than treating it as its own case.

### Cited Findings
- The NAIC model bulletin (December 2023) reportedly covers AI across the insurance lifecycle including claims, and ties it to unfair claims practices law. It applies only where a state adopts it — [Sullivan & Cromwell](https://www.sullcrom.com/SullivanCromwell/_Assets/PDFs/Memos/NAIC-Model-Bulletin-Use-AI-Insurers.pdf) [snippet].
- Twenty-four states had adopted it as of March 2025 — [Quarles](https://quarles.com/newsroom/publications/nearly-half-of-states-have-now-adopted-naic-model-bulletin-on-insurers-use-of-ai) [snippet]. A later vendor figure of 25 is unverified.
- A vendor guide shows adjusters condensing recorded statements, phone logs and emails into an AI claim summary — [FindSkill](https://findskill.ai/blog/chatgpt-for-claims-adjusters/) [snippet; vendor].
- US law gives the doctrine: a record must trace to someone with knowledge acting in the regular course, and an opponent can challenge trustworthiness — [FRE 803(6) and note](https://www.law.cornell.edu/rules/fre/rule_803) [opened].

### Inferences
- A claimant's recorded statement condensed into an AI summary can lose its "claimant says" framing. This is the Johnson v. Lutz problem, moved upstream. The step is plausible, but no source shows it happening.

### Gaps
- No regulator guidance found on generative AI at claims intake.
- Benefits administration was not researched in depth. Figures found on AI denial overturn rates were low-quality and conflicting, so they are excluded.
- A better next search would target state insurance bulletins, bad-faith claim-file cases, and medical-record copy-forward studies.

Research limits: Firecrawl's scrape tool ran out of credits, and SSO, CanLII and the ABA blocked direct fetches. Singapore statutes, Moffatt and the EU regulation were read in the browser instead. Moffatt was read from the CRT's own site.
