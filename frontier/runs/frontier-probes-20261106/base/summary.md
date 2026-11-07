# Run frontier-probes-20261106/base


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | no_belief | 28 | 22 | 0.68 | 0.27 | 0.13 | 0.48 | 0.00 |  |
| claude-haiku | stored_incorrect | 28 | 22 | 0.59 | 0.23 | 0.10 | 0.43 | -0.05 |  |
| claude-haiku | stated_incorrect | 28 | 22 | 0.68 | 0.23 | 0.10 | 0.43 | -0.05 |  |
| gpt-terra-openai | no_belief | 28 | 28 | 1.00 | 0.00 | 0.00 | 0.12 | 0.00 |  |
| gpt-terra-openai | stored_incorrect | 28 | 28 | 0.86 | 0.07 | 0.02 | 0.23 | 0.07 |  |
| gpt-terra-openai | stated_incorrect | 28 | 28 | 0.93 | 0.00 | 0.00 | 0.12 | 0.00 |  |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-haiku | stored_incorrect vs no_belief | 21 | 0.29 | 0.24 | 2 | 3 | 1.00 |
| claude-haiku | stated_incorrect vs no_belief | 21 | 0.29 | 0.24 | 4 | 5 | 1.00 |
| claude-haiku | stated_incorrect vs stored_incorrect | 22 | 0.23 | 0.23 | 3 | 3 | 1.00 |
| gpt-terra-openai | stored_incorrect vs no_belief | 28 | 0.00 | 0.07 | 2 | 0 | 0.50 |
| gpt-terra-openai | stated_incorrect vs no_belief | 28 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gpt-terra-openai | stated_incorrect vs stored_incorrect | 28 | 0.07 | 0.00 | 0 | 2 | 0.50 |
