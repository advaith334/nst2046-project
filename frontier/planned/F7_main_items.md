# F7. Frontier models on the main study's items (planned, not built)

Status: **spec only.** Proposed on 5 Nov after F1–F4 were built. Not in the planning chat's
original list.

## Question

Do the new frontier models also sit at 0% false answers on the main study's 48 long-tail items, as
Claude Sonnet 5.5 did? This adds them as new rows to the main results table, the most direct link
between the frontier tests and the existing results.

## Why it matters for F1–F4

| F7 result | What it means for the frontier tests |
|---|---|
| Frontier models at or near 0% in every condition | Confirms the main-study null is a ceiling. F1 then shows what happens once that ceiling is removed |
| Some frontier models move on the long-tail items | The ceiling explanation is incomplete; frontier susceptibility exists even on knowledge items |

## Design

An exact copy of the main study: `config/main.yaml`'s items (48 long-tail items plus the 4
useful-memory checks), all six conditions, 2 reps, seed 2046, temperature 0.7, 2,000 tokens, top-5
token probabilities. Only the models change.

## Models

The `frontier` set from F1–F4 as it is: Claude Sonnet 5.5 with the main study's exact spec, and
Haiku, Terra and Argon, all with reasoning at the host's default. This lines up with both the main
study (same settings as its Sonnet row) and F1–F4 (same models and settings). Re-running Sonnet
also measures run-to-run noise against its 27 Oct row. About $3, more if Terra and Argon reason a lot.

## Outcomes and analysis

- The existing harness report: `summary.md` and `paired.csv`, the same tables as `runs/main-20261027`.
- The main study's item-bootstrap and Holm analysis (`report/analysis/stats_analysis.py`) can take
  these rows as extra models.
- Comparisons with the 27 Oct main run cross runs, so treat small gaps as noise (about 11% of
  Nemo's trials differ between runs on identical prompts).

## Predictions (fill in before running)

| # | Question | Expectation if it's a ceiling | Your prediction (date) |
|---|---|---|---|
| P14 | Frontier false-answer rate, stored vs none | At or near 0% in both | |
| P15 | Sonnet re-run vs its 27 Oct row | Same (0%) | |

## What to build

| File | What |
|---|---|
| `frontier/config/main_items.yaml` | A copy of `config/main.yaml` pointing at the frontier registry and its `frontier` set |
| `tests/test_frontier.py` | The config matches `config/main.yaml` in everything except models |

Effort: about 15 minutes. No new code: `memsyco run` already does this.

## Run

```bash
uv run memsyco run --config frontier/config/main_items.yaml --runs-dir frontier/runs --run-id frontier-main-items-<date> --max-cost 5
```

## Limits

- At ceiling, this run can only confirm the null; it can't measure susceptibility. That is F1's job.
- With default reasoning, some models may reason at length, which costs more and can run out of
  tokens. Check `finish_reason` in the smoke test.
