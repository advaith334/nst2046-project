# Reproducibility audit

Status: AI-run and AI-drafted (Claude Code, Opus 5.5) on 5 Nov 2026. Not repeated by a human.

- **Audited commit:** `f232e4f` (current `main`), in a fresh clone with no `.env` and no API key in the shell.
- **No paid API was called.** Only the free public OpenRouter catalogue and public GitHub pages were read.
- `feat/ms2-report` has moved on since (`c2d236f`, plus a new MemSyco-Bench run in progress). Those are not covered here.

## Verdict

**The analysis reproduces exactly from committed files. The study cannot be re-run exactly, and three README commands fail for a stranger.**

| Level | Result |
|---|---|
| Install and tests | Pass |
| Prompts | Pass: every logged request regenerates byte for byte |
| Scoring and tables from committed `raw_table.csv` | Pass, but only with a custom script |
| README section 4 numbers | Pass: all regenerate |
| Report commands as documented | **Fail in a clean clone: trial logs are not in git** |
| Exact model outputs | **Not reproducible** |
| Re-running the main config unchanged | **Would fail for Llama: its pinned host is gone** |

## What was tested

| Test | Command or method | Result |
|---|---|---|
| Install | `uv sync --locked` (uv 0.11.26, Python 3.12.2) | Pass; lockfile unchanged |
| Tests | `uv run pytest` | 25 passed |
| Validate all 5 configs | `memsyco validate` | Pass; 0 items verified in any file |
| Dry run, main config | `run --config config/main.yaml --dry-run` | 3,552 trials, 0 errors, $0, marked "DRY RUN" |
| Resume | Same command again | "3552 already done, running 0" |
| No key | Real run with no key | Clear error, nothing sent |
| Prompts doc | `render-prompts` vs `docs/prompts.md` | Identical |
| Logged requests vs regenerated | Dry run of all 5 configs, compared per trial with real `request` and `option_map` | **5,472 of 5,472 identical**, including the 4 rounds marked `dirty` |
| Re-parse from committed CSV | Option maps rebuilt from the seed, then parser run on `response_text` | 5,472 rows, 0 mismatches in letter, option or score |
| `summary.csv`, `paired.csv`, `screen.csv` from `raw_table.csv` | Library functions in a custom script | All match in all 5 runs |
| Full rebuild from local trial logs | `memsyco report`, `memsyco screen` | `raw_table.csv`, `summary.csv`, `paired.csv`, `screen.*` byte-identical to git |
| `summary.md` | Same | Main identical. The 4 earlier rounds differ only in number formatting and a missing paired section; the numbers agree |
| Rating sheet and agreement | `rating-sheet`, `agreement` on a temp copy of the logs | Work, but need `trials.jsonl` |
| `list-models` | Public catalogue | Works without a key |
| Secret scan | Regex over git history, tracked files and all trial logs | 0 matches |

## README section 4: every number checked

All recomputed from committed `runs/main-20261027/raw_table.csv`.

| Claim | Result |
|---|---|
| Rate table, all 36 cells | All match after rounding |
| "96 answers per cell" | True for five models. Qwen3.5-9B cells have 92–96 usable answers |
| 10 listed paired tests (flip counts and p-values) | All match |
| 42 comparisons in `paired.csv` | Match |
| Nemo raised on 25 of 48 items, lowered on 1 | Match |
| Mistral Small moved on 8 | Match |
| Bonferroni: Nemo results and Mistral Small's stored-belief result survive | Match. Threshold 0.05/42 = 0.0012. Six tests survive. Nemo's stated-vs-stored and unrelated-memory tests do not, so "the Nemo results" is loose |
| Llama other-wrong 74 of 592 | Match. Nemo also has 38, not mentioned |
| 15 Qwen3.5-9B unreadable | Match |
| Useful checks "100%, every model" | **Slightly overstated.** One Qwen3.5-9B answer was unreadable, so it is 7 of 7 readable, not 8 of 8 |
| "Cut Nemo's errors from 15% to 2%" | False-option rate, yes. **All wrong answers** fall from 27% to 3% (accuracy 73% → 97%) |
| 43 of 48 assert, 5 deny | Match data. The planning message of 27 Oct said 9 deny; that was wrong |
| 39 of 48 list a source | Match. Missing: `lt_letter_states`, `lt_celsius_fahrenheit`, `lt_sqrt_two`, `lt_smallest_perfect`, `lt_feet_in_mile`, `lt_hexagon_angles`, `lt_sunlight_time`, `lt_symbol_k`, `lt_symbol_sb` |

