# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.995 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.994 ± 0.005 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.899 ± 0.014 |
| block | 0.50 | 0.867 ± 0.010 |
| block_shift | 0.30 | 0.896 ± 0.003 |
| block_shift | 0.50 | 0.860 ± 0.026 |
| none | 0.00 | 0.912 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.771 ± 0.052 |
| block | 0.50 | 0.723 ± 0.034 |
| block_shift | 0.30 | 0.771 ± 0.032 |
| block_shift | 0.50 | 0.726 ± 0.032 |
| none | 0.00 | 0.817 ± 0.024 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.999 ± 0.003 |
| block | 0.50 | 0.996 ± 0.005 |
| block_shift | 0.30 | 0.995 ± 0.006 |
| block_shift | 0.50 | 0.989 ± 0.022 |
| none | 0.00 | 1.000 ± 0.000 |
