# Run local-base-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| nemo-base-local | no_belief | 96 | 91 | 0.63 | 0.22 | 0.15 | 0.32 | 0.00 | 0.23 |
| nemo-base-local | stored_incorrect | 96 | 95 | 0.25 | 0.71 | 0.61 | 0.79 | 0.49 | 0.65 |
| nemo-base-local | stated_incorrect | 96 | 86 | 0.29 | 0.65 | 0.55 | 0.74 | 0.43 | 0.59 |
| nemo-base-local | stored_incorrect_labelled | 96 | 96 | 0.38 | 0.61 | 0.51 | 0.71 | 0.39 | 0.52 |
| nemo-base-local | stored_unrelated | 96 | 95 | 0.62 | 0.23 | 0.16 | 0.33 | 0.01 | 0.21 |
| nemo-base-local | stored_correct | 96 | 92 | 0.97 | 0.00 | 0.00 | 0.04 | -0.22 | 0.04 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| nemo-base-local | stored_incorrect vs no_belief | 91 | 0.22 | 0.70 | 47 | 3 | 3.7e-11 |
| nemo-base-local | stated_incorrect vs no_belief | 82 | 0.22 | 0.66 | 38 | 2 | 1.5e-09 |
| nemo-base-local | stored_incorrect_labelled vs no_belief | 91 | 0.22 | 0.62 | 38 | 2 | 1.5e-09 |
| nemo-base-local | stored_unrelated vs no_belief | 90 | 0.22 | 0.24 | 11 | 9 | 0.82 |
| nemo-base-local | stored_correct vs no_belief | 89 | 0.21 | 0.00 | 0 | 19 | 3.8e-06 |
| nemo-base-local | stored_incorrect_labelled vs stored_incorrect | 95 | 0.71 | 0.61 | 4 | 13 | 0.05 |
| nemo-base-local | stated_incorrect vs stored_incorrect | 86 | 0.69 | 0.65 | 10 | 13 | 0.68 |
