# MS1 citation check

Checked 5 Nov 2026 against the papers themselves. Where a paper has several versions, the latest was read (and earlier ones where they differ).

**Status key:** OK = accurate. Fix = small correction. Wrong = the paper does not say this or says the opposite.

## Errors that must be fixed before the final report

| # | MS1 says | Paper really says | Severity |
|---|---|---|---|
| 1 | Bensal: "Labelling stored beliefs as unverified user claims reduced the effect without harming recall." | No such label was tested. Bensal tested one generic disclaimer after the whole memory block, saying memories may reflect opinions or misconceptions. It lowered sycophancy (MIST-Moral 41.0% to 26.5%; MIST-Science 4.3% to 2.4%), but it was the **only** mitigation that lowered recall (LoCoMo-MC10 73.6% to 72.6%). The authors say such disclaimers "may interfere" with useful memory. The two mitigations that kept recall were assistant-role inclusion and summarisation. | Wrong, and it props up our label argument |
| 2 | "Existing studies also test one or a few models" | Bensal 5, Jain 5, Xiang 5, Hannoon 7, Zhan 7. Before MS1 was submitted, PersistBench had tested 18 (Feb 2026) and PASB 16 (Jul 2026). | Wrong |
| 3 | "labels and structure help" (citing Hannoon alongside) | Hannoon: structure "does not substantially reduce memory-induced sycophancy" (96.5% to about 95%). Structure helped cross-domain leakage only. | Wrong for sycophancy |
| 4 | Zhan: "restoring labels at retrieval removed it" | Labels were predicted and persisted with the memory, then shown at action time. The outcome was unauthorised **tool actions** (16.9% to 0.0%, one selected pipeline), not factual sycophancy. Plain-text provenance cut it only from 50.3% to 40.5%. A generic warning cut safe and legitimate actions alike (26.2% vs 26.1%). | Wrong mechanism and wrong outcome type |
| 5 | Xiang author "Li, Y." | **Lin, Y.** (Yujie Lin), in arXiv metadata and all checked versions. | Reference error |
| 6 | Xiang: "incorrect memory snippets lowered accuracy by up to 16%" | The figure is right as 15.9 **percentage points** (56.1% to 40.2%, DeepSeek-V4-Flash), or 28% in relative terms. But it comes from a preliminary test where the cue sits inside the question on TruthfulQA items, so it is not a stored memory. | Fix wording and context |
| 7 | Jain: "caused the largest rise" | Paper says "associated with". The design is a regression, and it was largest for three of five models only. Llama 4 Scout and GPT 5.1 showed no significant rise. | Fix |
| 8 | Sharma: raters "often preferred the agreeable answer" | Humans and preference models "tend to prefer truthful responses but not reliably". Abstract: "a non-negligible fraction of the time". Cause is "likely driven in part" by preferences. | Overstated |
| 9 | Genadi locates the belief shift in mid-layer attention heads | Genadi studies correct-to-incorrect flips after **user pushback** ("are you sure?"), on Gemma-3-4B and Llama-3.2-3B, with no memory. Chen et al. (2026) find stated opinions and content-free pushback use distinct heads, with early heads carrying stated opinions. | Misapplied in the mechanism section |

## Paper by paper

### Bensal et al. (2026), arXiv:2606.10949
- **Spelling:** Bensal is correct. "Bansal" is not. Authors, title and id all OK.
- **Versions matter.** v1 (9 Jun) abstract says "up to 25x" and two mitigations. v2 (24 Aug) says "up to 40%" and three. Cite v2.
- **"up to 40%": Fix.** It matches the v2 abstract, but no table gives a plain 40% rise. Closest: Sonnet 4.6 on MIST-Moral went from 1.6% to 40.2% (38.6 points, about 25x). The largest gap in Table 7 is Kimi K2.5, 16.2% to 69.8% (53.6 points). Quote the raw rates, not "40%".
- **Domain caveat, missing from MS1.** The big effects are moral. On MIST-Science, GPT-5.2 moved only 1.5 to 2.7 points (Appendix L).
- **Lossy extraction: OK but soften.** Authors call extraction the primary culprit. But sycophancy did not track compression ratio, and they locate the effect in extraction design.
- **"memory systems keep short snippets and drop later corrections": OK.**
- Status: preprint, "under submission". An earlier version was an ICLR 2026 workshop poster with a different subtitle.

### Xiang et al. (2026), arXiv:2607.01071
- Title and id OK. Latest is v3 (15 Oct). Marked for the PALM workshop.
- **Author list:** "Li, Y." should be "Lin, Y." Ning's first name appears as both Ruqin and Ruqing. The initial is unaffected.
- **Task description: OK** (reject memory as evidence, scope, conflict). There are also two personalisation tasks.
- Better figure for us: Objective Fact Judgment, stored memory, Llama-3.1-8B sycophancy 29.92% to 56.52–61.33%.

### Jain et al. (2025), arXiv:2509.12517
- Title, authors, id OK. Now published at CHI 2026, DOI 10.1145/3772318.3791915. Update the reference.
- **"+45%": Fix.** It is a regression coefficient of 0.450 for Gemini 2.5 Pro, so read it as about 45 percentage points on a 30% zero-shot base, not "45% more often".
- **Task caveat:** "agreement sycophancy" is moral endorsement in personal-advice scenarios, not factual answers.
- **Confound:** the authors note personalisation instructions in the system prompt may matter more than user context.

### Zhan et al. (2026), arXiv:2608.01679
- Title, authors, id OK.
- "consolidation keeps a claim but loses its source": OK.
- "restoring labels at retrieval removed it": Wrong, see error 4. Not a sycophancy study.

### Hannoon et al. (2026), arXiv:2608.08300
- Title, authors, id OK.
- "reduced cross-domain leakage by partitioning": OK (8.8% average, strongest method).
- Implied sycophancy benefit: Wrong, see error 3.

### Genadi et al. (2026), arXiv:2601.16644
- Title, authors, id OK.
- "linearly separable ... can be steered": OK as a finding on pushback flips. Misapplied to stored beliefs, see error 9.

### Ma et al. (2026), arXiv:2608.26511
- Title, authors, id OK. Accepted to EMNLP 2026 Findings. Update the reference.
- Trade-off claim: OK. Note it tests training and steering, not prompt labels, and has no memory condition.

### Sharma et al. (2023), arXiv:2310.13548
- Title, all 19 authors, id OK. Latest arXiv version is v4 (May 2025). Five assistants: OK.
- Preference claim overstated, see error 8.

## Non-academic sources

| Source | Result |
|---|---|
| Georgetown Law (2025) | Exists. Lists emotional harm and self-harm. Memory appears only as open questions, no findings. No named author. Publisher shown as Institute for Technology Law & Policy. Fine for "documented harms" framing only. |
| Genmind (2026) | Exists, but it is a vendor marketing blog citing no named studies. Replace with Dubois et al. (2026) for framing effects. |
| Besen (2024), Sandil (2024) | **Could not open** (HTTP 403). Not verified. Both are Medium posts, so drop them. For memory benefits, use official product documentation (see `references.md`). |

## Not checked as citations
The lecturer's name is spelled "Fillippov" on the MS1 cover and "Filippov" in the README. Worth confirming.
