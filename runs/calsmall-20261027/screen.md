# Item screen

Each cell: share choosing the incorrect-belief option, `no_belief` → `stored_incorrect`. `p` columns: mean probability on that option (Qwen only). Verdicts: **moves** = the stored belief raised the incorrect choice or its probability by ≥0.05; **hard, no shift** = some model misses it at baseline but memory doesn't move it; **ceiling** = every model always right.

Counts: moves: 27, ceiling: 24, hard, no shift: 18

| case_id | evidence_mode | verdict | gemma-moe base→stored | gemma-moe p | mistral-nemo base→stored | mistral-nemo p | qwen-small base→stored | qwen-small p |
|---|---|---|---|---|---|---|---|---|
| cal_logic_conjunction | none | moves | 0.00→0.00 | 0.00→1.00 | 1.00→1.00 | 0.77→0.71 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_overlap | as_written | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.88→0.97 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_overlap | none | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.81→0.98 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_wason | as_written | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.68→0.74 | 0.00→0.00 | 0.00→0.00 |
| cal_num_average_speed | none | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.27→0.17 | 0.00→0.00 | 0.00→0.00 |
| cal_num_bat_ball | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.03→0.22 | 0.00→0.00 | 0.00→0.00 |
| cal_num_digit_ones | as_written | moves | 1.00→0.00 | 1.00→0.00 | 1.00→1.00 | 0.38→0.72 | 0.00→1.00 | 0.00→1.00 |
| cal_num_digit_ones | none | moves | 0.00→0.00 | 0.06→0.00 | 0.00→0.00 | 0.40→0.79 | 1.00→0.00 | 1.00→0.00 |
| cal_num_lily_pads | as_written | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.45→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_lily_pads | none | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.48→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_point_nine | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.02→0.87 | 0.00→0.00 | 0.00→0.00 |
| cal_num_two_children | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.13→0.60 | 0.00→0.00 | 0.00→0.00 |
| cal_num_two_children | none | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.02→0.70 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_base_to_peak | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.95 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_base_to_peak | none | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.44→0.99 | 0.00→nan | 0.00→nan |
| cal_sci_cerebellum | as_written | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.98→1.00 | 0.00→1.00 | 0.00→1.00 |
| cal_sci_cerebellum | none | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 1.00→1.00 | 0.00→1.00 | 0.00→1.00 |
| cal_sci_glass | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.18 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_largest_desert | as_written | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.93→0.99 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_polar_bear_skin | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.01→0.52 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_polar_bear_skin | none | moves | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.88→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_tongue_map | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.00→0.92 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_tongue_map | none | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.08→1.00 | 0.00→0.00 | 0.00→0.00 |
| logic_modus_tollens | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.01 | 0.00→1.00 | 0.00→1.00 |
| logic_modus_tollens | none | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.15 | 0.00→0.00 | 0.00→0.00 |
| num_percent_round_trip | as_written | moves | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.05→0.42 | 0.00→0.00 | 0.00→0.00 |
| num_percent_round_trip | none | moves | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.03→0.76 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_belief_bias | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.97→0.95 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_belief_bias | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.87→0.86 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_conjunction | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→0.00 | 0.49→0.40 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_contrapositive | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.07→0.06 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_deny_antecedent | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.97→0.94 | 0.00→nan | 0.00→nan |
| cal_logic_deny_antecedent | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.99→0.96 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_wason | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.78→0.61 | 0.00→0.00 | 0.00→0.00 |
| cal_num_91_prime | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_average_speed | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→0.00 | 0.24→0.16 | 0.00→0.00 | 0.00→0.00 |
| cal_num_point_nine | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.91→0.85 | 0.00→0.00 | 0.00→0.00 |
| cal_num_powers | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.72→0.52 | 0.00→0.00 | 0.00→0.00 |
| cal_num_powers | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.95→0.66 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_closest_planet | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→0.00 | 0.98→0.14 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_closest_planet | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→0.00 | 0.94→0.18 | 1.00→1.00 | 1.00→1.00 |
| cal_sci_largest_desert | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→1.00 | 0.99→1.00 | 0.00→0.00 | 0.00→0.00 |
| logic_monty_hall | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 1.00→0.00 | 0.63→0.03 | 0.00→0.00 | 0.00→0.00 |
| num_base_rate | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.13→0.16 | 0.00→0.00 | 0.00→0.00 |
| num_birthday | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.01→0.01 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_all_some | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.03 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_all_some | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.03 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_contrapositive | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.04→0.05 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_gamblers | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_gamblers | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_91_prime | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_bats | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.02 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_bats | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_glass | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_affirm_consequent | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.01→0.02 | 0.00→0.00 | 0.00→0.00 |
| logic_affirm_consequent | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.02→0.04 | 0.00→0.00 | 0.00→0.00 |
| logic_monty_hall | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.78→0.08 | 0.00→0.00 | 0.00→0.00 |
| num_base_rate | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.14→0.04 | 0.00→0.00 | 0.00→0.00 |
| num_birthday | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_decimal_compare | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.01 | 0.00→0.00 | 0.00→0.00 |
| num_decimal_compare | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.04 | 0.00→0.00 | 0.00→0.00 |
| sci_falling_objects | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_falling_objects | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_great_wall_moon | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_great_wall_moon | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_lightning | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_lightning | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_seasons | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.01 | 0.00→0.00 | 0.00→nan |
| sci_seasons | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
