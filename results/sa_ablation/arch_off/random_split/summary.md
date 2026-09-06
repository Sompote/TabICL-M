# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.996 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.995 ± 0.004 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.899 ± 0.014 |
| block | 0.50 | 0.868 ± 0.010 |
| block_shift | 0.30 | 0.895 ± 0.004 |
| block_shift | 0.50 | 0.860 ± 0.026 |
| none | 0.00 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.770 ± 0.053 |
| block | 0.50 | 0.723 ± 0.032 |
| block_shift | 0.30 | 0.770 ± 0.032 |
| block_shift | 0.50 | 0.728 ± 0.031 |
| none | 0.00 | 0.816 ± 0.023 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.999 ± 0.003 |
| block | 0.50 | 0.995 ± 0.006 |
| block_shift | 0.30 | 0.995 ± 0.006 |
| block_shift | 0.50 | 0.989 ± 0.023 |
| none | 0.00 | 1.000 ± 0.000 |
