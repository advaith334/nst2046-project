# Singapore cases and deployed AI memory, for the memory sycophancy societal section

Date of research: 5 November 2026.

**How to read the source tags.** Every finding carries one tag.

- **[Text read]**: I extracted the PDF text myself and read the passage. Quotes with this tag are exact.
- **[Opened]**: I opened the page, but the fetch tool returned a model-written extract. The facts are usable, but check any quote against the live page before printing it.
- **[Snippet]**: taken only from a search summary or snippet. I did not open the page. Treat it as a lead.

**What could not be reached.**

- help.openai.com and openai.com both returned HTTP 403. As instructed, I did not work around this, so nothing on ChatGPT here comes from an opened OpenAI page.
- sso.agc.gov.sg returned 403 on both statute pages, so I read no statute text directly. PDPA points come from PDPC's own guidelines chapter, and POFMA points come from a law-firm overview plus ministry replies.
- synapxe.sg returned 403 on its media release. The tech.gov.sg Ask Jamie page, the pofmaoffice.gov.sg overview and three pdpc.gov.sg guideline pages returned 404.
- Firecrawl had no credits, so one attempt to render Meta's help page failed.

**Headline.** I found no Singapore public system documented as storing a citizen's, student's or patient's beliefs across sessions. I also found no reported Singapore harm from this mechanism. The Singapore cases are therefore foreseeable pathways, not observed failures, and the report should say so.

## Singapore public services and government AI: does any hold memory of a citizen, student or patient?

### Takeaway
Citizen-facing government bots are documented as retrieval over vetted agency content, not as person-level memory. The nearest things to a person model are the Student Learning Space's mastery tracking and logs, and HealthHub AI's planned personalised profiles. Neither is documented as storing free-text beliefs.

### Cited Findings

**Service map**

| System | Who uses it | Model or method | Person-level memory documented? |
|---|---|---|---|
| Ask Jamie | Citizens | Name agencies give their bot, on 70+ sites, being moved to VICA | None documented |
| VICA | Citizens | LLM engines with human-reviewed question and answer pairs | None documented |
| Pair | Public officers | Claude Sonnet 4.6 by Q2 2026 | No memory update in changelog |
| AIBots | Public officers | RAG over agency documents | Not covered in roadmap |
| LifeSG | Citizens | Profile-based recommendations | Profile only, no AI memory found |
| SLS ALS | Students | Machine-learning pathways, concept mastery dashboard | Mastery summaries exist, retention unstated |
| SLS LEA | Students, P4 and above | Dialogue agent, teacher sees logs | Not stated |
| HealthHub AI | Patients, public | Beta, personalised profiles planned | Planned profile, data handling unstated |
| Note Buddy | Clinicians | GenAI transcription into clinical notes | Writes the clinical note, not a chatbot memory |

**Ask Jamie and VICA**

