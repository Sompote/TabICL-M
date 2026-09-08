# Regression ablation of the source-aware parts

Regressor, 3000 steps each from the released TabICLv2 regressor on the source-aware prior, one switch off at a time; seven regression datasets, block and block_shift at 0.3 / 0.5, 5 seeds. Lower RMSE is better; positive % = the variant is better than the reference. `full_20k` is the main 20k-step checkpoint (10k + stage 4b).

- `full_3k`: all parts on
- `no_group_stats`: without col_group_stats
- `no_row_mask`: without row_missing_aware
- `no_pattern_token`: without pattern_token
- `no_objectives`: cell reconstruction, no consistency loss
- `arch_off`: all parts off, new prior only

## Leave-one-source-out, complete data (base strength): 35 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `tabpfn3` | 4.54 | 23/12, +2.85 % | — |
| `full_3k` | 5.09 | 17/18, +1.00 % | 15/20, -2.10 % |
| `arch_off` | 5.14 | 17/18, +0.17 % | 14/21, -2.91 % |
| `tabicl_impute` | 5.57 | — | 12/23, -3.24 % |
| `no_row_mask` | 5.69 | 16/19, +0.47 % | 14/21, -2.61 % |
| `no_objectives` | 5.71 | 17/18, +0.39 % | 12/23, -2.73 % |
| `no_group_stats` | 5.83 | 17/18, +0.17 % | 14/21, -2.97 % |
| `no_pattern_token` | 6.00 | 17/18, +0.29 % | 13/22, -2.87 % |
| `full_20k` | 6.29 | 17/18, +0.68 % | 14/21, -2.52 % |
| `tabpfn25` | 7.03 | 13/22, -1.61 % | 9/26, -5.18 % |
| `catboost` | 9.11 | 6/29, -13.91 % | 7/28, -18.75 % |

## Leave-one-source-out, held-out source with offset: 70 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `full_20k` | 3.29 | 59/11, +8.55 % | 44/26, +2.53 % |
| `tabpfn3` | 5.07 | 48/22, +5.43 % | — |
| `no_objectives` | 5.39 | 55/15, +5.08 % | 32/38, -1.39 % |
| `full_3k` | 5.47 | 53/17, +5.11 % | 31/39, -1.31 % |
| `no_pattern_token` | 5.47 | 53/17, +5.27 % | 32/38, -1.07 % |
| `no_group_stats` | 5.83 | 53/17, +4.87 % | 31/39, -1.51 % |
| `tabpfn25` | 5.83 | 50/20, +4.78 % | 33/37, -2.07 % |
| `no_row_mask` | 5.94 | 55/15, +4.82 % | 26/44, -1.85 % |
| `arch_off` | 6.03 | 56/14, +4.51 % | 26/44, -2.37 % |
| `tabicl_impute` | 8.09 | — | 22/48, -8.82 % |
| `catboost` | 9.60 | 14/56, -21.18 % | 8/62, -29.81 % |

## Leave-one-source-out, block without offset: 70 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `tabpfn3` | 3.26 | 60/10, +12.77 % | — |
| `full_20k` | 4.79 | 52/18, +6.15 % | 23/47, -9.31 % |
| `no_pattern_token` | 5.17 | 54/16, +7.46 % | 17/53, -9.27 % |
| `tabpfn25` | 5.30 | 49/21, +2.65 % | 18/52, -15.33 % |
| `full_3k` | 5.63 | 53/17, +6.59 % | 18/52, -9.87 % |
| `arch_off` | 5.66 | 55/15, +6.42 % | 20/50, -10.75 % |
| `no_row_mask` | 5.79 | 54/16, +6.74 % | 17/53, -10.11 % |
| `no_group_stats` | 5.80 | 56/14, +6.08 % | 17/53, -10.77 % |
| `no_objectives` | 5.89 | 54/16, +6.53 % | 17/53, -10.47 % |
| `tabicl_impute` | 8.03 | — | 10/60, -22.65 % |
| `catboost` | 10.70 | 5/65, -40.60 % | 1/69, -66.73 % |

