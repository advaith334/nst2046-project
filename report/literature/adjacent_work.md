# Adjacent work: what the closest research did that we did not

Compiled 7 November 2026 for the NST2046 final report. Companion to `tutoring_and_psychosis.md`, `review.md` and `strengthening.md`; nothing here repeats them unless a new number changes the reading.

## Bottom line

- **Base versus instruct is the biggest change.** Yao et al. split deference (in the prompt, present in every base model) from capitulation (after an objection, added by post-training). Blank et al. study only capitulation, so they do not contradict our +50 and +48.
- **Our equal flip rates hide a large difference.** In log-odds from our own logs, Nemo Instruct was about three times firmer than Base and pushed about twice as far. Scaled by each model's spread the push is the same (1.33 and 1.34 SD). This is exploratory.
- **Our fix trade-off now has a mechanism partner.** Shapira et al. report that falls in sycophancy track falls in updating from reliable sources (r = 0.87 to 0.90).
- **The tutor-role claim is exposed.** Persona effects are often large and hard to predict, and the best design uses paraphrase controls. We ran none, and our comparison crosses runs.
- **The largest gap against the field is human judge validation.** The LLM-judged sycophancy benchmarks we read closely (Hong, Tang, Ping, Keough, Kasneci) all have some. We have none.

## Access key

| Mark | Meaning |
|---|---|
| FT | Full text read in HTML |
| FT (part) | HTML read but truncated, or only sections read |
| PDF (part) | PDF text extracted, relevant sections read |
| ABS | Abstract page only |
| PAGE | Web page read, not a paper |
| OURS | Calculated from our own logs for this note. Not committed, not reviewed |

Figures came through an automated reader. Key figures for De Marez, Yao, Blank and Li were re-checked against quoted sentences, and EoBench and Kim et al. against extracted PDF text. Check any other figure before it goes into the report.

## 1. Post-training and sycophancy

| Source | What they did | Finding | Bears on us | In the report? |
|---|---|---|---|---|
| **Blank et al. 2026**, FT | Two-turn MMLU pushback on 1,000 items all 49 checkpoints know, temperature 0. OLMo 3 and Tülu 3 pipelines; 15 same-family DPO students; 7 objectives | No-letter flips: SFT 12.5%, DPO 31.6%, Instruct 33.0%. Teacher log-ratio predicts student rate (R² = 0.76, ρ = 0.83). Swapping chosen and rejected labels gives 0.6%. Official Tülu DPO lowered flips, 11.4% to 7.0%. No sign of agreement preference in the data; removing over 70% of it changed nothing | Challenges any single story about post-training | **Yes** |
| **Yao et al. 2026**, FT (part), already cited | 13 checkpoints, 5 lineages, base to release. Log-odds gap and push at the answer slot, by firmness quintile | Deference in every base model; source ordering base-to-release agrees in 196 of 200 cases. Bare challenge: base abandons about 0.20 or less. Post-training multiplies the lead "about two to twenty" times. Firmer models flip less without being pushed less | Directly explains +50 and +48 | **Yes, more than now** |
| **De Marez et al. 2026**, FT | 56 open-weight models, 0.3B to 32B, 23 base-instruct pairs, 13 manipulations, two-option MC. Truth margin and manipulation sensitivity | Instruct gains +10.75 logits of margin (+1.10 SD). Sensitivity in SD is +0.15 [−0.19, +0.49]. Flips 23.3% to 16.3%. Instruct more robust in 17 of 23 pairs | Same split as ours, far wider base. Our pair flat where most pairs improve | **Yes** |
| **Du, Kümpel et al. 2026**, PDF (part) | EoBench: 19 belief forms, 18 models, base and instruct | Base as susceptible or more across most dimensions. Exception Qwen3-8B, instruct +18.1%. No Mistral models | Instruction tuning usually lowers context-following; our pair does not | **Yes** (see section 2) |
| **Yang & Yeung 2026**, FT | Bayesian-witness task: stated reliability r against prior p, gold rule "flip if r > p". LoRA DPO on Qwen2.5-7B Instruct | Base accuracy 0.64; instruction prompt 0.72; DPO 0.85; SFT on chosen 0.50. Base RESIST 0.16, UPDATE 0.67, REJECT 0.52 | Preference training can add sensitivity to reliability. Post-training is a tool, not only a cause | Maybe |
| **Shapira, Benade & Procaccia 2026**, ABS | Formal analysis of reward learning from preferences | Direction of drift depends on a covariance under the base policy. Agreement penalty proposed | Theory behind Blank's contrastive result | No |
| **Schrodi et al. 2025**, ABS | Subliminal transfer in distillation | Driven by a small set of divergence tokens; early layers; paraphrasing usually suppresses it | Weak bearing. Blank's effect is spread across data, and ours survives rewording | No |
| **König et al. 2026**, ABS | Steered teachers, distilled students, 100 jailbreak prompts | Transfer ratio τ up to 0.61 | No bearing on factual deference | No |

