# Run fixes-20261105/answer_first


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect | 96 | 96 | 0.43 | 0.47 | 0.37 | 0.57 |  | 0.48 |
| mistral-nemo | stored_correct | 96 | 96 | 0.78 | 0.07 | 0.04 | 0.14 |  | 0.07 |
| mistral-nemo | useful_label_off | 8 | 8 | 0.75 | 0.00 | 0.00 | 0.32 |  | 0.10 |
| mistral-nemo | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 4.9e-03 |
| mistral-small | stored_incorrect | 96 | 96 | 0.91 | 0.08 | 0.04 | 0.16 |  | 8.3e-03 |
| mistral-small | stored_correct | 96 | 96 | 0.98 | 0.02 | 5.7e-03 | 0.07 |  | 0.08 |
| mistral-small | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| mistral-small | useful_label_on | 8 | 8 | 0.88 | 0.00 | 0.00 | 0.32 |  | 1.5e-04 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
