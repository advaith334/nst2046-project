# Run fixes-20261105/memory_gate


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect | 96 | 96 | 0.71 | 0.17 | 0.11 | 0.25 |  | 0.15 |
| mistral-nemo | stored_correct | 96 | 96 | 0.70 | 0.16 | 0.10 | 0.24 |  | 0.15 |
| mistral-nemo | useful_label_off | 8 | 8 | 0.75 | 0.00 | 0.00 | 0.32 |  | 3.3e-04 |
| mistral-nemo | useful_label_on | 8 | 8 | 0.75 | 0.00 | 0.00 | 0.32 |  | 2.2e-04 |
| mistral-small | stored_incorrect | 96 | 96 | 0.96 | 0.03 | 0.01 | 0.09 |  | 0.04 |
| mistral-small | stored_correct | 96 | 96 | 0.94 | 0.05 | 0.02 | 0.12 |  | 0.05 |
| mistral-small | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| mistral-small | useful_label_on | 8 | 8 | 0.88 | 0.00 | 0.00 | 0.32 |  | 0.00 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
