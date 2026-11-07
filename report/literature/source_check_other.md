# Source check: education, clinical, legal, philosophy, Singapore, product pages

Report text read from `git show HEAD:` (body_a, body_b, tutoring_values, references). Notes in `report/literature/` and `report/societal/` were used only as leads to find sources. "Minor" marks a reference or wording repair that does not change an argument.

Tools: Firecrawl scrape and search ran out of credits part-way, so later sources were opened with plain curl (public pages only), the NCBI and Crossref APIs, and WebSearch. Sites that returned 403 or a bot wall were not retried by other means and are marked.

| Source | Report's claim (short) | What the source says, with section or page | Status | Exact replacement wording if not confirmed |
|---|---|---|---|---|
| Anthropic n.d. | Help pages describe saved items without stating how they reach the model | Current sections give no mechanism for saved memory. But past-chat search "use[s] Retrieval-Augmented Generation (RAG)" and appears "as tool calls"; legacy section says the synthesis "provides context for every new standalone conversation" | OVERSTATED (minor) | "Help pages say saved items inform later chats but not how they enter the prompt (Anthropic, n.d.; Google, n.d.), though Claude's page says past-chat search runs as a tool call" |
| Anthropic n.d. | Reference: title, URL | Title and URL match; article resolves | CONFIRMED | |
| Google n.d. | Help page does not state how items reach the model | No mechanism stated | CONFIRMED | |
| Google n.d. | Gemini memory limited to adults | "Be 18 or over." | CONFIRMED | |
| Google n.d. | Off on school accounts | "isn't available when you sign in to a work, school, or supervised Google Account" | CONFIRMED | |
| Google n.d. | Reference: title, URL | Match | CONFIRMED | |
| Khan Academy (no ref entry) | "Khanmigo documents interests" | Blog: Khanmigo saves "your top interests from past conversations"; opt-in, editable | CONFIRMED | |
| Khan Academy (no ref entry) | Reference list | Claim has no citation and no reference entry | WRONG (reference, minor) | Add: Khan Academy. (2023, updated 2025). *New! Personalized AI learning with Khanmigo Interests*. https://blog.khanacademy.org/new-khanmigo-interests/ and cite it in the sentence |
| LearnLM & Eedi 2025 vs Exposure para | "No deployed tutor we read documents storing a student's wrong belief" | The cited trial says of Eedi's live platform: teachers "can view insights on class-wide and individual student-level misconceptions" (platform appendix) | WRONG | "No deployed AI tutor we read documents using a stored misconception in later sessions: Khanmigo documents interests, Eedi shows teachers individual misconceptions, and Gemini memory is limited to adults and is off on school accounts (Google, n.d.)." |
| Campus Technology 2025 | Study mode reportedly draws on memory of earlier chats | "based on questions that assess skill level and memory from previous chats" (OpenAI description, Personalized support bullet) | CONFIRMED | |
| Campus Technology 2025 | Reference | Title, date, URL match; article has a named author, Rhea Kelly | WRONG (reference, minor) | "Kelly, R. (2025, July 30). New ChatGPT study mode guides students through questions. *Campus Technology*." In text: (Kelly, 2025) |
| Bastani 2025 | Plain GPT-4 did better in practice | GPT Base 48% better on practice problems | CONFIRMED | |
| Bastani 2025 | 17% worse on later exam without it | "statistically significantly worse than students in the control arm by 17%" | CONFIRMED | |
| Bastani 2025 | Reference title | Full title has subtitle; volume, issue, e-number, DOI match (Crossref) | WRONG (reference, minor) | "Generative AI without guardrails can harm learning: Evidence from high school mathematics." |
| Bergson 2026 | 28 of 215,712 patients (0.013%) | "Twenty-eight patients (0.013% of those receiving mental health care)"; 215,712 unique patients. Discussion calls it "conditional on" a psychosis diagnosis, which sits oddly with that denominator | OVERSTATED (minor) | "in 28 of 215,712 patients receiving mental health care (0.013%)" |
| Bergson 2026 | Chatbot use judged to worsen psychosis | Category defined as "psychosis-worsening chatbot use"; two raters | CONFIRMED | |
| Bergson 2026 | 60.7% in a first episode | 17 of 28 (60.7%) | CONFIRMED | |
| Bergson 2026 | Authors say design cannot establish causation | The sentence concerns the rise after GPT-4o coinciding with sycophancy: "though our design cannot establish causation" | OVERSTATED (minor) | "and the authors say their design cannot establish that sycophancy caused the rise after GPT-4o" |
| Bergson 2026 | Reference | Authors, title, journal, DOI match. Research letter, online 7 Oct 2026 | CONFIRMED | |
| Bo 2026 | 24 novices | Within-subjects, n = 24 students | CONFIRMED | |
| Bo 2026 | Corrected wrong beliefs with low-sycophancy bot, not high | Sec 4.3: Low improved wrong beliefs (p = .028), High did not (p = .77) | CONFIRMED | |
| Bo 2026 | "17 reported no difference" | Interview results: 7/24 described a sycophancy-related difference, 5/24 noticed other differences, 12/24 said none. "17/24 (71%)" unobservant of sycophancy | WRONG | "and 17 did not notice the sycophancy, of whom 12 reported no difference at all" |
| Bo 2026 | Reference | Title and arXiv ID match; author order checked on arXiv | CONFIRMED | |
| Butterfield & Metcalfe 2001 | Confident errors likeliest to be corrected after feedback | "highly confident errors were the most likely to be corrected in a subsequent retest" (abstract) | CONFIRMED | |
| Butterfield & Metcalfe 2001 | Reference | Journal, vol 27(6), first page match PubMed. Marked (abstract) correctly | CONFIRMED | |
| Elish 2019 | Responsibility falls on a human with limited control over an automated system | Abstract: responsibility "misattributed to a human actor who had limited control" | CONFIRMED | |
| Elish 2019 | Reference | Title, vol 5, pp. 40-60, DOI match | CONFIRMED | |
| FRE 803(3) (LII) | Quoted phrase | Text: "A statement of the declarant's then-existing state of mind (such as motive, intent, or plan) or emotional, sensory, or physical condition (such as mental feeling, pain, or bodily health), but not including a statement of memory or belief to prove the fact remembered or believed unless it relates to the validity or terms of the declarant's will." | CONFIRMED | |
| FRE 803(3) (LII) | Exception apart from matters concerning a will | "relates to the validity or terms of the declarant's will" | CONFIRMED | |
| FRE 803(3) (LII) | Light example: shows belief, not the fact | Consistent with the rule and the committee note on exclusion | CONFIRMED | |
| FRE 803(3) (LII) | Reference URL | Resolves | CONFIRMED | |
| Fricker 2007 via Lackey | Norm, p. 19 | Lackey quotes p. 19: hearer "must match the level of credibility" to "the evidence that he is offering the truth" | CONFIRMED | |
| Fricker 2007 via Lackey | Central case, p. 28 | Lackey quotes p. 28: "the central case of testimonial injustice is identity-prejudicial credibility deficit" | CONFIRMED | |
| Fricker 2007 via Lackey | Excess is no epistemic injustice in itself, pp. 20-21 | Lackey quotes p. 20: "in itself it does her no epistemic injustice"; p. 21 on individual moments of excess | CONFIRMED | |
| Fricker 2007 via Lackey | Excess "can harm only by accumulating into arrogance" | p. 20 also says excess "may (unusually) be disadvantageous in various ways". "Only ... cumulatively" is Lackey's gloss, about testimonial injustice, not harm | OVERSTATED | "and can amount to testimonial injustice only cumulatively, as when it builds into epistemic arrogance (2007, pp. 20-21, as quoted in Lackey, 2018)" |
| Fricker 2007 via Lackey | Central case tracks a person across areas of life | Lackey, early in chapter: prejudice "tracks" the subject "through different dimensions of social activity" | CONFIRMED | |
| Lackey 2018 | Used only as a conduit for Fricker | Lackey rejects these views: she argues excess can be testimonial injustice and that credibility can be finite and distributive ("I disagree with Fricker here") | OVERSTATED (omission) | After the pp. 20-21 sentence add: "Lackey (2018) rejects this, arguing that excess can itself be a testimonial injustice, so our restraint rests on Fricker's account." |
| Lackey 2018 | Reference | Title, pp. 145-168, Springer match Crossref | CONFIRMED | |
| Fricker 2017 | Quoted phrase "less than their fair share of an epistemic good" | Exact. Continues "such as education, or access to expert advice or information" | CONFIRMED | |
| Fricker 2017 | "Fricker's distributive sense" | She credits it: "as David Coady (2010; and this volume) has rightly emphasized"; it is one she allows room for, not hers | OVERSTATED (minor) | "The distributive sense Fricker accepts from Coady fits better:" |
| Fricker 2017 | Reference | Editors, title, pp. 53-60 match White Rose record | CONFIRMED | |
| Kelly 2005 | Belief can stand in for evidence when nothing else is available | "stands in as a sort of proxy for the evidence on which it is based" when "I lacked access to your first-order evidence". Pre-publication draft | OVERSTATED (minor) | see next row |
| Kelly 2005 | "in proportion to their reliability" | The word "reliab" does not occur in the draft. Kelly says one presupposes "a competent evaluator"; no proportion claim | NOT FOUND IN SOURCE | "A person's belief can stand in as a proxy for evidence one cannot access, provided one takes them to be a competent evaluator (Kelly, 2005)" |
| Kelly 2005 | Reference | Editors and volume fine; pages missing. Crossref: pp. 167-196 | WRONG (reference, minor) | Add "(Vol. 1, pp. 167-196)" |
| LearnLM & Eedi 2025 | 165 UK students | "N = 165 students across five UK secondary schools" | CONFIRMED | |
| LearnLM & Eedi 2025 | Aged 13 to 15 | "Year 9 and 10 (ages 13-15)" | CONFIRMED | |
| LearnLM & Eedi 2025 | 93.0% LearnLM | 93.0% [90.4, 95.3], second attempt correct | CONFIRMED | |
| LearnLM & Eedi 2025 | 65.4% hints | 65.4% [63.8, 66.9] | CONFIRMED | |
| LearnLM & Eedi 2025 | 91.2% human tutors | 91.2% [88.5, 93.6] | CONFIRMED | |
| LearnLM & Eedi 2025 | Tutor told the specific misconception | Prompt included "the specific misconception underlying the answer" | CONFIRMED | |
| LearnLM & Eedi 2025 | Contrast implied to come from knowing the misconception | Static hints were also "designed to prompt reflection on a specific misconception". The contrast is interactive against static | OVERSTATED | Add after "human tutors": "Hints also targeted the misconception, so this compares live tutoring with static text, not knowing with not knowing." |
| LearnLM & Eedi 2025 | Expert checked every message | Tutors could "revise each message it drafted" | CONFIRMED | |
| LearnLM & Eedi 2025 | No memory across sessions | "its prompt did not provide any information on past tutoring sessions". Prompt did carry year group and predicted score | CONFIRMED | |
| LearnLM & Eedi 2025 | Reference | Title, arXiv ID match; "LearnLM Team, Google & Eedi" | CONFIRMED | |
| MOE 2026 (AI usage) | Rules "keep Primary 4 to 6 AI use in school and under supervision" | "Students in primary 4 to 6 will only use AI tools in school that are specifically designed for education" under teacher supervision. This limits tools used in school; it does not confine use to school | OVERSTATED | "MOE limits Primary 4 to 6 pupils in school to educational AI tools under teacher supervision (MOE, 2026), so the risk sits outside those rules" |
| MOE 2026 (tuition) | "MOE does not track who gets tuition" | "does not track the proportion of Primary 3 to 6 students receiving private tuition, broken down by subjects" | OVERSTATED | "and MOE does not track the share of Primary 3 to 6 students taking tuition by subject" |
| MOE 2026 | Reference | Dates right. Two replies in one entry, tuition title truncated, listing URL returned 404 | WRONG (reference, minor) | Two entries, with https://www.moe.gov.sg/news/parliamentary-replies/20260506-ai-usage-in-schools and https://www.moe.gov.sg/news/parliamentary-replies/20260212-breakdown-of-primary-3-to-6-students-receiving-private-tuition-by-subject-and-median-household-spending-to-evaluate-sufficiency-of-school-based-learning, in text (MOE, 2026a; 2026b) |
| Morrin 2025 | Hypothesise recalled detail could strengthen delusions of reference | v5: "delusions of reference and persecution would be enhanced" by personally relevant details | CONFIRMED | |
| Morrin 2025 | Reference | Title cut short; v5 URL resolves | WRONG (reference, minor) | "Delusions by design? How everyday AIs might be fuelling psychosis (and what can be done about it)" |
| Nan 2022 | False beliefs follow literacy, numeracy, subject knowledge, trust | Abstract: these "confer strong resistance" (trust in science), for health misinformation | CONFIRMED | |
| Nan 2022, Pew 2019 | These are "unequally distributed by education and class" | Pew 2019 shows education gaps. Neither reports class or income. Nan's abstract does not address distribution | NOT FOUND IN SOURCE | "On health and science facts, false beliefs follow literacy, numeracy, subject knowledge and trust in science (Nan et al., 2022), and science knowledge differs sharply by education (Pew Research Center, 2019)" |
| Nan 2022 vs Soon, Sultan | "Schooling alone predicts little on misinformation" | Nan abstract: "higher educational attainment predict[s] less susceptibility to health misinformation". Sentence hides this conflict | OVERSTATED | "Schooling predicts little on online news headlines (Sultan et al., 2024), though higher attainment predicts less susceptibility on health claims (Nan et al., 2022)." Add Soon & Goh only once its tables are read |
| Nan 2022 | Reference | Journal, vol, article number match; subtitle missing | WRONG (reference, minor) | Add ": A systematic review of individual differences in susceptibility to health misinformation" |
| NIE 2024 | SLS "shows teachers class-level misconceptions" | Page never says this. Only related lines: a teacher gets feedback on "individual student progress"; a tool clarifies misconceptions for students | NOT FOUND IN SOURCE | "the Student Learning Space helps teachers see where a class has gone wrong and what recurs across answers (Apolitical, n.d.)". Apolitical case study supports this but not the word misconceptions. GovTech page in the notes returned 403 |
| NIE 2024 | Reference | Page is a Straits Times article reprinted by NIE | WRONG (reference, minor) | If still cited: "Straits Times, reproduced by the National Institute of Education. (2024, July 29)." |
| Nguyen 2020 | Copy adds no corroboration | "the number of copies of that newspaper one encounters ought not add any extra weight" | CONFIRMED | |
| Nguyen 2020 | Belief "cannot be independent confirmation for the person who holds it" | Nguyen discusses copies and pre-selected networks, not one's own belief returned. The step is the report's | OVERSTATED (minor) | "and, on Nguyen's reasoning about copies, it adds nothing for the person who holds it (Nguyen, 2020)" |
| Nguyen 2020 | Time and interface hide that it is a copy | "the bootstrap here is obscured by time and interface", said of pre-selected networks. Footnote 4 denies all non-independence is bad | OVERSTATED (minor) | "A copy adds no corroboration, and such bootstraps are easily missed, being 'obscured by time and interface' (Nguyen, 2020)." |
| Nguyen 2020 | Reference | Title, vol, pages, DOI match | CONFIRMED | |
| Pan 2016 | 96% primary or less failed to reject | Table 3: 45 (95.7%) of 47 | CONFIRMED | |
| Pan 2016 | 75% post-secondary | Table 3: 506 (74.5%) | CONFIRMED | |
| Pan 2016 | "failed to reject", GP patients | "did not reject"; "not sure" counted incorrect; 24 private clinics | CONFIRMED | |
| Pan 2016 | Reference | Authors, BMC Fam Pract 17:148 match | CONFIRMED | |
| Pew 2019 | Knowledge varies by education | 9.1 vs 5 of 11 questions, postgraduate vs high school or less | CONFIRMED | |
| Pew 2019 | Reference | Title right; no date or URL | WRONG (reference, minor) | Add "(2019, March 28)" and https://www.pewresearch.org/science/2019/03/28/what-americans-know-about-science/ |
| Pew 2025 | Less-educated use chatbots less overall | ChatGPT ever used: 18% high school or less, 51-52% degree holders | CONFIRMED | |
| Pew 2025 | Reference | Title right; no date or URL | WRONG (reference, minor) | Add "(2025, June 25)" and https://www.pewresearch.org/short-reads/2025/06/25/34-of-us-adults-have-used-chatgpt-about-double-the-share-in-2023/ |
| Sadler 2013 | 181 teachers, 9,556 students | Abstract and tables | CONFIRMED | |
| Sadler 2013 | Stronger students: larger gains only with both kinds of knowledge | "Only when teachers had both SMK and KOSM were student gains significantly larger" | CONFIRMED | |
| Sadler 2013 | Correlational | "Its findings are correlational in nature" | CONFIRMED | |
| Sadler 2013 | Low scorers "gained under no category of teacher knowledge" | True of misconception items only. On non-misconception items they gained significantly with teacher SMK | OVERSTATED | "and students with low reading and mathematics scores showed no significant gain on misconception items under any category of teacher knowledge" |
| Sadler 2013 | Reference | Title, AERJ 50(5), 1020-1049 match | CONFIRMED | |
| Schroeder & Kucera 2022 | g = 0.41 [0.30, 0.51] | Exact, 44 comparisons | CONFIRMED | |
| Schroeder & Kucera 2022 | 0.28 after bias correction | Trim and fill g = 0.28 [0.16, 0.39]; authors judge bias not substantial | CONFIRMED | |
| Schroeder & Kucera 2022 | Reference title | Subtitle missing | WRONG (reference, minor) | "Refutation text facilitates learning: A meta-analysis of between-subjects experiments." |
| Evidence Act s 32(1)(b) | Professional record counts when built on what others told the record-keeper | WIPO Lex copy: "a record compiled by a person acting in the ordinary course of a trade, business, profession or other occupation based on information supplied by other persons" | CONFIRMED (2015 consolidation) | |
| Evidence Act s 32(5) | Court sets weight | "the court shall assign such weight as it deems fit to the statement" | CONFIRMED (2015 consolidation) | |
| Evidence Act s 32C(3) | Challenges to original supplier's credibility | "subsections (1) and (2) apply in relation to both the maker of the statement and the person who originally supplied the information" | CONFIRMED (2015 consolidation) | |
| Evidence Act | "Version in force on November 5, 2026" | SSO returned 403 to curl and WebFetch; LawPlayer 403. A search snippet of LawPlayer agrees on s 32C(3) | NOT ACCESSIBLE | Human check on SSO; the 2020 Revised Edition may have changed "shall" and sub-numbering |
| Soon & Goh 2021 | Schooling predicts little | IPS PDF behind an Incapsula bot wall. Commbox abstract only says education was examined. Press snippets name age and housing; none confirm education null. Project note says not significant: unverified | NOT ACCESSIBLE | Human check, or drop from the sentence (see Nan row) |
| Soon & Goh 2021 | Reference | Title and series number match Commbox listing | CONFIRMED | |
| Straits Times via ANN | S$162.60 and S$36.30 | "$162.60 a month" top 20%, "$36.30" bottom 20%, by income | CONFIRMED | |
| Straits Times via ANN | Reference year (2024) | Article dated January 23, 2025. Title and URL match | WRONG (reference, minor) | "(2025, January 23)" |
| Sultan 2024 | Schooling predicts little | Sec 1.2.3: education "did not have a credible effect on discrimination ability" (US news headlines) | CONFIRMED | |
| Sultan 2024 | Reference | Title, DOI match; volume missing | WRONG (reference, minor) | "*PNAS, 121*(47), e2409329121." |
| Willison 2025 | Quote on memory | Exact, inside quoted OpenAI text | CONFIRMED | |
| Willison 2025 | No evidence of a broad increase | "we don't have evidence that it broadly increases it" | CONFIRMED | |
| Willison 2025 | "Reproduces OpenAI's post" | It quotes excerpts with commentary | OVERSTATED (minor) | Body: "(as quoted in Willison, 2025)". Reference: "Quotes OpenAI's post." |
| Willison 2025 | Title, date, URL | Match | CONFIRMED | |

## Read in full or abstract

- Full text: Anthropic, Google, Campus Technology, Willison, NIE page, ANN article, Bergson (JAMA page), FRE 803 (rule and note), MOE both replies, Khan blog, Pew 2019 and 2025 pages (web report pages only), Bastani (PMC), Pan (PMC), Schroeder (PMC), Sultan (PMC), LearnLM (arXiv), Bo (arXiv), Sadler (hosted PDF), Morrin v5 (OSF PDF), Fricker 2017 (accepted version, White Rose), Lackey (author's draft), Kelly (pre-publication draft on a course site), Nguyen (first-view PDF hosted at Northeastern).
- For the full-text sources I searched and read the relevant passages, not every page, apart from the short web pages.
- Abstract or metadata only: Butterfield & Metcalfe (PubMed), Nan (PubMed abstract), Elish (journal abstract page).
- Not opened: Fricker 2007 (quotes seen only in Lackey), Soon & Goh full text, SSO text of the Evidence Act, GovTech SLS page.