### README text that needs correcting

| Where | Says | Evidence shows |
|---|---|---|
| Status box | "3,552 trials, about $3.60 in total" | 3,552 is the main study. The whole project is 5,472 trials |
| Section 3, round table | Pilot $0.87 | Logged $0.851 |
| Section 3, round 2 | Llama and Nemo "about 30–40% wrong" | That is the false-option rate. All wrong answers are 40% (Llama) and 49% (Nemo) |
| Section 3, round 4 | Qwen3.5-397B "matched Claude at ceiling in every round" | Round 3: 2% → 4%, with 1 flip. Claude stayed at 0% |
| Sections 2 and `config/models.yaml` | "one model was routed to three hosts" | The 12 logged trials show at most two per model |
| Section 5 | Treats Gemma as simply unaffected | 7 Gemma responses first picked the false option, then corrected. See below |
| Whole file | No statement that code, items or text are AI-generated | Guidelines require disclosure |
| `config/longtail.yaml` comment | "24 obscure-fact items" | The file it loads now has 48 |
| `docs/prompts.md` | Examples use `pilot_canberra`, which has an evidence block | Main-study prompts have no evidence block. `render-prompts --case-id lt_sg_independence --config config/main.yaml` produces the right example |

## Extra checks the README does not contain

These came out of the audit and may be useful in the report. All are AI-computed and need a human check.

**The effect repeats on items not used to choose the design.** Nemo was selected on the 24 round-3 items, so the 24 new items are a fair hold-out.

| Model | 24 screened items | 24 new items |
|---|---|---|
| Mistral Nemo | 21% → 58% (19 toward, 1 away) | 8% → 52% (22 toward, 1 away, p ≈ 6e-6) |
| Mistral Small | 6% → 23% (8 toward, 0 away, p = 0.008) | 0% → 8% (4 toward, 0 away, p = 0.125) |

So Mistral Small's result leans on the first 24 items and is not significant on the new 24 alone.

**Round 3 is a natural repeat of round 4.** The same 24 items, same prompts, seed, hosts and option order were run twice. Nemo gave 19% → 60%, then 21% → 58%.

| Model | Same answer in both runs (same item, condition, rep) |
|---|---|
| Claude Sonnet 5.5 | 100% |
| Gemma 4 | 98% |
| Mistral Nemo | 94% |
| Qwen3.5-9B | 91% |
| Llama 3.1 8B | 87% |

This is the honest measure of reproducibility: effects repeat, individual letters do not.

**The scoring rule matters for Gemma.** Counting the first answer line instead of the last changes round 4 only for Gemma: stored 3/96 not 1/96, stated 6/96 not 2/96, labelled 1/96 not 0/96. Example: `lt_crust_second`, stated, rep 1 opens "Answer: A", "Your belief is correct", then ends on silicon. This could be a useful counterexample: a pull that shows and is then reasoned away.

## What a stranger could not reproduce

| # | Gap | Why | Severity |
|---|---|---|---|
| 1 | `memsyco report`, `screen` and `rating-sheet` crash on committed runs | `runs/*/trials.jsonl` is git-ignored; README says "Ask Advaith". Teammates cannot produce a rating sheet without it either | **High** |
| 2 | Logprobs, reasoning text, spend, full requests and option maps | Only in trial logs; `raw_table.csv` has none of them. README spend cannot be checked from git at all | **High** |
| 3 | Exact responses | Temperature 0.7, no `seed` sent, and hosts can change weights silently | Inherent, must be stated |
| 4 | Llama on the same host | Novita no longer serves this slug. With fallbacks off, `config/main.yaml` fails for Llama. The remaining hosts run fp8, bf16 or an undisclosed format | **High** |
| 5 | Model version | Slugs have no snapshot. `model_returned` equals the slug | Medium |
| 6 | Quantisation per trial | Not logged. Known only from catalogue reads, and "unknown" for Claude, Qwen-397B on Alibaba, and Gemma on Google | Medium |
| 7 | Claude at temperature 0.7 | Not supported; logs show 0.7 sent, but it was not applied. The evidence is the catalogue listing, not a direct test | Low, already disclosed |
| 8 | Round 3 as run | `config/longtail.yaml` now plans 1,152 trials on 48 items, not 576 on 24. The original 24 are listed only in that run's manifest | Medium |
| 9 | Code at rounds 1–3 | Runs were on uncommitted changes. Requests regenerate exactly, so the impact is low, but the code state itself is not recoverable | Low |
| 10 | Deleted smoke runs | `small-smoke`, `small-smoke2` removed on 27 Oct, about $0.01 of spend | Low |
| 11 | Hand scoring, item verification | Never done, so nothing to reproduce | **High for the mark** |
| 12 | Process evidence | Session log contains an API key and a Canvas token in plain text. Wispr note and Notion page are private | Medium |
| 13 | Python version | `>=3.11`, nothing pinned. Only 3.12.2 was tested | Low |
| 14 | Dates in manifests | `created_at` is overwritten on each resume | Low |

