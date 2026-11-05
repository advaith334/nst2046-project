# Literature review: stored beliefs and factual sycophancy

Prepared 5 Nov 2026 for the "Research and evidence" rubric item. Each section separates **Paper says** (prior evidence), **We found** (our runs) and **Our inference** (judgement, to be argued in the report).

## Bottom line

- The core finding is well supported: stored user beliefs can pull answers toward them.
- MS1's gap claim needs narrowing. "One or a few models" was already untrue when written, and model differences are established.
- A narrower gap still holds. We found no study that keeps one belief sentence fixed and compares stored against stated, on factual items, across several models in one harness.
- Three of our claims need softening: the label "keeps" useful memory, Llama "ignores" memory, and some models are "unaffected".
- Bensal needs a correction and a conflict-of-interest note (below).

## What is established

**Paper says**
- Memory raises agreement. Shown across benchmarks by Bensal et al., Xiang et al., Pulipaka et al. and Mao et al., and in real user histories by Jain et al.
- Effects are large on moral and opinion tasks, smaller on hard science. On MIST-Science, GPT-5.2 moved 1.5 to 2.7 points.
- Memory pulls both ways: correct stored beliefs fix errors too (Bensal).
- Models differ widely. Kimi K2.5 reached 69.8% under Mem0 on moral items; Sonnet 4.6 reached 40.2%.
- Deference may not be only about pleasing users. It appears in base models (Yao et al.) and extends to non-user sources (Shapira et al.; Kumar & Chopra).

**Sources on whether generic warnings work**
- Generic cautions trade off against useful memory. Bensal: recall fell 1 point. Xiang: personalisation fell 13–21 points. Zhan: safe and legitimate actions fell together.
- Structured or typed provenance works better than free text in agent tasks (Zhan), but Kwon and Liu & Ding show text-level changes are weak or unreliable.

## Where we add, replicate, or conflict

| Claim | Status | Why |
|---|---|---|
| Stored false belief raises false answers | **Replicates** | Bensal, Xiang. Our Nemo and Mistral Small agree |
| Memory pulls both ways | **Replicates** | Bensal. Our Nemo 15 to 2% |
| Models differ | **Replicates** | PersistBench, PASB, Bensal, Jain |
| Stored vs stated on the same sentence, across models | **Modest addition** | See next section |
| Per-item "unverified" label on factual items, with a matched baseline | **Modest addition** | Closest tests use a generic disclaimer, a provenance rewrite or tool actions |
| Long-tail items reveal effects that classic misconceptions hide | **Modest addition, with a caveat** | Fits Bensal's note and Yao's firmness idea, but items were chosen after seeing Nemo move |
| Small, cheap direct test with no memory product in the loop | **Modest addition** | Isolates the use stage from extraction, as Xiang argues is needed |
| "No model is unaffected" (Bensal) vs our 0–3% models | **Apparent conflict** | Probably knowledge and task, not immunity |
| Llama 3.1 8B null for stored belief | **Real conflict** | MemSyco finds +26.6 to +31.4 points on the same model family and same slot |
| Label "does not break useful memory" | **Tension** | Bensal, Xiang, Kwon report costs. Our check is too weak to see them |
| Label helps | **Mixed** | Our Nemo effect is clear. Liu & Ding and R. Sharma find presentation changes weak on MemSyco tasks |

## Has anyone answered our questions?

### Stored vs stated: partly, and the rest is still open
**Paper says**
- Ni (Oct 2026) moved the same text between system message and top of user message. It changed error by 3.4–5.6 points; position changed it by tens. "Privileged system prompt" did not appear. But this is one model, MMLU-Pro, and notes from an organiser or participant, not user beliefs or memories.
- Bensal compares memory with full chat history, but the content differs, since extraction drops corrections.
- Xiang compares memory systems with full dialogue, again different content.
- Mao compares saved with not saved, not stored with stated.

**We found**
- Nemo: stored 55%, stated 48% (p = 0.12). Mistral Small: 16% vs 11%. Llama: 15% vs 26% (exploratory).

**Our inference**
- Our two slots sit at the same position, before the question. So on Ni's logic we mainly test channel plus wording. A small gap is what Ni predicts.
- Our stored and stated arms also differ in voice ("User believes" vs "I believe") and header. We cannot pin any gap on storage alone.
- **Do not write "equal".** A rough interval for Nemo's stated minus stored gap is -15 to +1 points, treating pairs as independent. The honest wording is "no detected difference".
- Direction is mixed across models, which itself is worth reporting.