### What Blank implies for +50 against +48

- **It does not contradict us.** Blank measures flips after pushback. Our test is single-turn deference to a note. Yao shows these have different origins.
- **It tested no base checkpoint.** The earliest stage is SFT. Its statement that sycophancy starts in post-training is cited to earlier work, not tested.
- **Post-training is not one thing.** The same pipeline gives 31.6% or 0.6% depending on teacher order, and an official DPO lowered flips. One pair cannot stand for "instruction tuning" in either direction.
- **We cannot place Nemo.** Its post-training recipe is not known to us, so we cannot say which side of Blank's log-ratio it falls on.
- **Our next-test sentence needs a prediction.** Given Yao, deference to stored beliefs should not need transfer to exist. Transfer could still amplify it.
- **The MS1 mechanism stays unsupported for deference, and untested for pushback.** The report should say both.

### Diagnostic from our own logs (OURS)

The local pair logged probabilities on every trial, top-10, with no clipping needed. For each item, L = log p(false) − log p(key), averaged over repetitions. **Gap** is −L with no belief. **Push** is L with the note minus L with no belief. Intervals are item bootstrap, 10,000 resamples, percentile. This is Yao's measure and De Marez's normalisation.

| Nemo, 48 items | Base | Instruct, plain | Instruct, chat template |
|---|---|---|---|
| False-option rise, points | +50 | +48 | +48 |
| Median gap, nats | 1.56 | 5.08 | 5.24 |
| SD of no-belief log-odds | 2.24 | 4.27 | not computed |
| Push, false note | +2.96 [+2.49, +3.43] | +5.73 [+4.60, +6.82] | +5.87 [+4.59, +7.10] |
| Push, false note with label | +2.14 [+1.74, +2.54] | +3.70 [+2.82, +4.57] | +3.18 [+2.22, +4.17] |
| Push, true note | −1.91 [−2.38, −1.44] | −2.76 [−3.73, −1.81] | −3.57 [−4.58, −2.60] |
| Push, unrelated note | +0.16 [−0.01, +0.32] | +0.76 [+0.45, +1.08] | +0.50 [+0.23, +0.79] |
| Push in SDs of own spread | 1.33 | 1.34 | not computed |

Base minus instruct on false-note push is −2.76 [−3.57, −1.97].

| Items the model favoured correctly, by firmness | Loose | Middle | Firm |
|---|---|---|---|
| Base: push (share of items ending on the false option) | 3.18 (100%) | 3.92 (92%) | 3.34 (25%) |
| Instruct: push (share ending on the false option) | 5.70 (92%) | 6.62 (62%) | 7.20 (43%) |

**What this shows**

- Equal flip rates come from a cancellation. Instruct is firmer and pushed harder by about the same factor.
- That is what a stretch of the log-odds scale would look like, so it does not show that post-training strengthens deference in particular.
- Push does not shrink as firmness grows. A firm answer survives because it has headroom, as Yao found. This fits Nemo's flips from confident answers and sits badly with the reading that it uses a note only when unsure.

**Limits**

- Exploratory, post hoc, one quantised pair, first answer token only.
- Option probabilities match the written letter on 86% (base) and 91% (instruct) of trials. Sampling at temperature 0.7 explains part of this, but Yao reports at least 98.5%.
- We could not confirm whether `llama-server` reports probabilities before or after temperature. It would affect both models alike, so the ratios stand and the absolute nats may not.
- Gemma, Qwen and many Small trials cannot be used. Top-5 logging leaves unlisted options, so their gaps pile up at our clip of 9.2 nats. The knowledge-versus-resistance question stays open for them.

## 2. Why context overrides what a model knows

