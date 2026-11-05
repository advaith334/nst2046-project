# Run fixes-20261105/rule


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect | 96 | 96 | 0.44 | 0.49 | 0.39 | 0.59 |  | 0.48 |
| mistral-nemo | stored_correct | 96 | 96 | 0.89 | 0.07 | 0.04 | 0.14 |  | 0.07 |
| mistral-nemo | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 3.1e-04 |
| mistral-nemo | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 2.0e-04 |
| mistral-small | stored_incorrect | 96 | 96 | 0.78 | 0.22 | 0.15 | 0.31 |  | 0.25 |
| mistral-small | stored_correct | 96 | 96 | 0.97 | 0.02 | 5.7e-03 | 0.07 |  | 1.0e-03 |
| mistral-small | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| mistral-small | useful_label_on | 8 | 8 | 0.88 | 0.00 | 0.00 | 0.32 |  | 5.1e-05 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
