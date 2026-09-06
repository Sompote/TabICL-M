# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.989 ± 0.006 |
| block | 0.50 | 0.988 ± 0.007 |
| block_shift | 0.30 | 0.985 ± 0.005 |
| block_shift | 0.50 | 0.983 ± 0.009 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.868 ± 0.025 |
| block | 0.50 | 0.845 ± 0.033 |
| block_shift | 0.30 | 0.849 ± 0.048 |
| block_shift | 0.50 | 0.810 ± 0.043 |
| none | 0.00 | 0.912 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.726 ± 0.043 |
| block | 0.50 | 0.702 ± 0.080 |
| block_shift | 0.30 | 0.701 ± 0.066 |
| block_shift | 0.50 | 0.679 ± 0.090 |
| none | 0.00 | 0.817 ± 0.024 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.993 ± 0.009 |
| block | 0.50 | 0.992 ± 0.008 |
| block_shift | 0.30 | 0.989 ± 0.009 |
| block_shift | 0.50 | 0.924 ± 0.058 |
| none | 0.00 | 1.000 ± 0.000 |