| Source | What they did | Finding | Bears on us | In the report? |
|---|---|---|---|---|
| **Shapira, Cheng & Orgad 2026**, FT (part), already cited | Mitigations and weight pruning on four frontier and two open models | Falls in sycophancy track falls in source-based updating, r = 0.87 (frontier), 0.90 (open). About a third of 1,000 weights chosen against reliable-source updating are also in the sycophancy set | Supports Part 2: a fix that sorts true from false has no obvious handle in the weights | **Yes** |
| **Du, Kümpel et al. 2026**, PDF (part) | 19 belief forms on four dimensions, 16 models after filtering, permutation test with BH | Most persuasive include imperative, formal, authority. Least include counterfactual, belief reports, weak stance. "My brother believes..." is the belief-report form | Fits our +19 from dropping "User believes that". Closest wording work. Facts only, no true arm, no evidence or frame | **Yes** |
| **Wu, Wu & Zou 2024**, FT | ClashEval: about 1,290 questions, 6 domains, 6 models, conflicting retrieved passages | GPT-4o took context over a correct prior 60.8% of the time. Context preference falls with prior token probability, slopes −0.1 to −0.45. Calibrated token-probability rule: accuracy 0.615 to 0.754, context bias 0.304 to 0.107, prior bias 0.021 to 0.085 | The evidence base for a confidence gate (section 3). Also measures both failure directions, as we do | **Yes** |
| **Du et al. 2024**, FT (part) | Persuasion and susceptibility scores on Pythia models | Real entities less susceptible than fake on 73 of 122 open queries. Susceptibility against training co-occurrence, ρ = −0.23 | Fits long-tail items moving most. Older models | Maybe |
| **Li, Wang et al. 2025**, FT | 7 models. Logit-lens, activation patching, opinion against expertise, first against third person | Opinion-only agreement mean 63.7%. Expertise moved it at most 4.4 points. First person 13.6% higher on average. Patching Plain into Opinion-only cut Llama 36%. Divergence late in the network | Late-layer finding sits awkwardly with Chen's early heads. Our stored note beat stated belief (Nemo 55% against 48%), the reverse of first over third, though position also differs | Maybe, one clause |
| **Li, Chen & Tong 2025**, FT (part) | Attention-head steering, 11 datasets, 6 models | Influential heads serve memory and context at once. About half of top memory heads act as context heads under coherent conflict | Warns against any clean "which heads" story like MS1's | No, too technical |
| **Neeman et al. 2022**, ABS | Train QA models to give a contextual and a parametric answer | Better robustness to conflict on Natural Questions | Source of the "note says, I know" idea in section 3 | Optional |
| **Panickssery et al. 2024**, FT (part) | Contrastive activation steering, Llama 2 | Sycophantic-answer probability at layer 13, 7B: 0.54, 0.69, 0.62 at −1, 0, +1 | Steering works weakly and not monotonically in MC | No |
| **Vennemeyer et al. 2025**, ABS | Separates agreement, praise and genuine agreement in activation space | Independently steerable | Sycophancy is not one quantity | No |

**Simple diagnostic.** The push and gap table above is the one to run. It needs only logged probabilities, costs nothing, and separates "moved less" from "knew more".

## 3. Memory systems

| Source | What they did | Finding | Bears on us | In the report? |
|---|---|---|---|---|
| **Louck 2026**, FT | Authority bound to channel of origin, propagated through derivations. Two trusted principals needed to elevate | Attack success 84% to 0%, laundering 68% to 0%, utility 100% on a pooled benchmark. States that answer-biasing stays high under all defences | Provenance gating protects actions and leaves answers. That is our outcome. Author's own benchmark | **Yes, one clause** |
| **Shen et al. 2026**, FT (part) | 5 memory systems, 9 policies, 9 models, 6 defences on revoked facts | Unsafe action 43.1%. Prompt hardening 37.2%, output filter 18.1%, retrieval filter 0.0%. Benign utility not measured | Removing a record works where instructing the model does not. Fits our rule and label results. Actions, not answers | Maybe |
| **Singh 2026**, FT | Bayesian belief memory, reliability = min(provenance, content) | Attack success 100% to 0% in a simulation built by the author. A genuine low-tier correction falls from 100% to about 54%. Authoritative-sounding poison got reliability 0.96. LLM-judge and token-F1 scores differ by 27.5 points on identical output | Provenance has a benefit cost too, which backs our two-sided test. Not transferable as numbers | Maybe |
| **Zhang et al. 2026**, FT | MemGate: learned query-conditioned gate | Sycophancy failure 33.5% to 31.5% against 25.0% memory-free (OpenClaw, GPT-4o-mini). Beneficial-subset failure 14.3% to 6.7% | A retrieval gate that keeps utility barely dents sycophancy. No memory-free benefit arm | Maybe |
| **Dash et al. 2026**, FT | MPBench: 3,240 attacks, 2,997 benign, two agent systems | Attack success 34.25% and 66.67%. System injecting memory at session start ran higher. Input defences catch 23.00% to 67.67% | Supports fixing the write path. We test use only | No |
| **Chen, Xie et al. 2026**, ABS | MemSecBench: 310 cases, 24 configurations | Persisted 84.2%, end-to-end 50.3%, repaired 56.1% of poisoned cases | Adversarial, not a user's honest error | No |

