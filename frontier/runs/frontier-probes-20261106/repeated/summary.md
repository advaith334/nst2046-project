# Run frontier-probes-20261106/repeated


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | stored_incorrect | 28 | 23 | 0.57 | 0.17 | 0.07 | 0.37 |  |  |
| gpt-terra-openai | stored_incorrect | 28 | 28 | 0.86 | 0.11 | 0.04 | 0.27 |  |  |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
