# Run weak-evidence-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | no_belief | 96 | 96 | 0.83 | 0.00 | 0.00 | 0.04 | 0.00 | 0.03 |
| mistral-nemo | stored_incorrect | 96 | 96 | 0.77 | 0.17 | 0.11 | 0.25 | 0.17 | 0.17 |
| mistral-nemo | stored_incorrect_labelled | 96 | 96 | 0.82 | 0.07 | 0.04 | 0.14 | 0.07 | 0.09 |
| mistral-small | no_belief | 96 | 96 | 0.98 | 0.01 | 1.8e-03 | 0.06 | 0.00 | 0.03 |
| mistral-small | stored_incorrect | 96 | 96 | 0.91 | 0.09 | 0.05 | 0.17 | 0.08 | 0.11 |
| mistral-small | stored_incorrect_labelled | 96 | 96 | 0.92 | 0.07 | 0.04 | 0.14 | 0.06 | 0.09 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect vs no_belief | 96 | 0.00 | 0.17 | 16 | 0 | 3.1e-05 |
| mistral-nemo | stored_incorrect_labelled vs no_belief | 96 | 0.00 | 0.07 | 7 | 0 | 0.02 |
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 96 | 0.17 | 0.07 | 1 | 10 | 0.01 |
| mistral-small | stored_incorrect vs no_belief | 96 | 0.01 | 0.09 | 8 | 0 | 7.8e-03 |
| mistral-small | stored_incorrect_labelled vs no_belief | 96 | 0.01 | 0.07 | 6 | 0 | 0.03 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 96 | 0.09 | 0.07 | 0 | 2 | 0.50 |