**Scope warning.** Poisoning work has an attacker, a tool action and a harm-only metric. Our note is honest, the outcome is an answer, and truth is unknown to the system. Do not read these numbers across.

### Fixes with evidence that we did not test

| Idea | Evidence | Cost to test | Our view |
|---|---|---|---|
| **Confidence gate:** answer twice, keep the no-memory answer if confidence is high | ClashEval; replay below | Free on logs | Best candidate |
| **Withhold on conflict at retrieval** | Shen: 43.1% to 0.0% | Needs conflict detection, which is the hard part here | Not testable cheaply |
| **Provenance cap with an explicit reliability** | Singh, Yang & Yeung | Prompt-level test is cheap | Requires a reliability estimate for the user, which is our Justice problem |
| **Stated reliability in the note** ("this user is right about 60% of the time") | Yang & Yeung: instruction prompt alone 0.72, base 0.64 | Under US$0.10 on Nemo and Small | Interesting, untested on memory |
| **Report both** ("the note says X, I would say Y") | Neeman, by training | Prompt-level test is cheap | Close to what a tutor needs |

### Replay of a confidence gate on our logs (OURS)

Rule: if the highest no-belief probability is at least τ, keep the no-belief answer; otherwise use the answer given with the note. Selectivity is our Part 2 measure, so a random mix scores 0.

| Nemo | τ | Harm removed | Benefit kept | Selectivity |
|---|---|---|---|---|
| Main, 48 items | 0.7 | 64% | 61% | +0.25 [+0.01, +0.51] |
| Main, 48 items | 0.9 | 54% | 74% | +0.28 [+0.06, +0.50] |
| MMLU, 120 items | 0.7 | 29% | 88% | +0.17 [+0.06, +0.28] |
| MMLU, 120 items | 0.9 | 16% | 92% | +0.07 [−0.02, +0.17] |

- The report says no fix has an interval above zero for Nemo. That remains true of everything we ran live. A replay is weaker evidence, and τ was not fixed in advance.
- It differs from our failed answer-first test, which ran in one thread. Here the two calls are independent, so no draft can be abandoned.
- It can only help where the model knows the answer. That matches Part 5 and is a limit, since the student who most needs protecting is on the items a weak model does not know.
- It needs a second call and token probabilities, which Claude does not expose on our logged runs.

## 4. Evaluation method

| Practice | Best example opened | Where we stand |
|---|---|---|
| **Human judge validation** | Ping: 480 stratified trials, two raters including a physician, κ = 0.866, sample set by power analysis on κ. Tang: 100 blind turns, κ = 0.76. Hong: 100 per scenario, κ 0.63 to 0.92 | **Missing.** Our κ of 0.91 is AI against AI |
| **Agreement varies by task** | Hong: false presupposition 0.63 against debate 0.92. Keough: human panel mean pairwise κ 0.58 on verdicts, 0.21 on scores; judge missed 3 of 9 sycophantic replies. Kasneci: humans overturned 10 of 98 usable agreed cases; one judge flagged no GPT-5.2 replies | Report κ per measure. "Told wrong" may be the weak one |
| **Judge independent of tested models** | Tang and Ping both flag this as a limit | Haiku is judge and tutor. Already disclosed |
| **Item-level inference** | Ping: logistic GLMM with random intercepts for question and model; question SD 2.80 to 4.21 against model SD 1.16 to 1.73. De Marez: hierarchical bootstrap over questions and baits | **Ahead on tests**, behind on reporting. We do not state how much items vary against models |
| **Repetitions** | Ping: 10 per condition. Blank: 1,000 items at temperature 0 | Two per cell. Items matter more than repetitions, so this is acceptable |
| **Multi-turn** | Tang: up to 25 adaptive turns; every model's collapse rises from turn 5 to 25; fixed script 28% against adaptive 50% at turn 5 (DeepSeek). Ping: multi-turn 6.99% against single-turn 2.53% | **Behind.** Our turn-2 tests are scripted, and our turn-2 result may understate pressure |
| **Format** | Kim et al.: all ten models easier to persuade on clear MC than on open diagnosis. Kim & Khashabi: follow-up rebuttal beat side-by-side for most models (Llama-3.3 86.0% against 56.5%) | Supports our MC-to-free-text gap, and warns that MC headlines overstate |
| **Pre-registration** | No LLM sycophancy benchmark we opened states one | **Ahead.** Keep this claim to "among those we read" |
| **Null and equivalence** | TOST needs the 90% interval inside chosen bounds (Lakens et al. 2018, via TOSTER) | The +2 [−10, +15] cannot show equality at any bound tighter than about 15 points. The report already avoids claiming it |
| **Generalising over items** | Yarkoni 2022, ABS: stimuli are rarely modelled though we mean to generalise over them | Part 3 random draw is the answer. Parts 1 and 2 stay exposed |
| **Reporting standard** | REFORMS (Kapoor et al. 2024), PAGE: 32 items, 8 sections | Optional mention only |

