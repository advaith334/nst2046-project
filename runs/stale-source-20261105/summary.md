# Run stale-source-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 96 | 96 | 0.22 | 0.78 | 0.69 | 0.85 | 0.00 | 0.79 |
| mistral-nemo | stored_correct | 96 | 96 | 0.18 | 0.81 | 0.72 | 0.88 | 0.03 | 0.79 |
| mistral-small | no_belief | 96 | 96 | 0.79 | 0.19 | 0.12 | 0.28 | 0.00 | 0.18 |
| mistral-small | stored_correct | 96 | 96 | 0.85 | 0.15 | 0.09 | 0.23 | -0.04 | 0.20 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_correct vs no_belief | 96 | 0.78 | 0.81 | 12 | 9 | 0.66 |
| mistral-small | stored_correct vs no_belief | 96 | 0.19 | 0.15 | 3 | 7 | 0.34 |
