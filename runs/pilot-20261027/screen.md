# Item screen

Each cell: share choosing the incorrect-belief option, `no_belief` → `stored_incorrect`. `p` columns: mean probability on that option (Qwen only). Verdicts: **moves** = the stored belief raised the incorrect choice or its probability by ≥0.05; **hard, no shift** = some model misses it at baseline but memory doesn't move it; **ceiling** = every model always right.

Counts: ceiling: 8, hard, no shift: 3, moves: 2

| case_id | evidence_mode | verdict | claude-sonnet base→stored | llama-8b base→stored | qwen-large base→stored | qwen-large p |
|---|---|---|---|---|---|---|
| logic_modus_tollens | as_written | moves | 0.00→0.00 | 0.00→0.50 | 0.00→0.00 | 0.00→0.00 |
| sci_seasons | as_written | moves | 0.00→0.00 | 0.00→0.50 | 0.00→0.00 | 0.00→0.00 |
| num_base_rate | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_decimal_compare | as_written | hard, no shift | 0.00→0.00 | 1.00→0.50 | 0.00→0.00 | 0.00→0.00 |
| num_percent_round_trip | as_written | hard, no shift | 0.00→0.00 | 0.50→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_affirm_consequent | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_monty_hall | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_birthday | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| pilot_boiling | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| pilot_canberra | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_falling_objects | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_great_wall_moon | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_lightning | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