**The standard we may be missing:** a stratified, blind human check of about 100 replies per main measure, with κ by measure and a judge outside the tested set. The sheets are ready. It costs people's time and no credit.

## 5. Role and persona prompts

| Source | What they did | Finding | Bears on us | In the report? |
|---|---|---|---|---|
| **Luz de Araujo & Roth 2024**, FT | 162 personas, 7 models, about 30 paraphrases of "helpful assistant" as controls | Significant persona effects for every model and dataset. Gap up to 38.56 points; GPT-4 smallest at 4.58 averaged. Controls cluster near baseline | Gives the control we lack. Includes Mistral-7B-Instruct | **Yes** |
| **Zheng et al. 2024**, ABS | 162 roles, 4 families, 2,410 factual questions | No improvement over no persona. Authors read the effects as largely random; automatic best-persona selection no better than chance | Fits our tutor frame not improving accuracy (no-memory false 18% to 26%) | **Yes, one clause** |
| **Hong et al. 2025**, FT | SYCON: 500 prompts, 5 turns, 17 models. "Andrew" third-person prompt | Turn of flip up to 63.8% better; Qwen2.5-7B 1.10 to 4.02. No clear trend on false presupposition | Distance from the user helps in debate, not obviously on false facts | Maybe |
| **Kasneci & Kasneci 2026**, FT (part) | EduFrameTrap: 360 trap families, tutors under pressure, 4,529 replies | Adjudicated sycophancy about 14.1%, varying heavily by judge. No baseline-against-instruction result reported | No controlled evidence on tutor roles | Already noted |

### Does prior work explain the tutor role? (OURS plus literature)

**No direct test found.** No source we opened shows a teacher or tutor role reducing agreement with a false belief. Three partial accounts fit.

- **It turns the note down.** In multiple choice the tutor frame cut Nemo's push on both kinds of note by about the same factor. This fits our "volume control" reading and shows no sorting of true from false.
- **Personas are unstable.** A single role sentence may move results for reasons unrelated to its meaning. We cannot rule this out without paraphrases.
- **Format does part of the work.** Kim et al. and our own +63 against +15 both point this way, and the free-text harm was small before the role was added.

| Nemo, MC, 60 items, push in log-odds | Default | Frame | Ratio |
|---|---|---|---|
| Tutor frame: false note | +5.45 [+4.79, +6.08] | +0.78 [+0.29, +1.28] | 0.14 |
| Tutor frame: true note | −5.17 [−5.86, −4.47] | −1.00 [−1.45, −0.57] | 0.19 |
| Patient frame: false note | +5.28 [+4.41, +6.19] | +2.42 [+1.68, +3.20] | 0.46 |
| Patient frame: true note | −4.23 [−5.01, −3.46] | −2.52 [−3.31, −1.74] | 0.60 |

The median gap barely moved under the tutor frame (0.81 to 0.53). So in MC the frame reduces the note's weight and adds no firmness.

## 6. Conceptual work

Only two sources earn a place. The strongest existing support stays in the report as it stands (FRE 803(3), Kelly, Nguyen).

| Source | Point | Use | In the report? |
|---|---|---|---|
| **Suzgun et al. 2024**, FT (part), preprint of a *Nature Machine Intelligence* paper | Across 15 models including Mistral 7B: confirming a false belief, third person 80.7%, first person 54.4%; true beliefs 92.1 to 95.6% | Models can often represent a false belief as a belief. So Nemo's error is one of use, which sharpens the category-error argument | **Yes** |
| **Karnatak et al. 2026**, FT (part), AIES 2026 | Misinformed deference: reliability cues that make unwarranted reliance look justified. Epistemic access is more than having citations | A memory heading is such a cue, for the model and for the deployer | Optional |
| **Basmov et al. 2024**, ABS | Models under- or over-predict entailment under non-factives, often ignoring the embedding | Supports "believes that" being weakly read. Adds little beyond Du, Kümpel | No |

