# Run local-instruct-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| nemo-instruct-local | no_belief | 96 | 96 | 0.72 | 0.16 | 0.10 | 0.24 | 0.00 | 0.17 |
| nemo-instruct-local | stored_incorrect | 96 | 96 | 0.32 | 0.64 | 0.54 | 0.72 | 0.48 | 0.63 |
| nemo-instruct-local | stated_incorrect | 96 | 96 | 0.36 | 0.57 | 0.47 | 0.67 | 0.42 | 0.57 |
| nemo-instruct-local | stored_incorrect_labelled | 96 | 96 | 0.53 | 0.45 | 0.35 | 0.55 | 0.29 | 0.43 |
| nemo-instruct-local | stored_unrelated | 96 | 96 | 0.68 | 0.22 | 0.15 | 0.31 | 0.06 | 0.18 |
| nemo-instruct-local | stored_correct | 96 | 96 | 0.98 | 0.01 | 1.8e-03 | 0.06 | -0.15 | 9.0e-03 |
| nemo-instruct-local-chat | no_belief | 96 | 96 | 0.72 | 0.14 | 0.08 | 0.22 | 0.00 | 0.16 |
| nemo-instruct-local-chat | stored_incorrect | 96 | 96 | 0.34 | 0.61 | 0.51 | 0.71 | 0.48 | 0.58 |
| nemo-instruct-local-chat | stated_incorrect | 96 | 96 | 0.48 | 0.43 | 0.33 | 0.53 | 0.29 | 0.45 |
| nemo-instruct-local-chat | stored_incorrect_labelled | 96 | 96 | 0.57 | 0.36 | 0.28 | 0.46 | 0.23 | 0.37 |
| nemo-instruct-local-chat | stored_unrelated | 96 | 96 | 0.70 | 0.17 | 0.11 | 0.25 | 0.03 | 0.18 |
| nemo-instruct-local-chat | stored_correct | 96 | 96 | 0.98 | 0.02 | 5.7e-03 | 0.07 | -0.11 | 0.02 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| nemo-instruct-local | stored_incorrect vs no_belief | 96 | 0.16 | 0.64 | 47 | 1 | 3.5e-13 |
| nemo-instruct-local | stated_incorrect vs no_belief | 96 | 0.16 | 0.57 | 42 | 2 | 1.1e-10 |
| nemo-instruct-local | stored_incorrect_labelled vs no_belief | 96 | 0.16 | 0.45 | 29 | 1 | 5.8e-08 |
| nemo-instruct-local | stored_unrelated vs no_belief | 96 | 0.16 | 0.22 | 7 | 1 | 0.07 |
| nemo-instruct-local | stored_correct vs no_belief | 96 | 0.16 | 0.01 | 0 | 14 | 1.2e-04 |
| nemo-instruct-local | stored_incorrect_labelled vs stored_incorrect | 96 | 0.64 | 0.45 | 1 | 19 | 4.0e-05 |
| nemo-instruct-local | stated_incorrect vs stored_incorrect | 96 | 0.64 | 0.57 | 3 | 9 | 0.15 |
| nemo-instruct-local-chat | stored_incorrect vs no_belief | 96 | 0.14 | 0.61 | 47 | 1 | 3.5e-13 |
| nemo-instruct-local-chat | stated_incorrect vs no_belief | 96 | 0.14 | 0.43 | 29 | 1 | 5.8e-08 |
| nemo-instruct-local-chat | stored_incorrect_labelled vs no_belief | 96 | 0.14 | 0.36 | 23 | 1 | 3.0e-06 |
| nemo-instruct-local-chat | stored_unrelated vs no_belief | 96 | 0.14 | 0.17 | 6 | 3 | 0.51 |
| nemo-instruct-local-chat | stored_correct vs no_belief | 96 | 0.14 | 0.02 | 0 | 11 | 9.8e-04 |
| nemo-instruct-local-chat | stored_incorrect_labelled vs stored_incorrect | 96 | 0.61 | 0.36 | 0 | 24 | 1.2e-07 |
| nemo-instruct-local-chat | stated_incorrect vs stored_incorrect | 96 | 0.61 | 0.43 | 3 | 21 | 2.8e-04 |
