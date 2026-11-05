# Run wrappers-20261105/verified_profile


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect | 96 | 96 | 0.39 | 0.57 | 0.47 | 0.67 |  | 0.55 |
| mistral-nemo | stored_incorrect_labelled | 96 | 96 | 0.62 | 0.30 | 0.22 | 0.40 |  | 0.30 |
| mistral-small | stored_incorrect | 96 | 96 | 0.84 | 0.15 | 0.09 | 0.23 |  | 0.17 |
| mistral-small | stored_incorrect_labelled | 96 | 96 | 0.89 | 0.10 | 0.06 | 0.18 |  | 0.08 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 96 | 0.57 | 0.30 | 0 | 26 | 3.0e-08 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 96 | 0.15 | 0.10 | 0 | 4 | 0.12 |
