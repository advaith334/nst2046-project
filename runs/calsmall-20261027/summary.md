# Run calsmall-20261027


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | evidence_mode | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-moe | as_written | no_belief | 35 | 35 | 0.97 | 0.03 | 0.01 | 0.15 | 0.00 | 0.03 |
| gemma-moe | as_written | stored_incorrect | 35 | 35 | 1.00 | 0.00 | 0.00 | 0.10 | -0.03 | 0.00 |
| gemma-moe | none | no_belief | 34 | 34 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.00 |
| gemma-moe | none | stored_incorrect | 34 | 34 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.03 |
| mistral-nemo | as_written | no_belief | 35 | 35 | 0.54 | 0.37 | 0.23 | 0.54 | 0.00 | 0.28 |
| mistral-nemo | as_written | stored_incorrect | 35 | 35 | 0.49 | 0.40 | 0.26 | 0.56 | 0.03 | 0.39 |
| mistral-nemo | none | no_belief | 34 | 34 | 0.50 | 0.35 | 0.21 | 0.52 | 0.00 | 0.37 |
| mistral-nemo | none | stored_incorrect | 34 | 34 | 0.53 | 0.44 | 0.29 | 0.61 | 0.09 | 0.43 |
| qwen-small | as_written | no_belief | 35 | 35 | 1.00 | 0.00 | 0.00 | 0.10 | 0.00 | 0.00 |
| qwen-small | as_written | stored_incorrect | 35 | 34 | 0.91 | 0.09 | 0.03 | 0.23 | 0.09 | 0.09 |
| qwen-small | none | no_belief | 34 | 34 | 0.94 | 0.06 | 0.02 | 0.19 | 0.00 | 0.06 |
| qwen-small | none | stored_incorrect | 34 | 33 | 0.94 | 0.06 | 0.02 | 0.20 | 0.00 | 0.06 |