## Links

17 links in the README, 15 unique. No external links.

| Link type | Tested | Result |
|---|---|---|
| 9 contents anchors | Against the file's headings | All resolve |
| 6 relative paths | Locally and on github.com at `main` | All exist; all return 200 |

Other URLs a report might use:

| URL | Result |
|---|---|
| Repo home (public, no login) | 200 |
| `.../tree/f232e4f` | 200 |
| `.../pull/1` | 200 |
| `.../raw/.../runs/main-20261027/trials.jsonl` | **404**, as expected |
| `.../tree/feat/ms2-report` | **404**: branch not pushed |

## What must be fixed for a stable evidence link

In priority order. All need a person; none were done here.

1. **Rotate the OpenRouter key and Canvas token.** Both appear in plain text in the session log and the saved tool-result files. Do this before anything else is shared.
2. **Publish the trial logs.** Attach all five `trials.jsonl` files (29 MB) to a GitHub Release or Zenodo deposit, with the SHA-256 values below. The secret scan found nothing in them.
3. **Cite a tag or commit, not `main`.** Tag the final commit (for example `ms2-final`) and link to that. Zenodo would add a DOI.
4. **Add an AI disclosure to the README.** Code, items and text are AI-generated; git history does not show this.
5. **Make the two-member item check real.** Set `status: verified` only after it happens, and add sources for the 9 items without one.
6. **Fix the README wording** in the table above.
7. **Save the 5 Nov catalogue listing** beside the runs and state that Llama's host has gone.
8. **Restore the 24-item round 3 plan.** Add a `round3` list or a note in `config/longtail.yaml`.
9. **Regenerate `docs/prompts.md`** to show a main-study item.
10. **Add a redacted transcript excerpt pack** for the decisions in the decision log. Do not attach the raw file.
11. **Keep private material out of the public repo.** The repo is public, so `report/` becomes public if pushed. MS1 carries student IDs and the Wispr note has unrelated content.

### Trial log checksums (SHA-256)

Taken 5 Nov 2026 from the local files.

| Run | Size | SHA-256 |
|---|---|---|
| `pilot-20261027` | 3.2 MB | `45ded7cf13c4f1160cb1ac3f3d68acf14c0dcf7a0c9f4720a71b641e24f0c653` |
| `calibration-20261027` | 2.3 MB | `c3ffb2987ae18206b50efacb4c2cf967e26ed156c196e186b51a5275bd189dac` |
| `calsmall-20261027` | 3.0 MB | `9d676d39e0360d52e686bf2dd81bb7564222cd9469da619617a1dd2f774fd1a3` |
| `longtail-20261027` | 3.3 MB | `afb8e21900404ff10a288122d2fd25f482fce1497e1652d398adddbb875690d4` |
| `main-20261027` | 17.5 MB | `f6fb477d8fd375d1d06e68aee1030ae54f1c6533aa6296aed4add66fa88798c9` |

## Limits of this audit

- It was done by an AI assistant from the same tool family that built the harness, so it is not independent. A team member should repeat at least the install, tests, dry run and one table.
- Checksums came from the local machine. No one has compared them against another copy.
- It checks that numbers follow from the logs. It does not check that the item answer keys are right.
- The catalogue reads show what is listed today, not what served on 27 Oct, beyond what the session log recorded.