## Leave-one-source-out, all incomplete conditions: 140 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `full_20k` | 4.04 | 111/29, +7.35 % | 67/73, -3.39 % |
| `tabpfn3` | 4.16 | 108/32, +9.10 % | — |
| `no_pattern_token` | 5.32 | 107/33, +6.37 % | 49/91, -5.17 % |
| `full_3k` | 5.55 | 106/34, +5.85 % | 49/91, -5.59 % |
| `tabpfn25` | 5.56 | 99/41, +3.71 % | 51/89, -8.70 % |
| `no_objectives` | 5.64 | 109/31, +5.81 % | 49/91, -5.93 % |
| `no_group_stats` | 5.81 | 109/31, +5.48 % | 48/92, -6.14 % |
| `arch_off` | 5.84 | 111/29, +5.46 % | 46/94, -6.56 % |
| `no_row_mask` | 5.86 | 109/31, +5.78 % | 43/97, -5.98 % |
| `tabicl_impute` | 8.06 | — | 32/108, -15.73 % |
| `catboost` | 10.15 | 19/121, -30.89 % | 9/131, -48.27 % |

## Random split, complete data (base strength): 35 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `tabpfn3` | 4.54 | 23/12, +2.85 % | — |
| `full_3k` | 5.09 | 17/18, +1.00 % | 15/20, -2.10 % |
| `arch_off` | 5.14 | 17/18, +0.17 % | 14/21, -2.91 % |
| `tabicl_impute` | 5.57 | — | 12/23, -3.24 % |
| `no_row_mask` | 5.69 | 16/19, +0.47 % | 14/21, -2.61 % |
| `no_objectives` | 5.71 | 17/18, +0.39 % | 12/23, -2.73 % |
| `no_group_stats` | 5.83 | 17/18, +0.17 % | 14/21, -2.97 % |
| `no_pattern_token` | 6.00 | 17/18, +0.29 % | 13/22, -2.87 % |
| `full_20k` | 6.29 | 17/18, +0.68 % | 14/21, -2.52 % |
| `tabpfn25` | 7.03 | 13/22, -1.61 % | 9/26, -5.18 % |
| `catboost` | 9.11 | 6/29, -13.91 % | 7/28, -18.75 % |

## Random split, block without offset: 70 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `tabpfn3` | 3.69 | 54/16, +1.12 % | — |
| `no_group_stats` | 5.33 | 42/28, +0.48 % | 24/46, -0.73 % |
| `full_20k` | 5.71 | 33/37, +0.40 % | 20/50, -0.81 % |
| `no_row_mask` | 5.73 | 43/27, +0.37 % | 22/48, -0.85 % |
| `no_objectives` | 5.74 | 35/35, +0.38 % | 20/50, -0.83 % |
| `full_3k` | 5.76 | 39/31, +0.47 % | 22/48, -0.74 % |
| `no_pattern_token` | 5.79 | 37/33, +0.38 % | 23/47, -0.83 % |
| `arch_off` | 5.84 | 38/32, +0.30 % | 20/50, -0.91 % |
| `tabpfn25` | 5.90 | 41/29, -1.83 % | 17/53, -2.76 % |
| `tabicl_impute` | 6.27 | — | 16/54, -1.23 % |
| `catboost` | 10.24 | 7/63, -5.37 % | 4/66, -6.63 % |

## Random split, all incomplete conditions: 140 conditions

| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |
|---|---|---|---|
| `tabpfn3` | 3.32 | 112/28, +1.42 % | — |
| `tabpfn25` | 5.34 | 82/58, -0.56 % | 33/107, -1.92 % |
| `full_20k` | 5.39 | 70/70, +0.41 % | 42/98, -1.08 % |
| `no_group_stats` | 5.54 | 79/61, +0.32 % | 39/101, -1.18 % |
| `full_3k` | 5.81 | 73/67, +0.33 % | 37/103, -1.16 % |
| `no_objectives` | 5.93 | 70/70, +0.22 % | 32/108, -1.28 % |
| `no_pattern_token` | 5.96 | 73/67, +0.27 % | 38/102, -1.23 % |
| `no_row_mask` | 6.04 | 76/64, +0.21 % | 37/103, -1.29 % |
| `tabicl_impute` | 6.18 | — | 28/112, -1.52 % |
| `arch_off` | 6.18 | 74/66, +0.12 % | 32/108, -1.38 % |
| `catboost` | 10.32 | 16/124, -5.33 % | 7/133, -6.92 % |
