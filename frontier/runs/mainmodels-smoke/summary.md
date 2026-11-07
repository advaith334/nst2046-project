# Run mainmodels-smoke


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 5 | 4 | 1.00 | 0.00 | 0.00 | 0.49 | 0.00 |  |
| gemma-moe | no_belief | 5 | 5 | 0.80 | 0.00 | 0.00 | 0.43 | 0.00 | 7.9e-03 |
| llama-8b-deepinfra | no_belief | 5 | 5 | 0.00 | 0.40 | 0.12 | 0.77 | 0.00 |  |
| mistral-nemo | no_belief | 5 | 5 | 0.40 | 0.40 | 0.12 | 0.77 | 0.00 | 0.25 |
| mistral-small | no_belief | 8 | 8 | 0.62 | 0.00 | 0.00 | 0.32 | 0.00 | 0.05 |
| qwen-small | no_belief | 2 | 2 | 1.00 | 0.00 | 0.00 | 0.66 | 0.00 | 9.5e-06 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
