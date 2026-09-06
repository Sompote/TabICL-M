# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.995 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.995 ± 0.005 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.899 ± 0.014 |
| block | 0.50 | 0.867 ± 0.009 |
| block_shift | 0.30 | 0.895 ± 0.004 |
| block_shift | 0.50 | 0.859 ± 0.026 |
| none | 0.00 | 0.911 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.771 ± 0.054 |
| block | 0.50 | 0.722 ± 0.035 |
| block_shift | 0.30 | 0.772 ± 0.033 |
| block_shift | 0.50 | 0.726 ± 0.033 |
| none | 0.00 | 0.818 ± 0.024 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.999 ± 0.003 |
| block | 0.50 | 0.996 ± 0.004 |
| block_shift | 0.30 | 0.996 ± 0.006 |
| block_shift | 0.50 | 0.988 ± 0.023 |
| none | 0.00 | 1.000 ± 0.000 |