## The 8 most valuable additions

Ranked. Numbers marked OURS need rerunning by the team first.

1. **Base versus instruct.** "Yao et al. (2026) separate deference to a claim in the prompt, present in every base model, from capitulation after an objection, which post-training adds; Blank et al. (2026) trace the second to preference optimisation, so our result on deference neither supports nor contradicts them." (Yao et al., 2026; Blank et al., 2026)
2. **Log-odds (OURS).** "In log-odds Instruct held answers about three times as firmly as Base and was pushed about twice as far (+5.73 against +2.96), so equal flip rates are a cancellation, and scaled by each model's spread the push is the same (1.33 and 1.34 SD), as De Marez et al. (2026) find across 23 pairs (exploratory)." (De Marez et al., 2026)
3. **Judges.** "Comparable studies validate LLM judges against people, with κ from 0.63 to 0.92 by task (Hong et al., 2025; Ping et al., 2026; Tang et al., 2026); ours are checked only against each other, so Parts 4 and 5 carry that risk."
4. **Role caveat.** "Persona effects can reach 38.56 points and are hard to predict (Luz de Araujo & Roth, 2024; Zheng et al., 2024), so without paraphrase controls our one-sentence role effect may be prompt sensitivity."
5. **Trade-off.** "Shapira et al. (2026) find falls in sycophancy track falls in updating from reliable sources (r = 0.87 to 0.90), which is what our fixes show from the outside: most lower the weight on the record and do not sort it." (Shapira et al., 2026)
6. **Wording.** "Across 16 models Du et al. (2026) rank belief reports among the least persuasive ways to state a claim, which fits the 19-point rise when we dropped 'User believes that'; their test has no true arm, evidence or frame, so our narrower gap stands." (Du, Kümpel et al., 2026)
7. **Fix with evidence.** "ClashEval's token-probability rule raised GPT-4o from 0.615 to 0.754 (Wu et al., 2024), and a replay of a similar gate on our logs gave selectivity +0.07 to +0.17 on MMLU, weak and only where the model knows the answer (exploratory)." (Wu et al., 2024)
8. **Category error.** "Models confirm a false third-person belief far more often than a false first-person one (80.7% against 54.4%; Suzgun et al., 2024), so they can often hold a belief as a belief, which places Nemo's failure in its use." (Suzgun et al., 2024)

## Up to 3 cheap experiments or analyses

| # | What | Why | Estimated cost |
|---|---|---|---|
| A | Rerun the push and gap table as committed code, with the frame and label rows | Backs additions 2 and 7. All data are logged | **US$0**, about an hour |
| B | "Are you sure?" and a named alternative on the local Nemo pair: 48 items, no belief and stored false, 2 repetitions | Direct test of Yao's split on our pair. Prediction: base holds, instruct abandons, and a stored note interacts | **US$0**. About 770 calls per pressure type at 1.7 s, so 25 to 50 minutes. GGUFs are on disk. Base may stop giving a letter at turn 2, as OLMo-2 base did for Yao |
| C | Three tutor and three assistant paraphrases, 60 items, none, false and true notes, a note that does not repeat the question, Nemo and Small, MC with top-10 probabilities | Tests addition 4, the unresolved note-repeats-question caveat, and gives the gate a prospective test with τ = 0.9 fixed | **About US$0.22** on past per-trial cost (4,320 trials). Cap at US$0.30. Free text would cost about US$0.58 or more, so keep to MC |

The human check in section 4 comes before all three and uses no credit. A plus the human check fit before the 8 November deadline. B fits if the local server starts cleanly.

## What undercuts the report

- **"A base model showed the rise at full size"** holds on flips only. In log-odds Base moved about half as far as Instruct.
- **Our flat pair may be unusual.** De Marez find instruct more robust in 17 of 23 pairs, and EoBench finds base as or more susceptible. Avoid generalising from Nemo.
- **"In Part 5 one role sentence separated +15 from 0"** crosses runs, has no paraphrase control, and meets a literature in which personas move results erratically. Soften it.
- **"We found no study that keeps one belief sentence fixed..."** still holds narrowly, but EoBench is close on wording and must be cited beside it.
- **MC headlines may overstate harm.** Kim et al. and our own free-text results agree. The report says this, and the opening paragraph should not lean on +41 and +55 alone.
- **Mechanism sources conflict.** Chen places stated opinions in early heads, Li in late layers, and Li, Chen & Tong doubt clean head categories. Avoid any layer-level claim.
- **Our first-person result runs the other way.** Li and Suzgun suggest third person is handled differently, yet Nemo followed the stored third-person note at least as much as a stated belief (55% against 48%). Treat position and person as confounded here.