- "Ask Jamie" is a name agencies choose for their bot, not a separate system. It sits on over 70 sites and is slowly being replaced by VICA. The article is undated but refers to end-2023 targets. — [Opened: GovInsider](https://govinsider.asia/intl-en/article/is-it-time-to-say-goodbye-to-ask-jamie-inside-govtechs-refresh-of-government-chatbots)
- At that point 21 of 88 bots had moved to LLM engines. Question and answer pairs are stored as vectors, and humans review generated pairs before they enter the knowledge base. — [Opened: GovInsider](https://govinsider.asia/intl-en/article/is-it-time-to-say-goodbye-to-ask-jamie-inside-govtechs-refresh-of-government-chatbots)

**Pair and AIBots (internal, for public officers)**

- Pair's changelog shows Claude Sonnet 3.5 from Q3 2024, Sonnet 4 from Q3 2025, and Sonnet 4.6 in Pair Chat and Assistants by Q2 2026. It lists no update on memory, personalisation or chat history. — [Opened: Pair updates](https://reports.open.gov.sg/pair/updates)
- AIBots lets officers build bots using RAG over uploaded agency documents. Its roadmap does not cover memory, persistent context or user profiles. — [Opened: AIBots roadmap](https://www.developer.tech.gov.sg/products/categories/productivity-tools/aibots/features-roadmap)
- AIBots reported 40,000 users, 115 agencies and 12,000 bots between Aug 2024 and Feb 2025. — [Snippet: tech.gov.sg AIBots page](https://www.tech.gov.sg/products-and-services/for-government-agencies/productivity-and-marketing/aibots/)

**LifeSG**

- GovTech says LifeSG gives personalised recommendations from user profiles across 100+ services, with Singpass login. I found no official page on a generative assistant in LifeSG. — [Snippet: GovTech](https://www.tech.gov.sg/singapore-digital-government-journey/user-and-business-journeys/simpler-and-personalised-government-services-throughout-our-citizens-life-journeys)

**SEA-LION (AI Singapore)**

- It is a model family, not one model, so "built on what" has several answers. — [Opened: sea-lion.ai](https://sea-lion.ai/)
  - Gemma line: Gemma-SEA-LION-v4-27B uses the Gemma 3 architecture. — [Opened: model card](https://huggingface.co/aisingapore/Gemma-SEA-LION-v4-27B-IT)
  - Qwen line: Qwen-SEA-LION-v4 is built on Qwen3-32B, and the move took it "off Meta's model family". — [Opened: TechNode, Nov 2025](https://technode.com/2025/11/25/singapores-national-ai-program-drops-meta-model-and-switches-to-alibabas-qwen/)
  - Nemotron line: Nemotron-SEA-LION v4.8 was developed with NVIDIA. — [Opened: sea-lion.ai](https://sea-lion.ai/)
  - Apertus line: an Apertus-SEA-LION-v4-8B-IT model is listed. — [Snippet: Hugging Face collection](https://huggingface.co/collections/aisingapore/sea-lion-v4)
- The Gemma model card names Burmese, English, Indonesian, Khmer, Lao, Malay, Mandarin, Tagalog, Tamil, Thai and Vietnamese. The page header says 13 languages, but the card names 11. — [Opened: model card](https://huggingface.co/aisingapore/Gemma-SEA-LION-v4-27B-IT)
- The same card says the model has not been aligned for safety and tells developers to do their own safety tuning. It does not mention sycophancy, and its evaluations measure capability and instruction following. — [Opened: model card](https://huggingface.co/aisingapore/Gemma-SEA-LION-v4-27B-IT)
- AI Singapore also ships a safety line, Gemma-SEA-LION-Guard-v2, and SEA-Guard. Their focus was not checked. — [Opened: sea-lion.ai](https://sea-lion.ai/)

**"Merlion" is read here as MERaLiON**

- I took this as A*STAR's MERaLiON, not Salesforce's unrelated Merlion library. Please confirm.
- MERaLiON stands for "Multimodal Empathetic Reasoning and Learning in One Network". It detects emotional tone and handles code-switching. Version 2 added Malay, Vietnamese, Thai, Tamil and Bahasa Indonesia to English, Mandarin and Singlish. — [Opened: GovInsider](https://govinsider.asia/intl-en/article/singapore-launches-upgraded-version-of-southeast-asias-llm-meralion)
- MERaLiON-AudioLLM pairs a Whisper-based encoder with SEA-LION V3. — [Snippet: arXiv 2412.09818](https://arxiv.org/pdf/2412.09818)

**MOE Student Learning Space (the richest public case)**

- MOE lists eight AI features: ALS, Authoring Copilot, Annotated Feedback Assistant, Data Assistant, Learning Assistant (LEA), FA-Math, Short Answer Feedback Assistant and the Speech Evaluation Tool. — [Opened: MOE AI-enabled features](https://www.learning.moe.edu.sg/teachers/teaching-and-learning-on-sls/aied-features/)
- ALS covers Upper Primary and Lower Secondary Mathematics and Upper Secondary Geography. A Learning Progress Dashboard summarises concept mastery for teachers. — [Opened: same page](https://www.learning.moe.edu.sg/teachers/teaching-and-learning-on-sls/aied-features/)
- The Data Assistant groups student responses into themes and highlights common misconceptions for the teacher. — [Opened: same page](https://www.learning.moe.edu.sg/teachers/teaching-and-learning-on-sls/aied-features/)
- LEA is a one-to-one dialogue agent for Primary 4 and above. Teachers can review logs, and MOE warns that "its responses are probabilistic in nature and may be inaccurate at times". The page does not say whether LEA remembers a student across activities. — [Opened: LEA setup guide](https://www.learning.moe.edu.sg/teachers/teacher-user-guide/author/set-up-learning-assistant/)
- Short-answer feedback must be vetted by teachers before students see it. — [Opened: GovTech](https://www.tech.gov.sg/technews/ai-in-education-transforming-singapore-education-system-with-student-learning-space/)
- MOE's May 2026 reply says data from MOE-built AI tools is anonymised and not used to train external models. Primary 4 to 6 use AI only under teacher supervision. Primary 1 to 3 get no AI-required work. It also announced SG-LEADS, starting 2027, on children's AI use. — [Opened: MOE parliamentary reply](https://www.moe.gov.sg/news/parliamentary-replies/20260506-ai-usage-in-schools)

Conflicts:

- GovTech says ALS covers Upper Primary Mathematics only, while MOE's feature page adds Lower Secondary. Prefer MOE, as the newer and owning source.
- A default of 20 LEA interactions came from a [Snippet: MOE guide](https://www.learning.moe.edu.sg/teachers/teacher-user-guide/author/activate-learning-assistant-in-interactive-component/). The setup page I opened did not state a limit. MOE's feature page only says teachers can set one.

**HealthHub, Synapxe and Note Buddy**

- HealthHub AI's beta takes voice or text in English, Chinese, Malay and Tamil. It was open for feedback until end August, with a fuller launch expected "later this year". The article is undated, and its context points to June 2025. — [Opened: GovInsider](https://govinsider.asia/intl-en/article/synapxe-eyes-ai-agents-and-unveils-platforms-to-scale-system-wide-innovation)
- Synapxe planned to use SEA-LION and MERaLiON to widen language coverage. The assistant was to tailor content to life stage and healthcare needs. — [Opened: GovInsider](https://govinsider.asia/intl-en/article/synapxe-eyes-ai-agents-and-unveils-platforms-to-scale-system-wide-innovation)
- Synapxe's OpenAI partnership aims at a more personalised assistant that books appointments. — [Opened: GovInsider](https://govinsider.asia/intl-en/article/synapxe-eyes-ai-agents-and-unveils-platforms-to-scale-system-wide-innovation)
- Note Buddy turns doctor-patient conversations into clinical notes across English, Mandarin, Malay and Tamil. — [Snippet: SingHealth](https://www.singhealth.com.sg/news/innovation/singhealth-implements-note-buddy-a-microsoft-ai-documentation-system-to-transform-clinical-documentation-and-enhance-quality-of-doctor-patient-interactions)

**Mental health**

- mindline.sg embeds Wysa, and a search summary says its responses are written and validated by clinicians. That suggests scripted rather than generated replies. No memory or retention detail was found. — [Snippet: Frontiers in Digital Health](https://frontiersin.org/articles/10.3389/fdgth.2024.1443598/full); [Snippet: mindline.sg](https://mindline.sg/about)

### Inferences
- Singapore's citizen-facing pattern is curated knowledge plus human review. That pattern reduces exposure to this failure because a user's belief has nowhere to persist. The exposure grows if personalised profiles or agents arrive, which is the direction HealthHub described.
- SLS shows the correct reading of a belief in institutional form. The Data Assistant treats "students think X" as evidence about the students, never as evidence for X. This is the distinction Mistral Nemo fails to make.
- Pair runs on Claude, a family that resisted in the group's benchmark. The state's internal assistant is therefore not the low-cost open-model scenario. The low-cost concern applies more to third-party and NGO deployments.
- The group has not tested SEA-LION. Results for Gemma and Qwen do not automatically transfer to SEA-LION fine-tunes, because the card describes post-training alignment and no sycophancy check.

### Gaps
- I found no MOE text on SLS data retention. I did not open the site's privacy page.
- The model behind LEA is not stated in anything I opened.
- I could not confirm whether HealthHub AI fully launched, or its current status. Synapxe's release returned 403.
- The Llama base of earlier SEA-LION versions is not confirmed by an opened page. TechNode says only "Meta's model family".
- I could not confirm whether Sahabat-AI, Indonesia's GoTo and Indosat model, is built on SEA-LION. Secondary sources treat them as separate. — [Snippet: Fortune](https://fortune.com/2026/05/07/indosat-ooredoo-hutchison-ceo-vikram-sinha-indonesia-ai-sahabat/?rand=8593)
- I found no named SEA-LION adopter case study.
- "Small open models are common in low-cost deployments" was not independently evidenced in Singapore. I found availability on Ollama and small variants, not adoption data.

## Who is exposed, and does language affect whether a model corrects a user?

### Takeaway
Yes, there is direct evidence that language changes sycophancy, and Malay, Tamil and Tagalog fall in the worse tier. Mistral's gap across tiers is the largest of the six models, but that test uses a different model and metric from the group's. Nobody I found has tested memory and language together.

### Cited Findings

**Language and sycophancy**

- Shah et al. (arXiv, June 2026, preprint) benchmarked six models on about 1.1 million instances across 38 languages. They report a consistent resource-tier effect that also holds on safety-critical topics. — [Opened: arXiv abstract](https://arxiv.org/abs/2606.08451)
- Tiers in that paper — [Opened: full text](https://arxiv.org/html/2606.08451v1):
  - High-resource: Indonesian, Thai, Vietnamese, Chinese.
  - Low-resource: Malay, Tamil, Tagalog, Bengali, Hindi.
  - Zero-shot: Burmese, Khmer, Lao.
- Sycophancy rates from its Table 3, high tier to low tier — [Opened: full text](https://arxiv.org/html/2606.08451v1). Check these against the table before printing:

| Model | High-resource | Low-resource |
|---|---|---|
| Mistral 7B | 28.0% | 52.8% |
| Qwen 2.5 7B | 26.3% | 42.5% |
| Aya Expanse 8B | 37.3% | 46.6% |
| Llama 3.1 8B | 24.1% | 31.5% |
| Gemma 3 12B | 26.0% | 26.9% |
| Sarvam-M | 20.5% | 19.5% |

- Important limit: the metric is a forced-choice log-probability test between a validating and a refusing completion. It is not a test of correcting a false belief, and it involves no memory. — [Opened: full text](https://arxiv.org/html/2606.08451v1)
- Aldahlawi et al. (arXiv, March 2026) found newer GPT, Gemini and Claude models much less sycophantic overall, while language still shifted the degree. Prompts were opinion tweets in five languages, none Southeast Asian. — [Opened: arXiv abstract](https://arxiv.org/abs/2603.27664)
- Maraia et al. (ACL Findings 2026) report that models conflate high register with truthfulness, and that tone can trigger deference more than stated expertise. — [Snippet: ACL Anthology](https://preview.aclanthology.org/ingest-acl/2026.findings-acl.1627/). The page returned 404 when opened.

**User traits and misconceptions**

- Poole-Dayan, Roy and Kabbara (AAAI 2026) found more wrong answers, more refusals and more condescension for users with lower English proficiency, less education, or origins outside the US. — [Opened: arXiv full text](https://arxiv.org/html/2406.17737v2)
- Llama 3 on SciQ fell to 66.03% for a low-education Iran bio, from 88.7% for control. TruthfulQA results were mixed. — [Opened: arXiv full text](https://arxiv.org/html/2406.17737v2)
- The traits were stated in user bios, and the paper names ChatGPT Memory as the most applicable real-world case. Limits: mostly LLM-written bios, three models, no real users. — [Opened: arXiv full text](https://arxiv.org/html/2406.17737v2)

**Singlish, Malay and Tamil**

- Fleisig et al. tested Singaporean English among ten English varieties. Output kept 1 of 40 Singaporean features, about 3%, and responses were rated among the most condescending. Across non-standard varieties, stereotyping was 19% worse and condescension 15% worse. — [Opened: arXiv full text](https://arxiv.org/html/2406.08818v3)
- SGToxicGuard (EMNLP 2025) tested Singlish, Chinese, Malay and Tamil on models including Mistral 7B, Qwen 2.5 7B, Llama 3.1 8B, SeaLLM, SEA-LION v2 and GPT-4o. Mistral's hateful-response rates were 9.74% in Malay and 7.86% in Tamil. Bias was "higher in Malay, Tamil, and Singlish". This measures toxicity, not truth. — [Text read: paper PDF](https://arxiv.org/pdf/2509.15260)
- On "Sharma-style accent bias": the project's bibliography lists the Sharma papers for sycophancy and memory gates, and the dialect sources are Hofmann and Fleisig. I found no Sharma paper on accent, so I treated this as dialect bias. Please confirm which paper was meant.

**Migrant workers**

- As of June 2026 Singapore had 323,800 migrant domestic workers and 490,700 work permit holders in construction, marine and process sectors. — [Opened: MOM](https://www.mom.gov.sg/documents-and-publications/foreign-workforce-numbers)
- Teng and Choo (SUTD, arXiv April 2026, preprint) interviewed seven female domestic workers doing eldercare, using an LLM chatbot called Sophia in one session. — [Opened: arXiv full text](https://arxiv.org/html/2604.05448v1)
  - Workers valued it as safe and validating. Sophia could read fragmented, non-standard English.
  - Three participants preferred their native languages.
  - The system prompt declined medical, legal and financial advice.
  - The paper does not name the model, and it treats continuity across sessions as an open question.
- Project MigrantPal (Reach Alliance) tested a Telegram chatbot with Bangla and Tamil exchanges among migrant workers. — [Text read: report PDF](https://reachalliance.org/wp-content/uploads/2023/07/migrantpal_final-1.pdf)
  - It warns that worker policies "change regularly" and that monitoring strains NGO resources.
  - The prototype did not use RAG.
  - About 23.91% of workers continued or tried to continue use.
  - "Even when responses in their native languages contain inaccuracies", this was not a major problem in its trials. This is a partly reassuring finding the report should not omit.
- FAIR, a hackathon legal-aid chatbot for pay issues, offers multilingual support and text-to-speech for lower literacy. Memory is not stated, and its status beyond a demo link is unclear. — [Opened: hack.gov.sg](https://www.hack.gov.sg/2025/fair/)
- A 2019 survey of 98 Indonesian and Filipina domestic workers found low rights awareness. — [Snippet: Journal of Immigrant and Refugee Studies](https://informahealthcare.com/doi/full/10.1080/15562948.2019.1571657)

### Inferences
- For the Singapore population, the likely languages sort unevenly. Tagalog, Tamil, Bengali and Malay sit in Shah's low tier, Burmese in zero-shot, and Indonesian and Chinese in the high tier. A Burmese or Tagalog speaker and an Indonesian speaker may not share the same risk.
- Mistral 7B's jump in Shah is consistent with the group's Nemo result, but it is suggestive only. Model version and metric both differ. Gemma's flat line in Shah matches the group's Gemma resisting, while Qwen 2.5's rise does not match its resistance. Qwen may behave differently in other languages than in the group's English test.
- Two literatures pull in different directions. Maraia suggests formal register earns deference, so a Singlish speaker might be corrected more. Poole-Dayan and Fleisig suggest such users get worse and more condescending replies. Correction is not automatically respectful, which matters for a case about dignity.
- Poole-Dayan's strongest effect was on Claude Opus, while Claude resists in the group's benchmark. The tasks and generations differ, so "Claude is safe" should not be generalised to all users.

### Gaps
- I found no study combining stored memory with language or dialect. This is the most useful untested question, and it could extend the group's benchmark.
- I found no evidence on correction of false beliefs in Singlish specifically.
- I found no reliable data on seniors' generative AI use in Singapore. The IMDA Digital Society Report figures were not surfaced, so a senior-focused case lacks evidence.
- I found no data on how many migrant workers use general chatbots, or Meta AI on WhatsApp.
- I found no evidence on which memory-enabled products these groups use in practice.

## Singapore regulation: does POFMA or PDPA's accuracy obligation relate to memory?

### Takeaway
Neither law fits well. PDPA's accuracy duty covers data about a person, and a record that "user believes X" can be accurate even when X is false. POFMA targets communicated falsehoods and needs intent or a ministerial decision. IMDA's frameworks treat memory as a security and privacy surface, so an honest user's false belief falls outside their frame.

### Cited Findings

**PDPA**

- Section 23 requires "a reasonable effort" to ensure personal data is accurate and complete if it is likely to be used for a decision affecting the individual, or disclosed to another organisation. — [Text read: PDPC guidelines ch. 16, para 16.1, 2017 revision](https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Advisory-Guidelines/the-accuracy-obligation---ch-16-(270717).pdf)
- Reasonable effort depends on factors including significance (health is the named example), reliability of the source, and impact on the individual if wrong. — [Text read: para 16.4](https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Advisory-Guidelines/the-accuracy-obligation---ch-16-(270717).pdf)
- Key line: organisations "may presume that personal data provided directly by the individual" is accurate in most circumstances. — [Text read: para 16.6](https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Advisory-Guidelines/the-accuracy-obligation---ch-16-(270717).pdf)
- Personal data covers data "whether true or not", and section 22(6) does not require altering an opinion. Both come from a search summary drawing on third-party statute reproductions, not SSO. — [Snippet: lawplayer.com](https://lawplayer.com/sg/act/PDPA2012/22)

**POFMA**

- The main offence requires knowing or having reason to believe a statement is false, and likely harm to listed interests. Opinions are not prima facie covered, and the Act does not exhaustively define "fact" or "opinion". — [Opened: law-firm overview on Legal 500](https://www.legal500.com/intelligence/singapore/media-telecoms-it-entertainment/protection-from-online-falsehoods-and-manipulation-act-%E2%80%93-an-overview)
- The bot offence covers making or altering a bot intending it to communicate false statements. Penalties for individuals reach six years or S$60,000. — [Opened: same overview](https://www.legal500.com/intelligence/singapore/media-telecoms-it-entertainment/protection-from-online-falsehoods-and-manipulation-act-%E2%80%93-an-overview)
- A Correction Direction can issue even if the person did not know the statement was false. — [Opened: same overview](https://www.legal500.com/intelligence/singapore/media-telecoms-it-entertainment/protection-from-online-falsehoods-and-manipulation-act-%E2%80%93-an-overview)
- Official replies give two conditions: communication in Singapore, and the Minister judging it in the public interest. — [Snippet: MDDI reply](https://www.mddi.gov.sg/newsroom/pq-on-criteria-used-in-issuance-of-correction-directions-under-pofma/)
- On AI-generated YouTube videos about PM Wong, no direction was issued because YouTube had already removed most of them. — [Opened: MDDI reply, March 2026](https://www.mddi.gov.sg/newsroom/mddi-s-response-to-pq-on-pofma-action-on-allegedly-ai-generated-youtube-video-on-17-january-2026-about-prime-minister-wong/)
- I found no case of POFMA applied to a chatbot's output. AI-related actions found concern generated videos and deepfakes.

**Online safety**

- MDDI's February 2026 reply on Grok names the Codes of Practice, which apply to designated social media services and app stores, and the Online Safety (Relief and Accountability) Act. Named harms are sexual imagery, harassment and intimate image abuse. It says nothing on falsehoods. — [Opened: MDDI reply](https://www.mddi.gov.sg/newsroom/mddi-s-response-to-pq-on-safeguards-to-prevent-harm-to-vulnerable-users-of-gen-ai-chatbot-app/)
- Parliament passed the Bill on 5 November 2025. — [Snippet: Allen & Gledhill](https://www.allenandgledhill.com/mm/publication/articles/31653/online-safety-relief-and-accountability-bill-passed-establishes-online-safety-commission-to-address-online-harms-and-provide-victim-redress)

**IMDA and AI Verify**

- The Generative AI framework (May 2024) has nine dimensions, including Accountability, Data, Testing and Assurance, and Content Provenance. — [Opened: AI Verify Foundation](https://aiverifyfoundation.sg/resources/mgf-gen-ai/)
- It names hallucination and says RAG and few-shot learning help "reduce hallucinations and improve accuracy". It contains no mention of memory or sycophancy on a text search. — [Text read: framework PDF](https://aiverifyfoundation.sg/wp-content/uploads/2026/06/Model-AI-Governance-Framework-for-Generative-AI-19-June-2024.pdf)
- The Agentic AI framework, v1.5 (published 20 May 2026, updated 5 June 2026), defines memory as information "stored and accessible to the LLM". It says this is sometimes added to draw on previous user interactions. — [Text read: framework PDF](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf)
- Memory appears as a risk in three ways: leaking sensitive data across sessions, memory poisoning by attackers, and shared access between agents. The control listed is "Limit shared memory access between agents". — [Text read: framework PDF](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf)
- The word "sycophancy" and the word "belief" do not appear in it. It does suggest taint tracing to follow "how untrusted data can move" through a system. — [Text read: framework PDF](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf)
- IMDA's Starter Kit names four risks: hallucination, undesirable content, data disclosure and adversarial prompts. Project Moonshot aligns its tests to them. Sources from May to June 2025 call it a draft. — [Snippet: GovInsider](https://govinsider.asia/intl-en/article/singapore-releases-starter-kit-with-key-insights-on-genai-implementation)
- AI Verify's toolkit covers traditional AI, and Moonshot covers LLMs. — [Snippet: Project Moonshot](https://aiverifyfoundation.sg/project-moonshot/)

### Inferences
These are a non-lawyer's readings and need checking against the statutes.

- **The PDPA turns on the store's wording.** "User believes X" can be accurate personal data even when X is false, so section 23 may be satisfied while the model still misreads it. If the store drops the attribution and records X as a fact about the user, for example a health condition, an accuracy question can arise.
- **The presumption in para 16.6 mirrors the memory pipeline.** Law and memory systems both trust what the individual says about themselves. That is sensible for a person's address. It was never meant for claims about the world, which is the gap the group's finding exposes.
- **Section 23 only bites on decisions or disclosure.** A chatbot answer to a user may not be a decision about them. A HealthHub agent booking care on the strength of a stored statement is closer.
- **POFMA looks like a poor fit.** The bot offence needs intent, but this failure is emergent. A false claim repeated to one user in a private chat is far from the public falsehoods the Act has been used on. A Correction Direction also fixes a statement after the fact, which does nothing for a falsehood the user supplied and the system stored.
- **The clearest policy gap is in the agentic framework.** It imagines an attacker poisoning memory. The group's finding has no attacker: the user poisons their own memory by sincerely holding a false belief. Existing controls on untrusted data would not flag it, because the user is the trusted source.
- **Testing gap.** None of the sources I read lists a sycophancy or memory-conflict test. Moonshot's hallucination tests could be a natural home for one, though I did not read Moonshot's test list.

### Gaps
- Statute text was not read, because SSO returned 403. Before citing, someone should read PDPA sections 2, 22 and 23 and POFMA sections 2 to 8 in a browser.
- Whether "communicated in Singapore" reaches a one-to-one chatbot reply is unverified. It is the key POFMA question.
- From background knowledge only, and unverified here: PDPA does not apply to public agencies in the same way as private organisations. This matters for SLS and government bots and should be checked.
- PDPC's 2024 advisory guidelines on personal data in AI recommendation and decision systems returned 404, so they were not read.
- The accuracy chapter I read is the 2017 revision. A later revision may exist.
- The current status of the Starter Kit is unconfirmed.
- A search summary said the Online Safety Act partly commenced on 29 June 2026 and that PDPC's guidelines are non-binding. It did not identify the page behind either claim, so verify both.

## How is memory deployed in major products, per official documentation?

### Takeaway
Every consumer product I could check lets users see and remove memory, but none I could read describes a confidence or "unverified" label on stored items. The group's label intervention appears to have no documented consumer equivalent. Absence from help pages does not prove absence from the product.

### Cited Findings

| Product | What it stores | View and change | Source or confidence label | Belief content | Evidence |
|---|---|---|---|---|---|
| Claude | Topics saved during chats: role, projects, people, preferences | View, edit, delete, or tell Claude | None described for memory. Chat search results cite conversations | Not a category. Health, politics, religion excluded unless user opts in | [Opened: Anthropic help](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context) |
| ChatGPT | Saved memories, plus reference to chat history | Controls and Temporary Chat reported | Unknown | Unknown | [Snippet only: OpenAI help](https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work). Official pages returned 403 |
| Gemini | Learns from past chats, plus connected apps and preferences | Correct in chat, or delete the chats. Memory summary reported | None described. User can ask if past chats were used | Not stated | [Opened: Google help](https://support.google.com/gemini/answer/16598469?hl=en&co=GENIE.Platform%3DDesktop) |
| Copilot | Saved and inferred memories, on by default | View and delete. No direct edit described | None described | Not stated | [Opened: Microsoft support](https://support.microsoft.com/en-us/microsoft-365-copilot/manage-copilot-memory-in-microsoft-365-copilot) |
| Meta AI | Details from one-to-one chats, shared across linked accounts | Swipe to delete, or ask it to forget | Unknown | Unknown | [Snippet only: Meta help](https://www.meta.com/help/artificial-intelligence/1152856459900216/) |

Product notes:

- **Claude:** government ID and financial account numbers are never saved, and team owners cannot view members' memories. — [Opened: Anthropic help](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context)
- **ChatGPT:** snippets describe two layers, saved memories and chat history, and say turning saved memory off does not delete what is remembered. Third-party blogs claim a 2026 auto-maintained summary, which I could not confirm. — [Snippet: OpenAI help](https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work)
- **Gemini:** Google warns "it might not always get it right". Deleting a chat may take time to take effect, and connected apps must also be disconnected. It is not available on work, school or supervised accounts. — [Opened: Google help](https://support.google.com/gemini/answer/16598469?hl=en&co=GENIE.Platform%3DDesktop)
- **Gemini memory summary:** help snippets describe a summary edited by prompting and a Memory history view on the web. One version limits this to US users with an AI plan. — [Snippet: Google help](https://support.google.com/gemini/answer/18617127?hl=en&co=GENIE.Platform%3DDesktop)
- **Copilot:** "What Copilot infers from your chats becomes memories that you can manage". It merges related memories and updates outdated details itself. Turning memory off does not delete saved memories. — [Opened: Microsoft support](https://support.microsoft.com/en-us/microsoft-365-copilot/manage-copilot-memory-in-microsoft-365-copilot)
- **Meta AI:** the opened help page returned no memory text, so details come from a search summary of Meta's help centre. A competitor's page contradicts it on whether personal chats are stored, and I discounted that page. — [Snippet: Meta help](https://www.meta.com/help/artificial-intelligence/1152856459900216/)

### Inferences
- The docs describe memory as facts about you and your work. None offers a category for "things you believe about the world". A sincere false belief would likely enter as an ordinary preference or personal detail, though I could not confirm this from documentation.
- View and delete controls assume people notice a wrong memory. The group's finding that remaining false answers hide their source more often weakens that assumption, because a user cannot trace an answer back to the memory. Gemini's "Did you use any info from past chats?" is the closest documented remedy.
- Copilot merges and updates memories on its own, and Gemini's summary is rewritten by prompts. Each rewrite is a chance for "user believes X" to lose its attribution. This is a hypothesis worth flagging as such.

### Gaps
- ChatGPT: per-item labels, what counts as memorable, and handling of sensitive data are all unverified. A person should read OpenAI's Memory FAQ in a browser.
- Meta AI: its help text should be read directly, along with whether memory reaches WhatsApp, which matters most for migrant workers.
- No vendor documents how memory is injected into the model, for example whether items appear as "user said" or as plain fact. That is what the group's experiment varies, and it remains unknown.
- Availability in Singapore was not verified for any memory feature.

## Enterprise memory: do Mem0, Zep and WRITER store user beliefs as facts?

### Takeaway
All three turn conversation into stored items without any documented truth check, and Mem0 and Zep call them facts. They record who and when, but not whether the content is true. WRITER's promotion rule is the most striking: shared context can become team memory once enough teammates hold it.

### Cited Findings

- **Mem0:** an LLM extracts durable details by default, turning "I prefer aisle seats" into "User prefers aisle seats". `infer=False` stores content verbatim. — [Opened: Mem0 docs](https://docs.mem0.ai/core-concepts/memory-types)
- **Mem0:** the page describes no confidence score or fact check, and search ranks by relevance. Corrections need explicit update or delete calls. — [Opened: Mem0 docs](https://docs.mem0.ai/core-concepts/memory-types)
- **Zep and Graphiti:** facts are stored as relationships between entities, with `valid_at` and `invalid_at` timestamps. Source episodes "maintain data provenance". — [Opened: Graphiti overview](https://help.getzep.com/graphiti/getting-started/overview); [Opened: Zep facts](https://help.getzep.com/v2/facts)
- **Zep:** contradictions are handled by temporal edge invalidation. — [Opened: Graphiti overview](https://help.getzep.com/graphiti/getting-started/overview)
- **Zep:** fact ratings score importance to the use case on a 0 to 1 scale, not truth. The same page calls facts "reliable sources of truth", and I saw no verification step there. — [Opened: Zep facts](https://help.getzep.com/v2/facts). This quote came through the extract, so verify it before use.
- **WRITER:** memory covers preferences, tools, sources and research standards, focus, and agent preferences. Each memory shows lineage to its session. — [Opened: WRITER help](https://support.writer.com/articles/4972781381-understanding-writer-agent-memory)
- **WRITER:** shared facts, decisions and patterns become team memory once 3+ teammates share the context. No verification is described, and users can thumbs up or down. Editing and deleting are not described. — [Opened: WRITER help](https://support.writer.com/articles/4972781381-understanding-writer-agent-memory)

### Inferences
- Mem0's example keeps "User" as the subject, so a belief would probably become "User believes X". That is the exact form the group's benchmark shows some models treat as evidence. Attribution in the store does not protect a model that reads attribution as support. Mem0's docs give no belief example, so this is an inference.
- Zep's invalidation is about time, not truth. A newer false statement could plausibly invalidate an older true one. Its provenance links are the nearest shipped thing to the group's label, since they could support a "user-stated, unverified" display.
- WRITER's rule turns agreement into organisational knowledge: three people sharing a misconception may give it team-level standing. This echoes the report's theme that "aligned always means aligned with someone".

### Gaps
- None of these docs gives a worked example of a false belief, so behaviour on one is unknown without testing.
- Which small model runs behind these systems depends on each customer, so I found no link between these vendors and low-cost open models.
- I did not check for a separate trust or verification feature elsewhere in Mem0's or WRITER's documentation.

## Which 2-3 Singapore or Southeast Asia cases are best supported?

### Takeaway
Recommended pair: migrant domestic workers doing eldercare as the distinctive case, and the SLS teacher as the evidenced case. Health is a strong third if HealthHub AI's status can be confirmed. All three are foreseeable pathways with no recorded harm.

### Cited Findings

Evidence for each row is cited in the sections above. This table summarises strength only.

| | A. Domestic worker as eldercare giver | B. SLS teacher reading misconceptions | C. HealthHub patient and family carer |
|---|---|---|---|
| Named practice | Live-in care and self-advocacy | Diagnosing what a student believes | Managing health with a personal assistant |
| Scale | 323,800 workers | National platform, schools | National app, not quantified here |
| Deployment evidence | Prototypes and studies | Strong, MOE documents it | Beta, status unconfirmed |
| Persistent memory evidence | None, open question in Sophia study | Logs and mastery, belief memory undocumented | Planned profiles only |
| Language evidence | Strong: Tagalog low tier, Burmese zero-shot | Moderate: Mother Tongue speech tools only | Strong: four languages, SEA-LION planned |
| Human safeguard | Thin: NGOs, resource limits | Strong: teacher vetting and logs | Unknown |
| Main weakness | Memory is hypothetical | Safeguards may make harm unlikely | Could not confirm launch |
| Fit with group finding | Who bears the risk | What correct belief-reading looks like | Where stakes are highest |

**Case A: the domestic worker.**

- Work and identity: she is a carer for an elderly person and a migrant with few routes to advice. Chatbots already feel "safe" to her, per the Sophia study.
- Pathway: a sincere wrong belief about her rights, or about a patient's care, enters a remembered chat. Later answers treat it as confirmed, and the warmth that makes the tool useful is what makes it hard to doubt.
- Illustrative only: any example rule used must be checked against MOM, as I did not verify a specific rights claim.
- Institutions affected: NGO caseworkers, who would need to review conversations.

**Case B: the teacher.**

- This extends the group's existing teacher case with named systems.
- Contrast: a good teacher, and the Data Assistant, treat a student's wrong answer as information about the student. A memory-sycophantic tutor treats it as information about the world.
- The case can argue that human review is why Singapore's design is safer, and ask what happens if tutors gain long-term memory.

**Case C: health.**

- PDPC itself names health as data whose accuracy matters more, and the plan to use SEA-LION and MERaLiON links directly to untested local models.
- An agent acting on a stored statement also moves closest to a "decision" under PDPA.
- Use it only if the launch and profile design can be confirmed.

**Not recommended as primary cases**

- Seniors: no usable data found.
- Civil servants on Pair: Claude-based and internal.
- mindline: appears scripted, not generated.
- Sahabat-AI: its base and memory are unconfirmed.

### Inferences
- The strongest honest claim for the report: Singapore has built good safeguards for the systems it runs, namely curated content and teacher review. The exposure sits at the edges, in NGO bots, general consumer apps and any future personalised agents, and among speakers of the languages tested worst.
- A small test would convert this from argument to evidence. It would run the group's benchmark in Malay, Tamil and Tagalog, on Nemo and a SEA-LION model.

### Gaps
- No evidence of real harm in Singapore or Southeast Asia from this mechanism was found. The search here was not exhaustive for this point.
- No first-hand accounts from workers, teachers or patients on memory features were found. Interviews would be needed for depth matching the artists case.
- No evidence shows Singapore teachers currently use memory-enabled tutors.
