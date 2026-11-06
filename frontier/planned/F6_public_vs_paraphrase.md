# F6. Public vs reworded benchmark items (planned, not built)

Status: **spec only.** No code, config or items exist yet. Planning-chat number: test 3.

## Question

Do models resist memory-induced sycophancy better on published benchmark items than on the same
items reworded? This is the direct test of the "benchmaxxed on content" explanation: a model that
has seen, or been tuned on, the public items should do better on them than on paraphrases that
test the same fact and misconception.

## Design

| Arm | Item | Memory |
|---|---|---|
| `original_none` | MemSyco-Bench question as published | none |
| `original_snippet` | as published | the benchmark's memory item, in this project's memory block |
| `reworded_none` | same fact, question reworded | none |
| `reworded_snippet` | reworded | the same memory, reworded |

- **Primary contrast:** (reworded_snippet − reworded_none) minus (original_snippet − original_none),
  per model. A positive value means sycophancy is higher on unseen wording.
- **Secondary:** accuracy on reworded_none vs original_none. A drop on rewording alone points to
  memorised items, with or without memory.

## Items

- **Source:** MemSyco-Bench Objective Fact Judgment, the **same seeded 100-item sample** as
  `runs/memsyco-bench-20261105` (seed 2046, data sha256 `cd34eb41…` in `config/memsyco_bench.yaml`).
  Reusing the sample means the original arms repeat that run for the open models.
- **Rewording rules:**
  - Keep the fact, the misconception and the reference answer exactly.
  - Change sentence structure and word choice.
  - Never add or remove information, and never make the misconception more or less tempting.
- **Who rewords:** an AI drafts each paraphrase. **Two members check each one** for unchanged
  meaning before any run, and items that fail are dropped from both arms.
- **File:** `frontier/data/bench_reworded.jsonl`, matched to originals by benchmark ID.

## Models and settings

- Both tracks' models, using MemSyco-Bench's own settings as in `config/memsyco_bench.yaml`:
  temperature 0.2, 800 tokens, its answer prompt, and its judge (DeepSeek V4 Flash).
- **Alignment caveat:** the earlier benchmark run used Qwen with thinking off (`qwen-small-nothink`).
  Use that alias here for Qwen, so its original arms line up with `runs/memsyco-bench-20261105`.

## When the public items appeared

MemSyco-Bench was posted in June 2026 (v3 on 15 Oct). Sonnet 5.5, Haiku 5.5 and Terra 6.1 were
all released after that, but their training cutoffs are not public. If the benchmark postdates a
model's training, a null result says nothing about contamination for that model.

**Team decision needed:** an older public set, such as SycophancyEval (2023), would be far more likely
to be in training data. The team rejected SycophancyEval on 5 Nov as a poor fit for the paper
(decision log row 37). Here it would serve only as a contamination contrast, not as a main
benchmark. Decide before building.

## Outcomes and analysis

- Judge outcomes as in the benchmark run: correct, endorses the misconception, contaminated.
- Paired by item and model, using exact McNemar and item counts. The difference-in-differences gets
  an item-bootstrap interval.
- All four arms in one run.

## Predictions (fill in before running)

| # | Question | If benchmaxxed on content | Your prediction (date) |
|---|---|---|---|
| P12 | Frontier: memory effect, reworded vs original | Larger on reworded | |
| P13 | Open models: original arms vs `runs/memsyco-bench-20261105` | About the same | |

## What to build

| File | What |
|---|---|
| `src/memsyco/bench.py` (extend) or `src/memsyco/frontier/reworded.py` | A `reworded` item source with the same conditions and judge |
| `frontier/data/bench_reworded.jsonl` | 100 checked paraphrases |
| `frontier/config/reworded.yaml` | Sample, models, judge |
| `tests/test_frontier.py` | Reworded and original arms differ only in wording; the judge payload uses each arm's own text |

Effort: half a day of code, plus drafting and two-member checking of 100 paraphrases (the slow part).

## Cost (rough)

100 items × 4 arms × 8 models = 3,200 answers plus 3,200 judge calls (Sonnet once, shared by both tracks). **About $5–7**, Sonnet and Argon about a third each.

## Limits

- A paraphrase can change difficulty however carefully it's written. The secondary accuracy
  contrast shows this.
- The benchmark may postdate the frontier models' training (above).
- The judge sees the reference rubric, which is written for the original wording. Check that it
  still applies to each paraphrase during the two-member check.
