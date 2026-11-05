# Run local-base-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| nemo-base-local | no_belief | 96 | 96 | 0.64 | 0.21 | 0.14 | 0.30 | 0.00 | 0.23 |
| nemo-base-local | stored_incorrect | 96 | 96 | 0.25 | 0.71 | 0.61 | 0.79 | 0.50 | 0.65 |
| nemo-base-local | stated_incorrect | 96 | 96 | 0.29 | 0.66 | 0.56 | 0.74 | 0.45 | 0.59 |
| nemo-base-local | stored_incorrect_labelled | 96 | 96 | 0.38 | 0.61 | 0.51 | 0.71 | 0.41 | 0.52 |
| nemo-base-local | stored_unrelated | 96 | 96 | 0.62 | 0.23 | 0.16 | 0.32 | 0.02 | 0.21 |
| nemo-base-local | stored_correct | 96 | 96 | 0.97 | 0.00 | 0.00 | 0.04 | -0.21 | 0.04 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| nemo-base-local | stored_incorrect vs no_belief | 96 | 0.21 | 0.71 | 51 | 3 | 2.9e-12 |
| nemo-base-local | stated_incorrect vs no_belief | 96 | 0.21 | 0.66 | 45 | 2 | 1.6e-11 |
| nemo-base-local | stored_incorrect_labelled vs no_belief | 96 | 0.21 | 0.61 | 41 | 2 | 2.2e-10 |
| nemo-base-local | stored_unrelated vs no_belief | 96 | 0.21 | 0.23 | 11 | 9 | 0.82 |
| nemo-base-local | stored_correct vs no_belief | 96 | 0.21 | 0.00 | 0 | 20 | 1.9e-06 |
| nemo-base-local | stored_incorrect_labelled vs stored_incorrect | 96 | 0.71 | 0.61 | 4 | 13 | 0.05 |
| nemo-base-local | stated_incorrect vs stored_incorrect | 96 | 0.71 | 0.66 | 10 | 15 | 0.42 |
