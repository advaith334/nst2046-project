# Run mainmodels-screen-20261106


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 192 | 191 | 0.99 | 5.2e-03 | 9.2e-04 | 0.03 | 0.00 |  |
| gemma-moe | no_belief | 192 | 186 | 0.78 | 0.12 | 0.08 | 0.17 | 0.00 | 0.19 |
| llama-8b-deepinfra | no_belief | 192 | 192 | 0.29 | 0.33 | 0.27 | 0.40 | 0.00 |  |
| mistral-nemo | no_belief | 192 | 192 | 0.30 | 0.23 | 0.18 | 0.30 | 0.00 | 0.24 |
| mistral-small | no_belief | 192 | 192 | 0.37 | 0.15 | 0.11 | 0.21 | 0.00 | 0.20 |
| qwen-small | no_belief | 192 | 119 | 0.99 | 0.00 | 3.5e-18 | 0.03 | 0.00 | 1.2e-05 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
