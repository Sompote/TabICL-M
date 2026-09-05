# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.984 ± 0.014 |
| block | 0.50 | 0.967 ± 0.033 |
| block_shift | 0.30 | 0.983 ± 0.008 |
| block_shift | 0.50 | 0.960 ± 0.026 |
| none | 0.00 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 65.017 ± 5.421 |
| block | 0.50 | 66.960 ± 5.555 |
| block_shift | 0.30 | 60.953 ± 1.837 |
| block_shift | 0.50 | 69.508 ± 3.643 |
| none | 0.00 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.74 |
| block | 0.50 | 0.80 |
| block_shift | 0.30 | 0.80 |
| block_shift | 0.50 | 0.82 |
| none | 0.00 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.857 ± 0.032 |
| block | 0.50 | 0.841 ± 0.035 |
| block_shift | 0.30 | 0.870 ± 0.028 |
| block_shift | 0.50 | 0.813 ± 0.027 |
| none | 0.00 | 0.908 ± 0.006 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.719 ± 0.039 |
| block | 0.50 | 0.690 ± 0.090 |
| block_shift | 0.30 | 0.695 ± 0.070 |
| block_shift | 0.50 | 0.680 ± 0.094 |
| none | 0.00 | 0.814 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 6.218 ± 1.139 |
| block | 0.50 | 6.149 ± 0.852 |
| block_shift | 0.30 | 5.813 ± 1.186 |
| block_shift | 0.50 | 6.879 ± 1.297 |
| none | 0.00 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.79 |
| block | 0.50 | 0.88 |
| block_shift | 0.30 | 0.82 |
| block_shift | 0.50 | 0.82 |
| none | 0.00 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.971 ± 0.054 |
| block | 0.50 | 0.988 ± 0.012 |
| block_shift | 0.30 | 0.992 ± 0.008 |
| block_shift | 0.50 | 0.971 ± 0.032 |
| none | 0.00 | 1.000 ± 0.000 |
