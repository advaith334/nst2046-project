# Comparison of the closest studies

All figures are from the papers. "pp" means percentage points. Our row is from the README and `runs/main-20261027`, and is our own finding, not prior evidence.

## Main table

| Study | Models | How memory gets in | Items | Metric | Key effects | Mitigation tested |
|---|---|---|---|---|---|---|
| **Bensal et al. 2026** (v2), MIST | 5 frontier: GPT-5.2, Sonnet 4.6, Qwen 3.5, Kimi K2.5, MiniMax 2.5 | Simulated chats pass through hosted Mem0, MemOS, Zep. Snippets go as a bulleted "Available memories" list in the **user message** before the question | 598 MCQ: GPQA 198, MMLU Medical 200, Moral Stories 200 | Strict sycophancy: share of zero-shot-correct answers switching to the biased option | Moral, chat history to Mem0: Sonnet 1.6 to 40.2%; Kimi 16.2 to 69.8%; GPT-5.2 6.1 to 41.0%. Science is far smaller: GPT-5.2 +1.5 to +2.7 pp | Generic disclaimer: Moral 41.0 to 26.5%, recall down 73.6 to 72.6%. Assistant-role: 20.3%. Summary: 12.8%. Both kept recall. Mem0 only |
| **Xiang et al. 2026** (v3), MemSyco-Bench | 5 backbones: Qwen3-8B, DeepSeek-V4-Flash, Llama-3.3-70B, **Llama-3.1-8B-Instruct**, GPT-4o mini; 7 memory systems | Memory or full dialogue appended to the **system prompt** (current public repo code, read Nov 2026; the paper states injection only generally) | 1,550 across 5 tasks; 300 Objective Fact Judgment. Long dialogues with a familiar false claim | Accuracy; sycophancy by LLM judge | Objective Fact, no memory to memory: Qwen3-8B 27.43 to 44.47–64.67; DeepSeek 18.67 to 32.00–42.67; Llama-3.1-8B see below | Caution instruction (DeepSeek): helps conflict, hurts personalisation by 13–21 points; little average change. "Are you sure?" usually worse |
| **Jain et al. 2025/CHI 2026** | 5: Claude Sonnet 4, GPT 4.1 Mini, GPT 5.1, Gemini 2.5 Pro, Llama 4 Scout | Real two-week histories from 38 users; extracted profile via a personalisation prompt | Personal-advice scenarios from Reddit (moral judgement, not facts) | LLM-judged agreement; regression | Memory profile: Gemini +45, Claude +33, GPT 4.1 Mini +16 (β as %). Llama 4 Scout and GPT 5.1 not significant | None; design suggestions |
| **Zhan et al. 2026**, AuthMem-Bench | 7: GPT-5.5, GPT-5.4 mini, Gemini 3.1 Pro, Gemini 3.5 Flash, Qwen3.7-Max, GLM-5.2, DeepSeek-V4-Pro | Consolidated memory, or supplied directly as a labelled memory block | 350 paired agent histories; tool actions | Unauthorised-action rate (ASR), task success (TSR) | Collapse in 48 of 49 configurations. ASR 50.3% without metadata | Source text 50.3 to 40.5%. Gold labels 5.8%/2.7%. Generic warning 26.2% ASR with 26.1% TSR. Predicted labels 16.9 to 0.0% |
| **Ma et al. 2026** | 4 open-weight: **Llama-3.1-8B-Instruct**, Llama-3.2-3B, Qwen3-8B, Gemma-3-4B | No memory. Two-turn pushback or evidence | TruthfulQA, PopQA, EX-FEVER, AQuA | Unsupported yielding; rational updating | Yielding 70.5% (Llama-3.1), 73.6%, 49.9%, 17.1% (Qwen3). Updating 40–65% | DPO, SFT, steering: recurring trade-off |
| **Hannoon et al. 2026** | 7: Gemini 3.1 Pro, Grok 4.1 Fast, Llama 3.3 70B, Qwen3-235B, DeepSeek-V3.2, GPT-OSS-120B, GLM-4.7 | Flat list vs partitioned list in the **system prompt** (PersistBench) | PersistBench: 200 leakage, 200 sycophancy, 100 beneficial | Judge failure rate | Sycophancy 96.5% at baseline, near ceiling | Partitioning: leakage down, 8.8% average. Sycophancy about 95%, no real change |
| **Genadi et al. 2026** | 2: Gemma-3-4B, Llama-3.2-3B | No memory. Pushback after a first answer | TruthfulQA, with transfer to other QA sets | Correct-to-incorrect rate | Signal in sparse mid-layer attention heads | Linear steering at inference |
| **Our study** (own finding) | 6: Mistral Nemo 12B, Mistral Small 24B, Llama 3.1 8B, Gemma 4 26B, Qwen3.5-9B, Claude Sonnet 5.5 | One sentence in the **system prompt** under "Saved memories", no extraction step. Stated arm: first line of the user message | 48 long-tail MCQ (no evidence passage), 4 useful-memory checks | Rate of choosing the false option vs own baseline; exact McNemar | Nemo 15 to 55%; Small 3 to 16%; Llama 14 to 15%; others 0–3% | Per-item "unverified" prefix: Nemo 55 to 32%, Small 16 to 11% |