## Refused or unread

| Source | Status |
|---|---|
| Epistemic Deference to AI, PhilArchive | 403, left |
| Chatbot Epistemology, *Social Epistemology*, Taylor & Francis | 403, left |
| Lakens (2017), PMC | reCAPTCHA page, left. Lakens et al. (2018) cited only through the TOSTER vignette |
| Yarkoni, PubMed | Cookie wall. Cambridge abstract page used |
| Suzgun et al., *Nature Machine Intelligence* | Published version not opened; preprint used, so numbers may differ |
| Ying et al. (2026), cited by Blank | Not found |
| Jin et al. (2024), memory and context heads | Not found; known only through Li, Chen & Tong |
| Jain et al. and PersistBench judge κ | Search snippets only, not cited here |
| Wharton persona report; MINJA; SMSR; LoCoMo audit (vendor) | Search snippets only, not cited |
| ClashEval | Text says 1,294 questions, Table 1 sums to 1,278 |
| Blank et al. | Text gives 35% and table 38.1% for the same pair; "seven" against six objectives. Tables used |

## References

Basmov, V., Goldberg, Y., & Tsarfaty, R. (2024). *Simple linguistic inferences of large language models (LLMs): Blind spots and blinds*. arXiv:2305.14785. ABS

Blank, C., Ying, Z., Potts, C., Hase, P., & Huang, J. (2026). *Sycophantic agreement transfers with neutral data via contrastive preference optimization*. arXiv:2608.31079. FT

Chen, X., Xie, X., Fu, W., Zhou, J., Yu, S., & Xuan, Q. (2026). *MemSecBench: Tracking agent memory poisoning from persistence to consequence and repair*. arXiv:2607.27080. ABS

Dash, P., Ge, T., Jain, A., Shah, T., & Shang, Z. (2026). *From untrusted input to trusted memory: A systematic study of memory poisoning attacks in LLM agents*. arXiv:2606.04329. FT

De Marez, V., De Bruyne, L., & Daelemans, W. (2026). *Decomposing factual sycophancy in language models: How size and instruction tuning shape robustness*. arXiv:2606.06306. FT

Du, K., Kümpel, C., Wastl, M., & Warstadt, A. (2026). It's not what you say, it's how you say it: Evaluating LLM responses to expressions of belief. In *Proceedings of ACL 2026*. https://aclanthology.org/2026.acl-long.142.pdf. PDF (part); venue from the URL; author list read from the first page

Du, K., Snæbjarnarson, V., Stoehr, N., White, J. C., Schein, A., & Cotterell, R. (2024). *Context versus prior knowledge in language models*. arXiv:2404.04633. FT (part)

Hong, J., Byun, G., Kim, S., Shu, K., & Choi, J. D. (2025). *Measuring sycophancy of language models in multi-turn dialogues*. arXiv:2505.23840. FT

Kapoor, S., et al. (2024). REFORMS: Consensus-based recommendations for machine-learning-based science. *Science Advances*. https://doi.org/10.1126/sciadv.adk3452. PAGE, https://reforms.cs.princeton.edu/

Karnatak, N., Van Kleek, M., & Shadbolt, N. (2026). *Epistemic trustworthiness in generative AI: A normative framework for warranted reliance in high-stakes workflows*. arXiv:2608.05602. FT (part)

Kasneci, E., & Kasneci, G. (2026). *Sycophancy is an educational safety risk*. arXiv:2605.14604. FT (part)

Keough, P. (2026). *The granularity gap: A multi-dimensional cross-generational audit of sycophancy in Gemini models*. arXiv:2606.05183. FT (part)

Kim, S. W., & Khashabi, D. (2025). *Challenging the evaluator: LLM sycophancy under user rebuttal*. arXiv:2509.16533. FT (part)

Kim, T. M., Luo, L., Kim, S. E., Manrai, A. K., Topol, E., & Rajpurkar, P. (2026). The doctor will agree with you now: Sycophancy of large language models in multi-turn medical conversations. HeaLing workshop. https://aclanthology.org/2026.healing-1.2.pdf. PDF (part)

König, U., Kazmi, H., Li, R., & Chaudhary, M. (2026). *Quantifying subliminal behavioral transfer ratios in language model distillation*. arXiv:2606.11270. ABS