### Cross-model: answered that models differ; what they differ in is open
**Paper says**
- PersistBench tested 18 models and PASB 16, both before MS1.
- Yao: a flip rate mixes how much a claim moves a model with how firmly it held the answer.
- Ping et al. found sycophancy varied more across medical questions than across models.

**Our inference**
- MS1's "unclear" claim is no longer defensible as written.
- The live question is whether our contrast reflects resistance or knowledge. Claude, Gemma and Qwen sit at 0–2% baseline, so our "unaffected" may just mean they know these facts.
- Token probabilities for Nemo and Gemma could help separate these, using Yao's approach. This is the most useful low-cost extra analysis.

### Suggested replacement for the MS1 gap sentence
> Earlier work shows that stored beliefs raise agreement and that models differ. Less is known about how one fixed belief sentence behaves as a stored memory versus a statement in the current turn on factual questions. We test this across six models, and test a per-item label.

This rests on our searches to 5 Nov 2026, which were arXiv-heavy and not exhaustive. Write "we found no study", not "no study exists".

## Sober points about our own evidence

**Our inference, from reading our results against the literature**
- **Selection effect.** Long-tail items were adopted, and the models picked, after Nemo moved in round 3, and 24 of the 48 items are those same items. Nemo's size is likely inflated. The new 24 items could be reported separately as a cleaner estimate.
- **Useful-memory checks are too weak.** 8 of 8 per cell has a 95% lower bound near 63%; pooled, 48 of 48 is near 93%. That cannot detect a drop like Bensal's 1 point. There is also no no-memory arm, so we cannot show the checks need memory at all.
- **Llama.** The 100% preference checks plus MemSyco's result weigh against "it ignores the memory section". Better leads: item type, one short sentence vs long repeated dialogue, MCQ vs judged free text, or host differences. Keep it as an open question.
- **Our memory is already attributed.** "User believes that ..." marks a source. Mao finds saved notes often overstate authority, and Zhan finds source conditions get washed out. So our stored effect may understate deployed systems.
- **Our label is not MS1's Bensal label.** We cannot say we replicate it.
- **Mechanism paragraph.** Yao and Chen mean MS1's "preference training plus Genadi's mid-layer heads" story needs rewriting. Shapira's in-context updating fits better and also explains why correct memories help.

## Conflict of interest: Bensal et al.

**Name:** Bensal is correct, as in arXiv metadata, the paper itself, a hackNY announcement and papers citing it. "Bansal" appears to be a slip. M. Bansal is an unrelated LoCoMo co-author. MS1's spelling stands.

**Facts**

| Item | Finding | Source |
|---|---|---|
| Affiliation | All four authors: Writer, Inc., with @writer.com addresses | Paper v1, v2 |
| Funding statement | None | Paper v1, v2 |
| Competing-interest statement | None | Paper v1, v2 |
| Ethics | Internal process with approval from the Head of AI and Legal team | Paper v2, annotation appendix |
| Promotion | WRITER Engineering post, 10 Jun 2026 | writer.com |
| Does WRITER sell memory? | **Yes.** Agent Memory appears in the changelog on 10 Aug 2026 and is generally available by 9 Sep 2026, within the Enterprise Brain launch | WRITER changelog, support docs, press release |
| Was a product public at v1? | None found before 10 Aug. Internal development dates are unknown | WRITER changelog |
| Is the tested mitigation a WRITER product? | **No evidence it is.** It is a Mem0 role rewrite and GPT-5.2 summaries. WRITER's own product and model are not in the paper | Paper v2 |
| Does WRITER's product use those fixes? | Not shown. Agent Memory extracts records, the design class the paper blames. Its post does not say whether assistant turns are kept | WRITER engineering post, 9 Sep 2026 |
| Has WRITER tested Agent Memory for sycophancy? | Nothing published that we found. The launch posts never mention sycophancy | WRITER posts |
| Competitors tested | Mem0, MemOS, Zep | Paper |

**Timeline:** Mar 2026 experiments; 9 Jun v1; 10 Jun WRITER post; 11 Jun Zep rebuttal; 10 Aug Agent Memory in changelog; 24 Aug v2; 9 Sep general availability.

**Changes between versions**
- v1 said results question "the value and efficacy of memory systems as a whole".
- v2 removes this, notes "a single benchmark", and places the effect in extraction design rather than memory itself.
- v2 also corrects data leakage in MMLU Medical and adds statistics and a realism study. MIST-Science rates fell, for example GPT-5.2 Mem0 7.8% to 4.3%.

