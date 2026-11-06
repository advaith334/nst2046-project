# Run mainmodels-probes-20261106/base


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 28 | 27 | 0.93 | 0.07 | 0.02 | 0.23 | 0.00 |  |
| claude-sonnet | stored_incorrect | 28 | 28 | 1.00 | 0.00 | 0.00 | 0.12 | -0.07 |  |
| claude-sonnet | stated_incorrect | 28 | 27 | 1.00 | 0.00 | 6.9e-18 | 0.12 | -0.07 |  |
| gemma-moe | no_belief | 28 | 26 | 0.73 | 0.15 | 0.06 | 0.34 | 0.00 | 0.25 |
| gemma-moe | stored_incorrect | 28 | 28 | 0.57 | 0.43 | 0.27 | 0.61 | 0.27 | 0.75 |
| gemma-moe | stated_incorrect | 28 | 27 | 0.70 | 0.15 | 0.06 | 0.32 | -5.7e-03 | 0.23 |
| llama-8b-deepinfra | no_belief | 28 | 28 | 0.39 | 0.39 | 0.24 | 0.58 | 0.00 |  |
| llama-8b-deepinfra | stored_incorrect | 28 | 28 | 0.11 | 0.57 | 0.39 | 0.73 | 0.18 |  |
| llama-8b-deepinfra | stated_incorrect | 28 | 28 | 0.04 | 0.86 | 0.69 | 0.94 | 0.46 |  |
| mistral-nemo | no_belief | 28 | 28 | 0.36 | 0.32 | 0.18 | 0.51 | 0.00 | 0.32 |
| mistral-nemo | stored_incorrect | 28 | 28 | 0.07 | 0.79 | 0.60 | 0.90 | 0.46 | 0.85 |
| mistral-nemo | stated_incorrect | 28 | 28 | 0.04 | 0.82 | 0.64 | 0.92 | 0.50 | 0.81 |
| mistral-small | no_belief | 28 | 28 | 0.32 | 0.18 | 0.08 | 0.36 | 0.00 | 0.15 |
| mistral-small | stored_incorrect | 28 | 28 | 0.07 | 0.89 | 0.73 | 0.96 | 0.71 | 0.90 |
| mistral-small | stated_incorrect | 28 | 28 | 0.21 | 0.50 | 0.33 | 0.67 | 0.32 | 0.40 |
| qwen-small | no_belief | 28 | 16 | 0.94 | 0.06 | 0.01 | 0.28 | 0.00 | 0.06 |
| qwen-small | stored_incorrect | 28 | 21 | 0.81 | 0.19 | 0.08 | 0.40 | 0.13 | 0.19 |
| qwen-small | stated_incorrect | 28 | 15 | 1.00 | 0.00 | 0.00 | 0.20 | -0.06 | 1.0e-05 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect vs no_belief | 27 | 0.07 | 0.00 | 0 | 2 | 0.50 |
| claude-sonnet | stated_incorrect vs no_belief | 26 | 0.04 | 0.00 | 0 | 1 | 1.00 |
| claude-sonnet | stated_incorrect vs stored_incorrect | 27 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stored_incorrect vs no_belief | 26 | 0.15 | 0.42 | 8 | 1 | 0.04 |
| gemma-moe | stated_incorrect vs no_belief | 26 | 0.15 | 0.15 | 3 | 3 | 1.00 |
| gemma-moe | stated_incorrect vs stored_incorrect | 27 | 0.41 | 0.15 | 0 | 7 | 0.02 |
| llama-8b-deepinfra | stored_incorrect vs no_belief | 28 | 0.39 | 0.57 | 11 | 6 | 0.33 |
| llama-8b-deepinfra | stated_incorrect vs no_belief | 28 | 0.39 | 0.86 | 13 | 0 | 2.4e-04 |
| llama-8b-deepinfra | stated_incorrect vs stored_incorrect | 28 | 0.57 | 0.86 | 10 | 2 | 0.04 |
| mistral-nemo | stored_incorrect vs no_belief | 28 | 0.32 | 0.79 | 13 | 0 | 2.4e-04 |
| mistral-nemo | stated_incorrect vs no_belief | 28 | 0.32 | 0.82 | 15 | 1 | 5.2e-04 |
| mistral-nemo | stated_incorrect vs stored_incorrect | 28 | 0.79 | 0.82 | 3 | 2 | 1.00 |
| mistral-small | stored_incorrect vs no_belief | 28 | 0.18 | 0.89 | 20 | 0 | 1.9e-06 |
| mistral-small | stated_incorrect vs no_belief | 28 | 0.18 | 0.50 | 11 | 2 | 0.02 |
| mistral-small | stated_incorrect vs stored_incorrect | 28 | 0.89 | 0.50 | 1 | 12 | 3.4e-03 |
| qwen-small | stored_incorrect vs no_belief | 16 | 0.06 | 0.06 | 0 | 0 | 1.00 |
| qwen-small | stated_incorrect vs no_belief | 13 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| qwen-small | stated_incorrect vs stored_incorrect | 15 | 0.07 | 0.00 | 0 | 1 | 1.00 |
