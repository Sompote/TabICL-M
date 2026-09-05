# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.996 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.994 ± 0.006 |
| none | 0.00 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 59.606 ± 2.558 |
| block | 0.50 | 65.462 ± 3.633 |
| block_shift | 0.30 | 58.910 ± 1.076 |
| block_shift | 0.50 | 65.212 ± 1.961 |
| none | 0.00 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.79 |
| block | 0.50 | 0.78 |
| block_shift | 0.30 | 0.80 |
| block_shift | 0.50 | 0.78 |
| none | 0.00 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.895 ± 0.013 |
| block | 0.50 | 0.864 ± 0.010 |
| block_shift | 0.30 | 0.894 ± 0.006 |
| block_shift | 0.50 | 0.857 ± 0.029 |
| none | 0.00 | 0.908 ± 0.006 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.763 ± 0.051 |
| block | 0.50 | 0.726 ± 0.035 |
| block_shift | 0.30 | 0.766 ± 0.028 |
| block_shift | 0.50 | 0.726 ± 0.028 |
| none | 0.00 | 0.814 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 3.689 ± 0.517 |
| block | 0.50 | 4.838 ± 0.554 |
| block_shift | 0.30 | 4.354 ± 0.625 |
| block_shift | 0.50 | 4.760 ± 0.840 |
| none | 0.00 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.81 |
| block | 0.50 | 0.77 |
| block_shift | 0.30 | 0.80 |
| block_shift | 0.50 | 0.78 |
| none | 0.00 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_patternnorm |
|---|---|---|
| block | 0.30 | 0.997 ± 0.005 |
| block | 0.50 | 0.995 ± 0.008 |
| block_shift | 0.30 | 0.996 ± 0.005 |
| block_shift | 0.50 | 0.989 ± 0.024 |
| none | 0.00 | 1.000 ± 0.000 |
