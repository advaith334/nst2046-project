# Run confirm-wordings-20261105/may_be_wrong


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 240 | 240 | 0.48 | 0.15 | 0.11 | 0.20 | 0.00 | 0.17 |
| mistral-nemo | stored_incorrect | 240 | 240 | 0.38 | 0.45 | 0.39 | 0.51 | 0.30 | 0.44 |
| mistral-nemo | stored_correct | 240 | 240 | 0.82 | 0.06 | 0.04 | 0.10 | -0.08 | 0.06 |
| mistral-small | no_belief | 240 | 240 | 0.73 | 0.06 | 0.04 | 0.10 | 0.00 | 0.11 |
| mistral-small | stored_incorrect | 240 | 240 | 0.55 | 0.32 | 0.26 | 0.38 | 0.25 | 0.33 |
| mistral-small | stored_correct | 240 | 240 | 0.94 | 0.02 | 6.5e-03 | 0.04 | -0.05 | 0.03 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 240 | 0.15 | 0.45 | 79 | 6 | 2.4e-17 |
| mistral-nemo | stored_correct vs no_belief | 240 | 0.15 | 0.06 | 8 | 28 | 1.2e-03 |
| mistral-small | stored_incorrect vs no_belief | 240 | 0.06 | 0.32 | 62 | 1 | 1.4e-17 |
| mistral-small | stored_correct vs no_belief | 240 | 0.06 | 0.02 | 1 | 12 | 3.4e-03 |
