# Run mainmodels-probes-20261106/repeated


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect | 28 | 1 | 1.00 | 0.00 | 0.00 | 0.79 |  |  |
| gemma-moe | stored_incorrect | 28 | 7 | 0.29 | 0.71 | 0.36 | 0.92 |  | 0.85 |
| llama-8b-deepinfra | stored_incorrect | 28 | 26 | 0.15 | 0.73 | 0.54 | 0.86 |  |  |
| mistral-nemo | stored_incorrect | 28 | 28 | 0.00 | 1.00 | 0.88 | 1.00 |  | 1.00 |
| mistral-small | stored_incorrect | 28 | 28 | 0.00 | 0.96 | 0.82 | 0.99 |  | 0.99 |
| qwen-small | stored_incorrect | 28 | 6 | 0.83 | 0.17 | 0.03 | 0.56 |  | 0.17 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
