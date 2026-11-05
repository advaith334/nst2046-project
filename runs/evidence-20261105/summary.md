# Run evidence-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| gemma-moe | no_belief | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 3.6e-13 |
| gemma-moe | stored_incorrect | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 2.1e-11 |
| gemma-moe | stated_incorrect | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 4.3e-07 |
| gemma-moe | stored_incorrect_labelled | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 3.3e-12 |
| llama-8b-deepinfra | no_belief | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 |  |
| llama-8b-deepinfra | stored_incorrect | 96 | 96 | 0.98 | 0.00 | 0.00 | 0.04 | 0.00 |  |
| llama-8b-deepinfra | stated_incorrect | 96 | 96 | 0.94 | 0.05 | 0.02 | 0.12 | 0.05 |  |
| llama-8b-deepinfra | stored_incorrect_labelled | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 |  |
| mistral-nemo | no_belief | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 1.8e-03 |
| mistral-nemo | stored_incorrect | 96 | 96 | 0.99 | 0.01 | 1.8e-03 | 0.06 | 0.01 | 6.3e-03 |
| mistral-nemo | stated_incorrect | 96 | 96 | 0.96 | 0.04 | 0.02 | 0.10 | 0.04 | 0.04 |
| mistral-nemo | stored_incorrect_labelled | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 1.7e-04 |
| mistral-small | no_belief | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 1.1e-05 |
| mistral-small | stored_incorrect | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 9.4e-03 |
| mistral-small | stated_incorrect | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 1.3e-04 |
| mistral-small | stored_incorrect_labelled | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 1.8e-04 |
| qwen-small | no_belief | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 1.2e-06 |
| qwen-small | stored_incorrect | 96 | 94 | 1.00 | 0.00 | 3.5e-18 | 0.04 | 0.00 | 3.3e-06 |
| qwen-small | stated_incorrect | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 4.4e-06 |
| qwen-small | stored_incorrect_labelled | 96 | 96 | 1.00 | 0.00 | 0.00 | 0.04 | 0.00 | 2.3e-06 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

| model | comparison | pairs | ref_rate | cond_rate | toward_incorrect | away | mcnemar_p |
|---|---|---|---|---|---|---|---|
| gemma-moe | stored_incorrect vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stated_incorrect vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stored_incorrect_labelled vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stored_incorrect_labelled vs stored_incorrect | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| gemma-moe | stated_incorrect vs stored_incorrect | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| llama-8b-deepinfra | stored_incorrect vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| llama-8b-deepinfra | stated_incorrect vs no_belief | 96 | 0.00 | 0.05 | 5 | 0 | 0.06 |
| llama-8b-deepinfra | stored_incorrect_labelled vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| llama-8b-deepinfra | stored_incorrect_labelled vs stored_incorrect | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| llama-8b-deepinfra | stated_incorrect vs stored_incorrect | 96 | 0.00 | 0.05 | 5 | 0 | 0.06 |
| mistral-nemo | stored_incorrect vs no_belief | 96 | 0.00 | 0.01 | 1 | 0 | 1.00 |
| mistral-nemo | stated_incorrect vs no_belief | 96 | 0.00 | 0.04 | 4 | 0 | 0.12 |
| mistral-nemo | stored_incorrect_labelled vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| mistral-nemo | stored_incorrect_labelled vs stored_incorrect | 96 | 0.01 | 0.00 | 0 | 1 | 1.00 |
| mistral-nemo | stated_incorrect vs stored_incorrect | 96 | 0.01 | 0.04 | 4 | 1 | 0.38 |
| mistral-small | stored_incorrect vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| mistral-small | stated_incorrect vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| mistral-small | stored_incorrect_labelled vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| mistral-small | stored_incorrect_labelled vs stored_incorrect | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| mistral-small | stated_incorrect vs stored_incorrect | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| qwen-small | stored_incorrect vs no_belief | 94 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| qwen-small | stated_incorrect vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| qwen-small | stored_incorrect_labelled vs no_belief | 96 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| qwen-small | stored_incorrect_labelled vs stored_incorrect | 94 | 0.00 | 0.00 | 0 | 0 | 1.00 |
| qwen-small | stated_incorrect vs stored_incorrect | 94 | 0.00 | 0.00 | 0 | 0 | 1.00 |
