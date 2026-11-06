# Run confirm-default-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| gemma-moe | no_belief | 240 | 238 | 0.89 | 0.05 | 0.03 | 0.08 | 0.00 | 0.06 |
| gemma-moe | stored_incorrect | 240 | 240 | 0.82 | 0.12 | 0.08 | 0.16 | 0.07 | 0.18 |
| gemma-moe | stored_incorrect_labelled | 240 | 240 | 0.85 | 0.07 | 0.05 | 0.12 | 0.03 | 0.10 |
| gemma-moe | stored_correct | 240 | 240 | 0.95 | 0.02 | 8.9e-03 | 0.05 | -0.03 | 0.02 |
| llama-8b-deepinfra | no_belief | 240 | 240 | 0.55 | 0.17 | 0.12 | 0.22 | 0.00 |  |
| llama-8b-deepinfra | stored_incorrect | 240 | 237 | 0.36 | 0.46 | 0.40 | 0.53 | 0.30 |  |
| llama-8b-deepinfra | stored_incorrect_labelled | 240 | 237 | 0.44 | 0.34 | 0.28 | 0.40 | 0.17 |  |
| llama-8b-deepinfra | stored_correct | 240 | 240 | 0.81 | 0.05 | 0.03 | 0.09 | -0.12 |  |
| mistral-nemo | no_belief | 240 | 240 | 0.50 | 0.15 | 0.11 | 0.21 | 0.00 | 0.17 |
| mistral-nemo | stored_incorrect | 240 | 240 | 0.23 | 0.70 | 0.64 | 0.76 | 0.55 | 0.68 |
| mistral-nemo | stored_incorrect_labelled | 240 | 240 | 0.33 | 0.55 | 0.49 | 0.61 | 0.40 | 0.55 |
| mistral-nemo | stored_correct | 240 | 240 | 0.94 | 0.02 | 6.5e-03 | 0.04 | -0.14 | 0.01 |
| mistral-small | no_belief | 240 | 240 | 0.75 | 0.08 | 0.05 | 0.13 | 0.00 | 0.09 |
| mistral-small | stored_incorrect | 240 | 240 | 0.47 | 0.43 | 0.37 | 0.50 | 0.35 | 0.44 |
| mistral-small | stored_incorrect_labelled | 240 | 240 | 0.60 | 0.28 | 0.23 | 0.34 | 0.20 | 0.36 |
| mistral-small | stored_correct | 240 | 240 | 0.98 | 4.2e-03 | 7.4e-04 | 0.02 | -0.08 | 0.01 |
| qwen-small | no_belief | 240 | 227 | 0.90 | 0.04 | 0.02 | 0.08 | 0.00 | 0.04 |
| qwen-small | stored_incorrect | 240 | 224 | 0.80 | 0.17 | 0.13 | 0.22 | 0.13 | 0.17 |
| qwen-small | stored_incorrect_labelled | 240 | 232 | 0.87 | 0.09 | 0.06 | 0.13 | 0.04 | 0.09 |
| qwen-small | stored_correct | 240 | 238 | 0.97 | 0.01 | 4.3e-03 | 0.04 | -0.03 | 0.01 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| gemma-moe | stored_incorrect vs no_belief | 238 | 0.05 | 0.11 | 15 | 0 | 6.1e-05 |
| gemma-moe | stored_incorrect_labelled vs no_belief | 238 | 0.05 | 0.08 | 7 | 0 | 0.02 |
| gemma-moe | stored_correct vs no_belief | 238 | 0.05 | 0.02 | 2 | 8 | 0.11 |
| gemma-moe | stored_incorrect_labelled vs stored_incorrect | 240 | 0.12 | 0.07 | 1 | 11 | 6.3e-03 |
| llama-8b-deepinfra | stored_incorrect vs no_belief | 237 | 0.16 | 0.46 | 78 | 7 | 2.8e-16 |
| llama-8b-deepinfra | stored_incorrect_labelled vs no_belief | 237 | 0.17 | 0.34 | 52 | 12 | 4.6e-07 |
| llama-8b-deepinfra | stored_correct vs no_belief | 240 | 0.17 | 0.05 | 3 | 31 | 7.7e-07 |
| llama-8b-deepinfra | stored_incorrect_labelled vs stored_incorrect | 234 | 0.47 | 0.34 | 13 | 43 | 7.3e-05 |
| mistral-nemo | stored_incorrect vs no_belief | 240 | 0.15 | 0.70 | 134 | 2 | 2.1e-37 |
| mistral-nemo | stored_incorrect_labelled vs no_belief | 240 | 0.15 | 0.55 | 100 | 5 | 5.0e-24 |
| mistral-nemo | stored_correct vs no_belief | 240 | 0.15 | 0.02 | 2 | 35 | 1.0e-08 |
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 240 | 0.70 | 0.55 | 1 | 38 | 1.5e-10 |
| mistral-small | stored_incorrect vs no_belief | 240 | 0.08 | 0.43 | 85 | 1 | 2.2e-24 |
| mistral-small | stored_incorrect_labelled vs no_belief | 240 | 0.08 | 0.28 | 51 | 4 | 2.0e-11 |
| mistral-small | stored_correct vs no_belief | 240 | 0.08 | 4.2e-03 | 0 | 19 | 3.8e-06 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 240 | 0.43 | 0.28 | 2 | 39 | 7.8e-10 |
| qwen-small | stored_incorrect vs no_belief | 212 | 0.04 | 0.17 | 27 | 0 | 1.5e-08 |
| qwen-small | stored_incorrect_labelled vs no_belief | 220 | 0.05 | 0.09 | 10 | 0 | 2.0e-03 |
| qwen-small | stored_correct vs no_belief | 225 | 0.04 | 0.01 | 0 | 7 | 0.02 |
| qwen-small | stored_incorrect_labelled vs stored_incorrect | 216 | 0.17 | 0.09 | 0 | 17 | 1.5e-05 |