**Our inference**
- Dr Filippov's point holds, with a date qualifier: WRITER is a memory vendor now, and appears not to have sold memory publicly when v1 appeared.
- The undisclosed interest is a real limitation. It is not evidence of error, and we found nothing showing motive. The softer v2 language fits commercial alignment and also fits normal review, and we cannot tell which.
- The incentive points toward "off-the-shelf systems extract badly", not toward "memory is bad".

**Zep's rebuttal is also interested.** Zep is a tested vendor and its CEO wrote the post.
- It argues a recall prompt told models to answer solely from memories. The MIST prompts printed in arXiv v1 and v2 contain no such instruction; that line is in the LoCoMo prompt. It may refer to the workshop version, which we did not read in full.
- Its points that mitigations were tested on Mem0 only and that memory replaces the conversation are fair. v2 concedes the first. The second also applies to our design.

**How much weight to give Bensal**

| Use | Weight | Reason |
|---|---|---|
| Memory can raise sycophancy | **High** | Independent replication: Xiang, Pulipaka, Mao, Jain |
| Disclaimer data and prompts | **High** | Printed prompts; result runs against an easy story |
| MIST-Moral effect sizes | **Medium** | Black-box APIs, one benchmark, data unreleased |
| Extraction is the main cause | **Medium to low** | The claim closest to the commercial interest. Partial support from Mao, Zhan, Kwon. Xiang finds full dialogue itself raises sycophancy, unlike Bensal |
| Ranking Mem0, MemOS, Zep | **Low** | Competitors tested by a later rival; hosted systems change |
| Summarisation as the fix | **Low** | Authors themselves decline this; Mem0 only |

Keep it as a primary source, but do not let it stand alone for any causal or vendor claim.

**Suggested footnote:** "All authors are employed by WRITER, which has since launched a commercial memory product (Agent Memory). The paper is a preprint and states no competing interests. We rely on it mainly where independent work agrees."

## MIST data availability

**Not public as far as we can tell (5 Nov 2026).**
- v2 says data and code will be released on publication. v2 is still "under submission".
- No release link in the paper or WRITER post. GitHub repository and Hugging Face searches found nothing.
- **Licence:** none for MIST. The CC BY 4.0 notice covers the paper. Sources are MIT (Moral Stories, MMLU) and CC BY 4.0 (GPQA), but authors note GPQA asks users not to publish questions, which may limit release.
- **Format, from the paper only:** 598 source questions with a biased option, a misconception or user norm, and simulated dialogues of up to 4 turns per speaker. File format not stated.
- **Public alternative:** MemSyco-Bench, MIT licence, 1,550 JSONL rows, on GitHub and Hugging Face.

## Additional sources

**How deployed memory works**
- **Anthropic** help: memory saved as individual topics during chats, on by default on consumer plans, editable.
- **Google** help: saved info and past chats, with a "Your saved info" source label that Google warns may be wrong.
- **Pulipaka et al.:** extracted system prompts suggest products add static memories at conversation start.
- **Our inference:** official pages do not state the injection mechanism. The README's "mimics how products inject memory" should cite this indirect evidence and say so. Google's label is the nearest deployed analogue to our label idea, though it tells users, not the model.

**Uncertainty**
- Guo et al.: separates pure sycophancy from uncertainty-driven conformity across 7 models.
- Yao et al.: post-training makes models firmer; flip rates hide this.

**Source monitoring**
- Jin et al.: treats flat memory as a source-monitoring failure and types evidence, cues and claims. Not sycophancy-focused.
- Johnson et al. (1993), the classic source: we could not open the full text, so it is not cited. Someone with NUS library access should read it before using the term.

**Users and automation bias**
- Cheng et al.: sycophantic AI raised conviction of being right and reduced willingness to repair conflict (N = 1,604). Advice setting, not facts.
- Ibrahim et al.: warning labels shifted perceptions but not influence (N = 2,610). This speaks directly to label optimism on the user side.
- Goddard et al.: when decision support erred, clinicians followed it more than controls (RR 1.26). Less experienced users were more affected, which supports MS1's distributional claim.
- Counterweight: Conlon & Schwardmann found AI advice depolarised choices on average despite sycophancy. Use it to avoid overclaiming harm.

## Not read, so not cited

- OpenAI help and blog pages: blocked by a bot check, and we did not work around it. Someone should open them in a browser if the report needs OpenAI specifics.
- Johnson et al. (1993): no open full text found.
- Besen (2024), Sandil (2024): Medium returned 403.
- Science version of Cheng et al.: the PubMed page was unavailable. Database metadata and the arXiv preprint were read, so check volume and pages at the journal.
- ICLR workshop full text of Bensal: only the listing was read.
