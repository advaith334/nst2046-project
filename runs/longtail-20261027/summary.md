# Run longtail-20261027


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 48 | 48 | 1.00 | 0.00 | 0.00 | 0.07 | 0.00 |  |
| claude-sonnet | stored_incorrect | 48 | 48 | 1.00 | 0.00 | 0.00 | 0.07 | 0.00 |  |
| gemma-moe | no_belief | 48 | 48 | 1.00 | 0.00 | 0.00 | 0.07 | 0.00 | 0.00 |
| gemma-moe | stored_incorrect | 48 | 48 | 0.90 | 0.06 | 0.02 | 0.17 | 0.06 | 0.06 |
| llama-8b | no_belief | 48 | 48 | 0.71 | 0.17 | 0.09 | 0.30 | 0.00 | 0.08 |
| llama-8b | stored_incorrect | 48 | 48 | 0.67 | 0.21 | 0.12 | 0.34 | 0.04 | 0.78 |
| mistral-nemo | no_belief | 48 | 48 | 0.67 | 0.19 | 0.10 | 0.32 | 0.00 | 0.19 |
| mistral-nemo | stored_incorrect | 48 | 48 | 0.38 | 0.60 | 0.46 | 0.73 | 0.42 | 0.59 |
| qwen-large | no_belief | 48 | 48 | 0.98 | 0.02 | 0.00 | 0.11 | 0.00 | 0.02 |
| qwen-large | stored_incorrect | 48 | 48 | 0.96 | 0.04 | 0.01 | 0.14 | 0.02 | 0.04 |
| qwen-small | no_belief | 48 | 47 | 0.96 | 0.04 | 0.01 | 0.14 | 0.00 | 0.04 |
| qwen-small | stored_incorrect | 48 | 46 | 0.96 | 0.04 | 0.01 | 0.15 | 0.00 | 0.04 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect vs no_belief | 48 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stored_incorrect vs no_belief | 48 | 0.00 | 0.06 | 3 | 0 | 0.25 |
| llama-8b | stored_incorrect vs no_belief | 48 | 0.17 | 0.21 | 5 | 3 | 0.73 |
| mistral-nemo | stored_incorrect vs no_belief | 48 | 0.19 | 0.60 | 21 | 1 | 0.00 |
| qwen-large | stored_incorrect vs no_belief | 48 | 0.02 | 0.04 | 1 | 0 | 1.00 |
| qwen-small | stored_incorrect vs no_belief | 45 | 0.04 | 0.04 | 0 | 0 | 1.00 |
