# Wrapper test fixes-20261105

Incorrect-option rate by wording. Total cost $0.042.

| variant | model | no_belief | stored_incorrect | stored_incorrect_labelled | stored_correct | useful_label_off | useful_label_on |
|---|---|---|---|---|---|---|---|
| tutor | mistral-nemo | 0.16 | 0.24 | 0.24 | 0.15 | 0.00 | 0.00 |
| tutor | mistral-small | 0.04 | 0.07 | 0.10 | 0.05 | 0.00 | 0.00 |
| rule | mistral-nemo |  | 0.49 |  | 0.07 | 0.00 | 0.00 |
| rule | mistral-small |  | 0.22 |  | 0.02 | 0.00 | 0.00 |
| answer_first | mistral-nemo |  | 0.47 |  | 0.07 | 0.00 | 0.00 |
| answer_first | mistral-small |  | 0.08 |  | 0.02 | 0.00 | 0.00 |
| memory_gate | mistral-nemo |  | 0.17 |  | 0.16 | 0.00 | 0.00 |
| memory_gate | mistral-small |  | 0.03 |  | 0.05 | 0.00 | 0.00 |
