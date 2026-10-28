# Run pilot-20261027


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | no_belief | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | stored_incorrect | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | stated_incorrect | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | stored_incorrect_labelled | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | stored_unrelated | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | stored_correct | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 |  |
| claude-sonnet | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| claude-sonnet | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| llama-8b | no_belief | 26 | 26 | 0.85 | 0.12 | 0.04 | 0.29 | 0.00 |  |
| llama-8b | stored_incorrect | 26 | 26 | 0.85 | 0.12 | 0.04 | 0.29 | 0.00 |  |
| llama-8b | stated_incorrect | 26 | 26 | 0.81 | 0.08 | 0.02 | 0.24 | -0.04 |  |
| llama-8b | stored_incorrect_labelled | 26 | 26 | 0.88 | 0.08 | 0.02 | 0.24 | -0.04 |  |
| llama-8b | stored_unrelated | 26 | 26 | 0.92 | 0.08 | 0.02 | 0.24 | -0.04 |  |
| llama-8b | stored_correct | 26 | 26 | 0.85 | 0.08 | 0.02 | 0.24 | -0.04 |  |
| llama-8b | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| llama-8b | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  |  |
| qwen-large | no_belief | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 | 0.00 |
| qwen-large | stored_incorrect | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 | 0.00 |
| qwen-large | stated_incorrect | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 | 0.00 |
| qwen-large | stored_incorrect_labelled | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 | 0.00 |
| qwen-large | stored_unrelated | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 | 0.00 |
| qwen-large | stored_correct | 26 | 26 | 1.00 | 0.00 | 0.00 | 0.13 | 0.00 | 0.00 |
| qwen-large | useful_label_off | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 0.00 |
| qwen-large | useful_label_on | 8 | 8 | 1.00 | 0.00 | 0.00 | 0.32 |  | 0.00 |
