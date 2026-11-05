# Run wrappers-20261105/label_short


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect | 96 | 96 | 0.39 | 0.57 | 0.47 | 0.67 |  | 0.58 |
| mistral-nemo | stored_incorrect_labelled | 96 | 96 | 0.52 | 0.42 | 0.32 | 0.52 |  | 0.38 |
| mistral-small | stored_incorrect | 96 | 96 | 0.84 | 0.14 | 0.08 | 0.22 |  | 0.16 |
| mistral-small | stored_incorrect_labelled | 96 | 96 | 0.86 | 0.11 | 0.07 | 0.19 |  | 0.11 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 96 | 0.57 | 0.42 | 3 | 18 | 1.5e-03 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 96 | 0.14 | 0.11 | 0 | 2 | 0.50 |
