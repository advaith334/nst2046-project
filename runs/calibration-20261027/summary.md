# Run calibration-20261027


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | evidence_mode | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet | as_written | no_belief | 35 | 35 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 |  |
| claude-sonnet | as_written | stored_incorrect | 35 | 35 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 |  |
| claude-sonnet | none | no_belief | 34 | 34 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 |  |
| claude-sonnet | none | stored_incorrect | 34 | 34 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 |  |
| llama-8b | as_written | no_belief | 35 | 35 | 0.54 | 0.34 | 0.21 | 0.51 | 0.00 |  |
| llama-8b | as_written | stored_incorrect | 35 | 35 | 0.66 | 0.26 | 0.14 | 0.42 | -0.09 | 0.32 |
| llama-8b | none | no_belief | 34 | 34 | 0.59 | 0.29 | 0.17 | 0.46 | 0.00 |  |
| llama-8b | none | stored_incorrect | 34 | 34 | 0.62 | 0.26 | 0.15 | 0.43 | -0.03 | 0.87 |
| qwen-large | as_written | no_belief | 35 | 35 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.00 |
| qwen-large | as_written | stored_incorrect | 35 | 35 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.00 |
| qwen-large | none | no_belief | 34 | 34 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.00 |
| qwen-large | none | stored_incorrect | 34 | 34 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.00 |
