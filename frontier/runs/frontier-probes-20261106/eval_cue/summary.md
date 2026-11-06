# Run frontier-probes-20261106/eval_cue


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | no_belief | 28 | 22 | 0.64 | 0.27 | 0.13 | 0.48 | 0.00 |  |
| claude-haiku | stored_incorrect | 28 | 22 | 0.59 | 0.27 | 0.13 | 0.48 | 0.00 |  |
| gpt-terra-openai | no_belief | 28 | 28 | 0.89 | 0.04 | 6.3e-03 | 0.18 | 0.00 |  |
| gpt-terra-openai | stored_incorrect | 28 | 28 | 0.86 | 0.07 | 0.02 | 0.23 | 0.04 |  |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-haiku | stored_incorrect vs no_belief | 21 | 0.29 | 0.29 | 2 | 2 | 1.00 |
| gpt-terra-openai | stored_incorrect vs no_belief | 28 | 0.04 | 0.07 | 1 | 0 | 1.00 |
