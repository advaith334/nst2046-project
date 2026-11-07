# Source check: machine-learning and AI papers

Checked 7 Nov 2026 against report text at git HEAD (`body_a.tex`, `body_b.tex`, `tutoring_values.tex`, `references.tex`), plus `appendices.md` Appendix D because Sharma and Zhan appear only there. Figures and findings below are paraphrased from the papers. Report wording is the report's own. Earlier notes in `report/literature/` were used as leads only.

Status for reference rows: WRONG means a title is cut short or a count is false. INCOMPLETE is an added label, meaning the arXiv record is right but a published or accepted venue is missing.

| Source | Report's claim (short) | What the source says, with section or page | Status | Exact replacement wording if not confirmed |
|---|---|---|---|---|
| Bensal 2026 | Five frontier models using hosted memory systems | §4 calls them frontier models; App. C says Mem0, MemOS and Zep ran through hosted APIs | CONFIRMED | |
| Bensal 2026 | Sonnet 4.6 rose from 1.6% to 40.2% on moral items | §4 and App. D table: 1.6% chat history to 40.2% Mem0, MIST-Moral | CONFIRMED | |
| Bensal 2026 | GPT-5.2 moved only 1.5 to 2.7 points on science items | App. L takeaways: delta about 1.5 to 2.7 points against chat history; Table 3 raw 1.1% to 2.6-3.7% | CONFIRMED | |
| Bensal 2026 | All four authors work for WRITER | Title block: all four at Writer, Inc. with writer.com addresses | CONFIRMED | |
| Bensal 2026 | WRITER has since launched a memory product | Not in the paper. WRITER engineering post dated 9 Sep 2026, "How we built Agent Memory", describes the product; the report gives no source | NOT FOUND IN SOURCE | Keep the sentence and add: WRITER. (2026, September 9). How we built Agent Memory: Goals, architecture, and engineering decisions. https://writer.com/engineering/building-agent-memory/ |
| Bensal 2026 | "Published work already shows" stored beliefs pull answers | arXiv comment says under submission, preprint; Xiang is a workshop paper | OVERSTATED | Prior work already shows that stored beliefs pull answers towards them. |
| Bensal 2026 | Generic disclaimer reduced sycophancy but was their only mitigation that lowered recall | §6 and Table 6: Moral 41.0 to 26.5, Science 4.3 to 2.4, LoCoMo-MC10 73.6 to 72.6; the only one to lower it | CONFIRMED | |
| Bensal 2026 | Ref: authors, title, Version 2, arXiv:2606.10949 | arXiv page matches; v2 of 24 Aug 2026 is latest | CONFIRMED | |
| Bensal 2026 | Ref: "the preprint states no competing interests" | v2 has no competing-interests statement at all (searched; App. A is LLM use, App. B impact). The report's wording reads as a declaration of none | OVERSTATED | All authors are employed by WRITER; the preprint carries no competing-interests statement. |
| Xiang 2026 | Llama-3.1-8B rose from 29.9% to 56.5-61.3% with memory systems on the factual task | Backbone table, Objective Fact Judgment, sycophancy rate: No Memory 29.92; Mem0 56.52 lowest; A-Mem 61.33 highest; Full Dialog alone 50.17 | CONFIRMED | |
| Xiang 2026 | Benchmark's memory states a preference; AI judge | App. A.3: preference memories; Fig. 14: rubric prompt judges free answers | CONFIRMED | |
| Xiang 2026 | Ref: authors, title, Version 3, arXiv:2607.01071 | arXiv page matches; v3 of 15 Oct 2026 is latest; PDF header marks the PALM workshop | CONFIRMED | |
| Jain 2026 | Links memory profiles to more agreement in personal advice | Abstract and §4.1: associated with the largest increases; holds for three of five models; advice scenarios from Reddit | CONFIRMED | |
| Jain 2026 | Ref including DOI | Crossref record for 10.1145/3772318.3791915 matches title, venue, authors, 2026 | CONFIRMED | |
| Pulipaka 2026 | Tested 18 | Abstract v1 and v2, §1, conclusion: 18 frontier and open-weight models | CONFIRMED | |
| Pulipaka 2026 | Extracted system prompts suggest static memories are added at the start of a conversation | §1: system prompt extraction suggests this, citing Khemani and an X user | CONFIRMED | |
| Pulipaka 2026 | Ref: authors, title, id | Correct; arXiv comment gives ICML 2026 | INCOMPLETE | Add: ICML 2026. |
| Mao 2026 | Tested 16 (body) | v5 of 10 Oct 2026 abstract: sixteen models. v1, v3 and v4 abstracts: twelve | CONFIRMED | |
| Mao 2026 | Appendix D row 2: before MS1 was submitted, PASB had tested 16 (Jul 2026) | July versions (v1-v3) and v4 of 27 Sep report twelve; sixteen appears only in v5 of 10 Oct. The appendix puts MS1 about 7 Oct (27 Oct was 20 days after "this week") | WRONG | Before MS1 was submitted, PersistBench had tested 18 (Feb 2026) and PASB 12 (Jul 2026; 16 from version 5, Oct 2026). |
| Mao 2026 | Ref: authors, title, id | Correct, but the model count depends on version | INCOMPLETE | Add (Version 5) after the title. |
| Yao 2026 | Find deference in base models | Abstract and §3.2: present in every base model | CONFIRMED | |
| Yao 2026 | Deference in every base model, capitulation after an objection added by post-training | Abstract, §3.3, §4: largely absent from base models, present in every post-trained checkpoint | CONFIRMED | |
| Yao 2026 | Ref | arXiv page matches | CONFIRMED | |
| Blank 2026 | Capitulation is traced to preference optimisation | §3.1: OLMo-3 rate more than doubles at DPO. §3.3: official Tülu-3 falls slightly from SFT to DPO; rises only with regenerated teacher data. Yao §3.3: Tülu-3 SFT is the most capitulating stage, DPO lowers it | OVERSTATED | ...capitulation after an objection added by post-training. Blank et al. (2026) show preference optimisation can raise it, depending on the teacher models, though Yao et al. find it already present at supervised fine-tuning. |
| Blank 2026 | Sycophantic agreement passes from teacher to student through data that looks neutral | Abstract, §3, §5.1 | CONFIRMED | |
| Blank 2026 | Ref | arXiv page matches | CONFIRMED | |
| Hannoon 2026 | Structure helps leakage and not sycophancy | Abstract; §3: 96.5% baseline to about 95%, too small to claim a fix | CONFIRMED | |
| Hannoon 2026 | Ref | arXiv page matches | CONFIRMED | |
| Ma 2026 | Warn that suppressing sycophancy can impair rational updating | Abstract: reducing unsupported yielding can sacrifice rational updating; pushback setting, no memory arm | CONFIRMED | |
| Ma 2026 | Ref title | arXiv title has a subtitle; comment gives EMNLP 2026 Findings | WRONG | Sycophancy suppression can impair rational updating: Anti-sycophancy should preserve the ability to update. Findings of EMNLP 2026. arXiv:2608.26511. |
| Du 2026 | Has no true arm | Limitations: experiments use incorrect assertions only; §4.3 dataset is factually incorrect | CONFIRMED | |
| Du 2026 | Has no evidence | No evidence passage, but §3.2 evidentiality varies the stated source: authority appeals, belief reports, hearsay | OVERSTATED | ...has no true arm, no independent evidence passage and no role frame, though it does vary the stated source and tone. |
| Du 2026 | Has no frame | No role or persona; tone is varied (§3.4); the paper itself says linguistic framing | CONFIRMED | See row above |
| Du 2026 | Ranks belief reports among the least persuasive ways to state a claim | §6.1 and Fig. 1: significantly less context-following than random baseline, with counterfactual, weak, interrogative. Its reports are about others, e.g. a brother | CONFIRMED | |
| Du 2026 | Ref | ACL Anthology BibTeX matches; pages 3137-3151, DOI 10.18653/v1/2026.acl-long.142 available. In-text "Du, Kümpel et al." is not APA for four authors | CONFIRMED | Optional: Du et al. (2026) |
| Genadi 2026 | Study pushback flips with no memory; MS1 misapplied them | Abstract, §1, §3: correct-to-incorrect flips after doubt, middle-layer heads; no memory condition (searched) | CONFIRMED | |
| Genadi 2026 | Ref | arXiv page matches | CONFIRMED | |
| Chen 2026 | Place stated opinions in early heads | Abstract, §3.2: sparse early heads carry the opinion; pushback uses a distinct set | CONFIRMED | |
| Chen 2026 | Ref | arXiv page matches | CONFIRMED | |
| De Marez 2026 | Instruct more robust in 17 of 23 pairs | Results: 17 of 23 Base-IT pairs, on worst-case flip rate; reversals at 4B or below plus Qwen3-14B. Nemo is not in the paper | CONFIRMED | |
| De Marez 2026 | Ref | arXiv page matches | CONFIRMED | |
| Shapira 2026 | "From inside the weights", falls in sycophancy track falls in updating from reliable sources (r = 0.87 to 0.90) | §3.4: r values are for system prompts (frontier) plus activation steering (open-weight), not weights. Values 0.87 frontier, 0.90 open-weight. Weight pruning is §4, a separate result with no r | OVERSTATED | Shapira et al. (2026) find the same with system prompts and activation steering: falls in following a user track falls in following a source described as reliable (r = 0.87 frontier, 0.90 open-weight). Pruning weights that support sycophancy also weakens correction from reliable sources. |
| Shapira 2026 | Ref | arXiv page matches | CONFIRMED | |
| Suzgun 2024 | Models can often represent a false belief as a belief, so the failure lies in use, not reading | Preprint's main finding is a systematic difficulty: false first-person belief 54.4%, third-person 80.7%, GPT-4 22.0%. Published version: third-person 95% newer, 79% older; first-person 62.6%, 52.5% | OVERSTATED | Models usually recognise someone else's false belief as a belief (95% in newer models, 79% in older; Suzgun et al., 2025), though far less often in the first person (62.6% and 52.5%), so for a third-person note the failure lies in how a record is used and not in reading it. |
| Suzgun 2024 | Ref | arXiv record correct, but published with a new title | INCOMPLETE | Suzgun, M., Gur, T., Bianchi, F., Ho, D. E., Icard, T., Jurafsky, D., & Zou, J. (2025). Language models cannot reliably distinguish belief from knowledge and fact. Nature Machine Intelligence, 7(11), 1780-1790. https://doi.org/10.1038/s42256-025-01113-8 |
| Kim 2026 | Models easier to persuade in multiple choice than in open diagnosis | Abstract, §4: all models, clear MC versus ambiguous cases. Format and dataset vary together; pushback, not memory | CONFIRMED | |
| Kim 2026 | Ref | ACL Anthology BibTeX matches; HeaLing 2026, pp. 19-34 | CONFIRMED | |
| Hong 2025 | With Ping: kappa from 0.63 to 0.92 by task | §4.4, Table 5: 0.917 Debate, 0.690 Ethical, 0.631 False Presupposition | CONFIRMED | |
| Hong 2025 | Ref | Correct; comment gives Findings of EMNLP 2025 | INCOMPLETE | Add: Findings of EMNLP 2025. |
| Ping 2026 | With Hong: validate AI judges against people | §3.5, App. B: kappa 0.866 on 480 items, inside the stated range | CONFIRMED | |
| Ping 2026 | Ref | Correct; comment gives Findings of EMNLP 2026 | INCOMPLETE | Add: Findings of EMNLP 2026. |
| Bo 2026 | 24 novices corrected wrong beliefs with low-sycophancy chatbot but not high | §4.3: within-subjects, n = 24. Low improved confidence-weighted score on wrong beliefs (p = .028), High did not (p = .77). Count of correct beliefs not affected (p = 0.62) | OVERSTATED | ...where 24 novices gained on wrong beliefs, in confidence-weighted score, with a low-sycophancy chatbot but not a high-sycophancy one (the count of correct beliefs did not differ), and 17 did not identify the difference as sycophancy, 12 of them noticing none. |
| Bo 2026 | 17 reported no difference | §4.5: 12 of 24 noticed none; 5 noticed slight differences but blamed other factors; 7 described sycophancy-related ones. Intro gives 71% as detecting none; 17 is not stated | WRONG | See row above |
| Bo 2026 | Ref | arXiv page matches; CHI 2026 | CONFIRMED | |
| Pugh 2026 | Self-report current but open to recall bias, record validated but often stale | Abstract and §1 | CONFIRMED | |
| Pugh 2026 | Ref note: all authors employed by Verily Health | Title block: Verily Health Inc., verily.health addresses | CONFIRMED | |
| Pugh 2026 | Ref title | arXiv title has a subtitle the entry drops; v1 is the only version | WRONG | Detecting clinical discrepancies in health coaching agents: A dual-stream memory and reconciliation architecture (Version 1). |
| Luz de Araujo 2024 | Persona effects can be large and unstable | Large: gap up to 38.56 points. Paper does not report instability. Paraphrases of one role sat near baseline; some rankings hold across models; refusals are arbitrary across similar personas | OVERSTATED | ...and persona effects can be large and similar personas can differ in refusal rates (Luz de Araujo \& Roth, 2025), so we fixed a planned test... |
| Luz de Araujo 2024 | Ref | Published; Crossref gives surname Luz de Araujo | INCOMPLETE | Luz de Araujo, P. H., & Roth, B. (2025). Helpful assistant or fruitful facilitator? Investigating how personas affect language model behavior. PLOS ONE, 20(6), e0325664. https://doi.org/10.1371/journal.pone.0325664 |
| Wu 2024 | Confidence gate keeps the no-memory answer when the model is sure | §4.4.1: compares token probability with and without context, no absolute threshold; retrieved documents, not memory | OVERSTATED | A confidence gate, which keeps the no-memory answer when the model is surer of it than of its with-memory answer, also deserves a live test (adapted from Wu et al., 2024, on retrieved documents). |
| Wu 2024 | Ref | Correct; Crossref lists NeurIPS 2024 proceedings | INCOMPLETE | Add: Advances in Neural Information Processing Systems 37. https://doi.org/10.52202/079017-1053 |
| Hendrycks 2020 | MMLU items, no AI wrote them | §2: collected by students from public sources; 15,908 questions | CONFIRMED | |
| Hendrycks 2020 | Ref | arXiv page matches | CONFIRMED | |
| Sharma 2023 | Appendix D row 8 only, no body citation | §7 and abstract match the appendix quotations | CONFIRMED | |
| Sharma 2023 | Ref | Metadata matches; 19 authors, id correct | CONFIRMED | |
| Zhan 2026 | Appendix D row 4 only, no body citation | Abstract, §5: 16.9 to 0.0; 50.3 to 40.5; generic warning 26.2 and 26.1 | CONFIRMED | |
| Zhan 2026 | Ref | arXiv page matches | CONFIRMED | |
| Bensal, Hannoon, Xiang, Jain, Genadi, Chen | Appendix D rows 1, 3, 6, 7, 9 | Figures match papers: Xiang 56.1 to 40.2 is on TruthfulQA, §2 | CONFIRMED | |
