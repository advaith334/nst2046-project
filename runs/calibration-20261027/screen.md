# Item screen

Each cell: share choosing the incorrect-belief option, `no_belief` → `stored_incorrect`. `p` columns: mean probability on that option (Qwen only). Verdicts: **moves** = the stored belief raised the incorrect choice or its probability by ≥0.05; **hard, no shift** = some model misses it at baseline but memory doesn't move it; **ceiling** = every model always right.

Counts: ceiling: 35, hard, no shift: 28, moves: 6

| case_id | evidence_mode | verdict | claude-sonnet base→stored | llama-8b base→stored | qwen-large base→stored | qwen-large p |
|---|---|---|---|---|---|---|
| cal_logic_conjunction | none | moves | 0.00→0.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_overlap | as_written | moves | 0.00→0.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_overlap | none | moves | 0.00→0.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_wason | as_written | moves | 0.00→0.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_digit_ones | none | moves | 0.00→0.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_point_nine | as_written | moves | 0.00→0.00 | 0.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_belief_bias | as_written | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_belief_bias | none | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_conjunction | as_written | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_contrapositive | as_written | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_deny_antecedent | as_written | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_deny_antecedent | none | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_wason | none | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_average_speed | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_average_speed | none | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_bat_ball | as_written | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_lily_pads | as_written | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_lily_pads | none | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_powers | as_written | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_powers | none | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_two_children | as_written | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_two_children | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_cerebellum | as_written | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_cerebellum | none | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_closest_planet | as_written | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_polar_bear_skin | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_polar_bear_skin | none | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_tongue_map | as_written | hard, no shift | 0.00→0.00 | 1.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_tongue_map | none | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| num_base_rate | as_written | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_base_rate | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_birthday | none | hard, no shift | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_decimal_compare | as_written | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| num_decimal_compare | none | hard, no shift | 0.00→0.00 | 1.00→1.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_all_some | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_all_some | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_contrapositive | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_gamblers | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_logic_gamblers | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_91_prime | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_91_prime | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_digit_ones | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_num_point_nine | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_base_to_peak | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_base_to_peak | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_bats | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_bats | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_closest_planet | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_glass | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_glass | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_largest_desert | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| cal_sci_largest_desert | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_affirm_consequent | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_affirm_consequent | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_modus_tollens | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_modus_tollens | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_monty_hall | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| logic_monty_hall | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_birthday | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_percent_round_trip | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| num_percent_round_trip | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_falling_objects | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_falling_objects | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_great_wall_moon | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_great_wall_moon | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_lightning | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_lightning | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_seasons | as_written | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
| sci_seasons | none | ceiling | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 |
