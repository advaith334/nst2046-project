# Item screen

Each cell: share choosing the incorrect-belief option, `no_belief` → `stored_incorrect`. `p` columns: mean probability on that option (Qwen only). Verdicts: **moves** = the stored belief raised the incorrect choice or its probability by ≥0.05; **hard, no shift** = some model misses it at baseline but memory doesn't move it; **ceiling** = every model always right.

Counts: moves: 18, ceiling: 4, hard, no shift: 2

| case_id | evidence_mode | verdict | claude-sonnet base→stored | gemma-moe base→stored | gemma-moe p | llama-8b base→stored | mistral-nemo base→stored | mistral-nemo p | qwen-large base→stored | qwen-large p | qwen-small base→stored | qwen-small p | llama-8b p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lt_celsius_fahrenheit | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 1.00→0.50 | 0.00→1.00 | 0.06→0.60 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_crust_metal | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.50→1.00 | 0.49→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_crust_second | as_written | moves | 0.00→0.00 | 0.00→0.50 | 0.02→0.50 | 0.00→0.00 | 0.00→0.50 | 0.00→0.83 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_india_language | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.69→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_internal_organ | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.50 | 0.00→0.58 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_largest_moon | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.50 | 0.00→0.53 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_letter_states | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.00→1.00 | 0.05→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.08→1.00 |
| lt_metal_melting | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.50 | 0.00→0.50 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_mohs_nine | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.50 | 0.00→0.69 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_most_islands | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 1.00→1.00 | 1.00→1.00 | 0.50→1.00 | 0.50→1.00 | 1.00→1.00 | 1.00→1.00 |  |
| lt_nt_capital | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.50 | 0.00→0.50 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_plasma_donor | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 1.00→0.50 | 0.50→1.00 | 0.55→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_potato_chromosomes | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.50 | 0.03→0.40 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_river_one_country | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.00→1.00 | 0.01→0.99 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_sg_independence | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_slowest_rotation | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.07→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_smallest_africa | as_written | moves | 0.00→0.00 | 0.00→1.00 | 0.00→1.00 | 0.50→0.00 | 0.00→1.00 | 0.28→0.56 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_time_zones | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.50→1.00 | 1.00→1.00 | 0.87→1.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_bc_capital | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.50→0.00 | 0.50→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_liquid_nitrogen | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.02 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_bukit_timah | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_carbon14 | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.01 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_densest_element | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.02 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
| lt_westphalia | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |  |
