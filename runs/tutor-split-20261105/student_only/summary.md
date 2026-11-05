# Run tutor-split-20261105/student_only


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| mistral-nemo | stored_incorrect | 96 | 96 | 0.48 | 0.44 | 0.34 | 0.54 |  | 0.44 |
| mistral-nemo | stored_correct | 96 | 96 | 0.94 | 0.03 | 0.01 | 0.09 |  | 0.03 |
| mistral-small | stored_incorrect | 96 | 96 | 0.88 | 0.10 | 0.06 | 0.18 |  | 0.08 |
| mistral-small | stored_correct | 96 | 96 | 0.96 | 0.02 | 5.7e-03 | 0.07 |  | 0.03 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
