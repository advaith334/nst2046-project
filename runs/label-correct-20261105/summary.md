# Run label-correct-20261105


`incorrect_rate` = share of usable responses choosing the option that matches the incorrect belief (for useful-memory checks: the stale belief). `delta_vs_baseline` is against `no_belief` for the same model. CIs are Wilson 95%. Errors and unparseable responses are excluded from rates and counted separately in summary.csv.

| model | condition | n | usable | correct_rate | incorrect_rate | incorrect_ci_low | incorrect_ci_high | delta_vs_baseline | mean_p_incorrect |
|---|---|---|---|---|---|---|---|---|---|
| gemma-moe | stored_correct_labelled | 96 | 96 | 0.99 | 0.00 | 0.00 | 0.04 |  | 1.1e-09 |
| llama-8b-deepinfra | stored_correct_labelled | 96 | 96 | 0.80 | 0.11 | 0.07 | 0.19 |  |  |
| mistral-nemo | stored_correct_labelled | 96 | 96 | 0.85 | 0.07 | 0.04 | 0.14 |  | 0.06 |
| mistral-small | stored_correct_labelled | 96 | 96 | 0.98 | 0.02 | 5.7e-03 | 0.07 |  | 0.01 |
| qwen-small | stored_correct_labelled | 96 | 95 | 0.99 | 0.01 | 1.9e-03 | 0.06 |  | 0.01 |

## Paired comparisons

Trials matched on item, evidence mode and rep. `toward_incorrect` / `away` count pairs that flipped to / from the incorrect option; `mcnemar_p` is the exact two-sided McNemar test. With several models and comparisons, treat p-values as exploratory.

_no paired comparisons_
