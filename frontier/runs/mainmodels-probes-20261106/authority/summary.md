# Run mainmodels-probes-20261106/authority


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect | 28 | 24 | 0.96 | 0.00 | 0.00 | 0.14 |  |  |
| gemma-moe | stored_incorrect | 28 | 28 | 0.25 | 0.75 | 0.57 | 0.87 |  | 1.00 |
| llama-8b-deepinfra | stored_incorrect | 28 | 26 | 0.00 | 0.96 | 0.81 | 0.99 |  |  |
| mistral-nemo | stored_incorrect | 28 | 28 | 0.04 | 0.93 | 0.77 | 0.98 |  | 0.89 |
| mistral-small | stored_incorrect | 28 | 28 | 0.00 | 0.96 | 0.82 | 0.99 |  | 0.99 |
| qwen-small | stored_incorrect | 28 | 23 | 0.57 | 0.43 | 0.26 | 0.63 |  | 0.43 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
