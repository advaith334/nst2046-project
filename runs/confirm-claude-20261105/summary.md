# Run confirm-claude-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 80 | 80 | 0.93 | 0.03 | 6.9e-03 | 0.09 | 0.00 |  |
| claude-sonnet | stored_incorrect | 87 | 87 | 0.92 | 0.03 | 0.01 | 0.10 | 9.5e-03 |  |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect vs no_belief | 60 | 0.03 | 0.05 | 1 | 0 | 1.00 |
