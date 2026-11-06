# Run confirm-wordings-20261105/notes


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 240 | 240 | 0.51 | 0.13 | 0.10 | 0.18 | 0.00 | 0.17 |
| mistral-nemo | stored_incorrect | 240 | 240 | 0.31 | 0.56 | 0.50 | 0.62 | 0.43 | 0.52 |
| mistral-nemo | stored_correct | 240 | 240 | 0.88 | 0.03 | 0.02 | 0.06 | -0.10 | 0.04 |
| mistral-small | no_belief | 240 | 240 | 0.75 | 0.08 | 0.05 | 0.12 | 0.00 | 0.11 |
| mistral-small | stored_incorrect | 240 | 240 | 0.50 | 0.39 | 0.33 | 0.45 | 0.31 | 0.37 |
| mistral-small | stored_correct | 240 | 240 | 0.95 | 4.2e-03 | 7.4e-04 | 0.02 | -0.07 | 6.1e-03 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 240 | 0.13 | 0.56 | 102 | 0 | 3.9e-31 |
| mistral-nemo | stored_correct vs no_belief | 240 | 0.13 | 0.03 | 4 | 28 | 1.9e-05 |
| mistral-small | stored_incorrect vs no_belief | 240 | 0.08 | 0.39 | 77 | 3 | 1.4e-19 |
| mistral-small | stored_correct vs no_belief | 240 | 0.08 | 4.2e-03 | 0 | 18 | 7.6e-06 |