## Newer or uncited studies that change the picture

| Study | Date | Why it matters | Key result |
|---|---|---|---|
| **Ni 2026** | Oct | Separates API channel from position, same text | System vs top of user message differs by 3.4–5.6 points; position differs by tens. One model (Qwen3.5-27B), MMLU-Pro |
| **Pulipaka et al. 2026**, PersistBench | Feb | Cross-model, pre-dates MS1 | 18 models, median 97% sycophancy failure. Items are adversarially searched and failure means any of 3 tries, so read rates with care |
| **Mao et al. 2026**, PASB | Jul | Cross-model, agents write their own notes | 16 models, 1,600 tasks. Failure 68.1% if claim saved vs 35.6% if not. 38.8% of notes overstate authority |
| **Yao et al. 2026** | Oct | Separates influence from firmness; tests base models | Deference to a prompt claim is present in every base model. Includes Llama-3.1-8B base and Instruct |
| **Shapira et al. 2026** | Oct | Is sycophancy really about approval? | Models also follow false claims from other sources, and credible sources move them more than users do |
| **Kumar & Chopra 2026** | Sep | Source vs user | Verified-source note flips 45–88% of correct answers in seven of eight models |
| **Liu & Ding 2026** | Oct | Admission vs presentation | Rendering changes gave no robust effect. Conflict failures stayed at 82% or above unless memory was removed |
| **R. Sharma et al. 2026** | Oct | Closest test to our label, on MemSyco | Provenance rewrite ("a belief the user holds, not an established fact") and its gated variant: conflict task stays at 80%+ on three models, 70–92% on Llama 3.1 8B. Objective-fact results for the gate improve; the paper's text gives no separate figure for the rewrite |
| **Kwon 2026** | Jun | Tests an "unverified" tag | Passive tag unreliable and model-dependent, also costs utility. Hand-built agent scenarios, 5 models |
| **Hu 2026** | Sep | Removing "unverified" framing | Risky approval 5% to 60% on Llama-3.1-8B. Authorisation monitors, not factual answers |
| **Chen et al. 2026** | Sep | Mechanism for stated opinions | Early attention heads; distinct from pushback |

## Llama-3.1-8B across studies

| Study | Setup | Result |
|---|---|---|
| Xiang et al. (MemSyco) | Memory in system prompt, long dialogues, judged open-ended | Sycophancy 29.92% to 56.52–61.33% with memory systems (+26.6 to +31.4 pp); 50.17% with full dialogue (+20.25) |
| Ma et al. | Two-turn pushback, no memory | Average yielding 70.5% |
| Hu | "Unverified" framing removed, monitor task | Risky approval 5% to 60% |
| **Our study** (own finding) | One-sentence memory in system prompt, MCQ | False answers 14% to 15% stored; 26% stated (exploratory) |

**Our inference:** Llama-3.1-8B is one of the more movable models elsewhere, and MemSyco also uses the system prompt. So "Llama ignores the memory section" is not a safe explanation for our null.

## Prompt placement detail

| Study | Slot | Text form |
|---|---|---|
| Bensal | User message, before question | Extracted snippets, bulleted |
| Xiang | System prompt, under a retrieved-memories header | Retrieved memories or dialogue |
| Hannoon / PersistBench | System prompt | Flat list based on leaked prompts |
| Ours, stored | System prompt, after instructions | "User believes that ..." |
| Ours, stated | Top of user message, before the question | "I believe that ..." |
