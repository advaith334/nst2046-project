# Run frontier-smoke


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | no_belief | 4 | 4 | 1.00 | 0.00 | 0.00 | 0.49 | 0.00 |  |
| claude-sonnet | no_belief | 4 | 4 | 1.00 | 0.00 | 0.00 | 0.49 | 0.00 |  |
| gemini-argon | no_belief | 6 | 0 |  |  |  |  |  |  |
| gpt-terra-openai | no_belief | 6 | 0 |  |  |  |  |  |  |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
