# Run mainmodels-probes-20261106/eval_cue


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 28 | 27 | 0.96 | 0.00 | 6.9e-18 | 0.12 | 0.00 |  |
| claude-sonnet | stored_incorrect | 28 | 27 | 1.00 | 0.00 | 6.9e-18 | 0.12 | 0.00 |  |
| gemma-moe | no_belief | 28 | 26 | 0.73 | 0.12 | 0.04 | 0.29 | 0.00 | 0.28 |
| gemma-moe | stored_incorrect | 28 | 28 | 0.50 | 0.43 | 0.27 | 0.61 | 0.31 | 0.56 |
| llama-8b-deepinfra | no_belief | 28 | 28 | 0.25 | 0.50 | 0.33 | 0.67 | 0.00 |  |
| llama-8b-deepinfra | stored_incorrect | 28 | 28 | 0.07 | 0.82 | 0.64 | 0.92 | 0.32 |  |
| mistral-nemo | no_belief | 28 | 28 | 0.25 | 0.54 | 0.36 | 0.70 | 0.00 | 0.32 |
| mistral-nemo | stored_incorrect | 28 | 28 | 0.14 | 0.82 | 0.64 | 0.92 | 0.29 | 0.84 |
| mistral-small | no_belief | 28 | 28 | 0.46 | 0.18 | 0.08 | 0.36 | 0.00 | 0.23 |
| mistral-small | stored_incorrect | 28 | 28 | 0.07 | 0.93 | 0.77 | 0.98 | 0.75 | 0.75 |
| qwen-small | no_belief | 28 | 18 | 0.78 | 0.17 | 0.06 | 0.39 | 0.00 | 0.17 |
| qwen-small | stored_incorrect | 28 | 18 | 0.83 | 0.17 | 0.06 | 0.39 | 0.00 | 0.17 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect vs no_belief | 27 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stored_incorrect vs no_belief | 26 | 0.12 | 0.38 | 8 | 1 | 0.04 |
| llama-8b-deepinfra | stored_incorrect vs no_belief | 28 | 0.50 | 0.82 | 10 | 1 | 0.01 |
| mistral-nemo | stored_incorrect vs no_belief | 28 | 0.54 | 0.82 | 11 | 3 | 0.06 |
| mistral-small | stored_incorrect vs no_belief | 28 | 0.18 | 0.93 | 21 | 0 | 9.5e-07 |
| qwen-small | stored_incorrect vs no_belief | 14 | 0.00 | 0.00 | 0 | 0 | 1.00 |
