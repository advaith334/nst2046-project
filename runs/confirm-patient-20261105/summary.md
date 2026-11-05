# Run confirm-patient-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 120 | 120 | 0.58 | 0.14 | 0.09 | 0.22 | 0.00 | 0.14 |
| mistral-nemo | stored_incorrect | 120 | 120 | 0.52 | 0.33 | 0.25 | 0.41 | 0.18 | 0.33 |
| mistral-nemo | stored_correct | 120 | 120 | 0.87 | 0.04 | 0.02 | 0.09 | -0.10 | 0.05 |
| mistral-small | no_belief | 120 | 120 | 0.77 | 0.07 | 0.04 | 0.14 | 0.00 | 0.05 |
| mistral-small | stored_incorrect | 120 | 120 | 0.65 | 0.19 | 0.13 | 0.27 | 0.12 | 0.12 |
| mistral-small | stored_correct | 120 | 120 | 0.87 | 0.04 | 0.02 | 0.09 | -0.03 | 0.02 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 120 | 0.14 | 0.33 | 24 | 2 | 1.0e-05 |
| mistral-nemo | stored_correct vs no_belief | 120 | 0.14 | 0.04 | 2 | 14 | 4.2e-03 |
| mistral-small | stored_incorrect vs no_belief | 120 | 0.07 | 0.19 | 14 | 0 | 1.2e-04 |
| mistral-small | stored_correct vs no_belief | 120 | 0.07 | 0.04 | 1 | 5 | 0.22 |
