# Run confirm-tutor-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 120 | 120 | 0.35 | 0.26 | 0.19 | 0.34 | 0.00 | 0.23 |
| mistral-nemo | stored_incorrect | 120 | 120 | 0.38 | 0.35 | 0.27 | 0.44 | 0.09 | 0.33 |
| mistral-nemo | stored_correct | 120 | 120 | 0.55 | 0.15 | 0.10 | 0.22 | -0.11 | 0.16 |
| mistral-small | no_belief | 120 | 120 | 0.68 | 0.07 | 0.04 | 0.14 | 0.00 | 0.08 |
| mistral-small | stored_incorrect | 120 | 120 | 0.66 | 0.14 | 0.09 | 0.22 | 0.07 | 0.23 |
| mistral-small | stored_correct | 120 | 120 | 0.73 | 0.08 | 0.05 | 0.15 | 8.3e-03 | 0.10 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 120 | 0.26 | 0.35 | 25 | 14 | 0.11 |
| mistral-nemo | stored_correct vs no_belief | 120 | 0.26 | 0.15 | 12 | 25 | 0.05 |
| mistral-small | stored_incorrect vs no_belief | 120 | 0.07 | 0.14 | 15 | 7 | 0.13 |
| mistral-small | stored_correct vs no_belief | 120 | 0.07 | 0.08 | 9 | 8 | 1.00 |
