# Run fixes-20261105/tutor


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 96 | 96 | 0.72 | 0.16 | 0.10 | 0.24 | 0.00 | 0.17 |
| mistral-nemo | stored_incorrect | 96 | 96 | 0.62 | 0.24 | 0.17 | 0.33 | 0.08 | 0.24 |
| mistral-nemo | stored_incorrect_labelled | 96 | 96 | 0.68 | 0.24 | 0.17 | 0.33 | 0.08 | 0.24 |
| mistral-nemo | stored_correct | 96 | 96 | 0.75 | 0.15 | 0.09 | 0.23 | -0.01 | 0.15 |
| mistral-nemo | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 3.8e-04 |
| mistral-nemo | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 3.6e-04 |
| mistral-small | no_belief | 96 | 96 | 0.95 | 0.04 | 0.02 | 0.10 | 0.00 | 0.03 |
| mistral-small | stored_incorrect | 96 | 96 | 0.92 | 0.07 | 0.04 | 0.14 | 0.03 | 0.06 |
| mistral-small | stored_incorrect_labelled | 96 | 96 | 0.89 | 0.10 | 0.06 | 0.18 | 0.06 | 0.13 |
| mistral-small | stored_correct | 96 | 96 | 0.91 | 0.05 | 0.02 | 0.12 | 0.01 | 0.14 |
| mistral-small | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 3.3e-05 |
| mistral-small | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 2.3e-05 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 96 | 0.16 | 0.24 | 14 | 6 | 0.12 |
| mistral-nemo | stored_incorrect_labelled vs no_belief | 96 | 0.16 | 0.24 | 11 | 3 | 0.06 |
| mistral-nemo | stored_correct vs no_belief | 96 | 0.16 | 0.15 | 5 | 6 | 1.00 |
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 96 | 0.24 | 0.24 | 6 | 6 | 1.00 |
| mistral-small | stored_incorrect vs no_belief | 96 | 0.04 | 0.07 | 4 | 1 | 0.38 |
| mistral-small | stored_incorrect_labelled vs no_belief | 96 | 0.04 | 0.10 | 6 | 0 | 0.03 |
| mistral-small | stored_correct vs no_belief | 96 | 0.04 | 0.05 | 4 | 3 | 1.00 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 96 | 0.07 | 0.10 | 3 | 0 | 0.25 |