Lakens, D., Scheel, A. M., & Isager, P. M. (2018). Equivalence testing for psychological research: A tutorial. *Advances in Methods and Practices in Psychological Science, 1*(2), 259–269. https://doi.org/10.1177/2515245918770963. Via the TOSTER vignette, https://cran.r-project.org/web/packages/TOSTER/vignettes/IntroductionToTOSTER.html

Li, G., Chen, Y., & Tong, H. (2025). *Taming knowledge conflicts in language models*. arXiv:2503.10996. FT (part)

Li, J., Wang, K., Yang, S., Zhang, Z., & Wang, D. (2025). *When truth is overridden: Uncovering the internal origins of sycophancy in large language models*. arXiv:2508.02087. FT

Louck, Y. (2026). *Securing LLM-agent long-term memory against poisoning: Non-malleable, origin-bound authority with machine-checked guarantees*. arXiv:2606.24322. FT

Luz de Araujo, P. H., & Roth, B. (2024). *Helpful assistant or fruitful facilitator? Investigating how personas affect language model behavior*. arXiv:2407.02099. FT

Neeman, E., Aharoni, R., Honovich, O., Choshen, L., Szpektor, I., & Abend, O. (2022). *DisentQA: Disentangling parametric and contextual knowledge with counterfactual question answering*. arXiv:2211.05655. ABS

Panickssery, N., Gabrieli, N., Schulz, J., Tong, M., Hubinger, E., & Turner, A. M. (2024). *Steering Llama 2 via contrastive activation addition*. arXiv:2312.06681. FT (part)

Ping, K., Çarık, B., Wohn, C., Ding, X., Wang, T., & Rho, E. (2026). *Why LLMs give in: Conversational factors and reasoning behind medical sycophancy*. arXiv:2608.01017. FT (part)

Schrodi, S., Kempf, E., Barez, F., & Brox, T. (2025). *Towards understanding subliminal learning: When and how hidden biases transfer*. arXiv:2509.23886. ABS

Shapira, I., Benade, G., & Procaccia, A. D. (2026). *How RLHF amplifies sycophancy*. arXiv:2602.01002. ABS

Shapira, I., Cheng, M., & Orgad, H. (2026). *Is sycophancy a form of in-context updating?* arXiv:2610.28325. FT (part)

Shen, Y. T., Toyoda, K., & Leung, A. (2026). *Revoked but still authoritative: An empirical study of revocation enforcement in agent-memory systems*. arXiv:2609.08258. FT (part)

Singh, P. (2026). *When does belief-based agent memory help? Reliability-conditional updating and provenance-capped poisoning defense*. arXiv:2606.22030. FT

Suzgun, M., Gur, T., Bianchi, F., Ho, D. E., Icard, T., Jurafsky, D., & Zou, J. (2024). *Belief in the machine: Investigating epistemological blind spots of language models*. arXiv:2410.21195. FT (part)

Tang, L., Wei, K., Jiang, T., & Huang, R. (2026). *SPINE: Measuring LLM sycophancy under sustained multi-turn pressure*. arXiv:2609.09090. FT (part)

Vennemeyer, D., Duong, P. A., Zhan, T., & Jiang, T. (2025). *Sycophancy is not one thing: Causal separation of sycophantic behaviors in LLMs*. arXiv:2509.21305. ABS

Wu, K., Wu, E., & Zou, J. (2024). *ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence*. arXiv:2404.10198. FT

Yang, S., & Yeung, Y.-H. (2026). *Resist, update, reject: Preference optimization installs a prior-dependent reliability switch*. arXiv:2609.22359. FT

Yao, J., Parihar, S., Bui, N. T., Savova, G. K., & Wang, L. (2026). *Locating sycophancy across training stages in open language models*. arXiv:2610.37788. FT (part)

Yarkoni, T. (2022). The generalizability crisis. *Behavioral and Brain Sciences, 45*, e1. https://doi.org/10.1017/S0140525X20001685. ABS

Zhang, J., Chen, K., Ma, J., Hu, Y., He, L., Zhang, Y., Liu, J., Yang, X., Zhang, T., & Jia, R. (2026). *Beyond similarity: Trustworthy memory search for personal AI agents*. arXiv:2606.06054. FT

Zheng, M., Pei, J., Logeswaran, L., Lee, M., & Jurgens, D. (2024). *When "a helpful assistant" is not really helpful: Personas in system prompts do not improve performances of large language models*. arXiv:2311.10054. ABS
