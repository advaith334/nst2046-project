# Run mainmodels-probes-20261106/real_cue


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 28 | 26 | 0.96 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | stored_incorrect | 28 | 28 | 1.00 | 0.00 | 0.00 | 0.12 | 0.00 |  |
| gemma-moe | no_belief | 28 | 28 | 0.50 | 0.36 | 0.21 | 0.54 | 0.00 | 0.37 |
| gemma-moe | stored_incorrect | 28 | 28 | 0.43 | 0.50 | 0.33 | 0.67 | 0.14 | 0.67 |
| llama-8b-deepinfra | no_belief | 28 | 28 | 0.29 | 0.32 | 0.18 | 0.51 | 0.00 |  |
| llama-8b-deepinfra | stored_incorrect | 28 | 28 | 0.04 | 0.93 | 0.77 | 0.98 | 0.61 |  |
| mistral-nemo | no_belief | 28 | 28 | 0.25 | 0.36 | 0.21 | 0.54 | 0.00 | 0.33 |
| mistral-nemo | stored_incorrect | 28 | 28 | 0.14 | 0.79 | 0.60 | 0.90 | 0.43 | 0.84 |
| mistral-small | no_belief | 28 | 28 | 0.46 | 0.14 | 0.06 | 0.31 | 0.00 | 0.13 |
| mistral-small | stored_incorrect | 28 | 28 | 0.14 | 0.61 | 0.42 | 0.76 | 0.46 | 0.62 |
| qwen-small | no_belief | 28 | 14 | 1.00 | 0.00 | 0.00 | 0.22 | 0.00 | 1.2e-05 |
| qwen-small | stored_incorrect | 28 | 19 | 0.74 | 0.26 | 0.12 | 0.49 | 0.26 | 0.26 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| claude-sonnet | stored_incorrect vs no_belief | 26 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stored_incorrect vs no_belief | 28 | 0.36 | 0.50 | 7 | 3 | 0.34 |
| llama-8b-deepinfra | stored_incorrect vs no_belief | 28 | 0.32 | 0.93 | 17 | 0 | 1.5e-05 |
| mistral-nemo | stored_incorrect vs no_belief | 28 | 0.36 | 0.79 | 13 | 1 | 1.8e-03 |
| mistral-small | stored_incorrect vs no_belief | 28 | 0.14 | 0.61 | 14 | 1 | 9.8e-04 |
| qwen-small | stored_incorrect vs no_belief | 13 | 0.00 | 0.08 | 1 | 0 | 1.00 |
