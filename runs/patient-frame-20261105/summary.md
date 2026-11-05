# Run patient-frame-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 96 | 96 | 0.79 | 0.10 | 0.06 | 0.18 | 0.00 | 0.12 |
| mistral-nemo | stored_incorrect | 96 | 96 | 0.62 | 0.26 | 0.18 | 0.36 | 0.16 | 0.26 |
| mistral-nemo | stored_incorrect_labelled | 96 | 96 | 0.69 | 0.18 | 0.11 | 0.27 | 0.07 | 0.19 |
| mistral-nemo | stored_correct | 96 | 96 | 0.78 | 0.11 | 0.07 | 0.19 | 0.01 | 0.14 |
| mistral-small | no_belief | 96 | 96 | 0.94 | 0.03 | 0.01 | 0.09 | 0.00 | 0.06 |
| mistral-small | stored_incorrect | 96 | 96 | 0.90 | 0.09 | 0.05 | 0.17 | 0.06 | 0.08 |
| mistral-small | stored_incorrect_labelled | 96 | 96 | 0.91 | 0.08 | 0.04 | 0.16 | 0.05 | 0.04 |
| mistral-small | stored_correct | 96 | 96 | 0.96 | 0.02 | 5.7e-03 | 0.07 | -0.01 | 0.05 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 96 | 0.10 | 0.26 | 20 | 5 | 4.1e-03 |
| mistral-nemo | stored_incorrect_labelled vs no_belief | 96 | 0.10 | 0.18 | 12 | 5 | 0.14 |
| mistral-nemo | stored_correct vs no_belief | 96 | 0.10 | 0.11 | 5 | 4 | 1.00 |
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 96 | 0.26 | 0.18 | 0 | 8 | 7.8e-03 |
| mistral-small | stored_incorrect vs no_belief | 96 | 0.03 | 0.09 | 6 | 0 | 0.03 |
| mistral-small | stored_incorrect_labelled vs no_belief | 96 | 0.03 | 0.08 | 5 | 0 | 0.06 |
| mistral-small | stored_correct vs no_belief | 96 | 0.03 | 0.02 | 2 | 3 | 1.00 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 96 | 0.09 | 0.08 | 0 | 1 | 1.00 |
