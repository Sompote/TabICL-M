# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.988 ± 0.010 |
| block | 0.50 | 0.986 ± 0.008 |
| block_shift | 0.30 | 0.985 ± 0.005 |
| block_shift | 0.50 | 0.981 ± 0.012 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.868 ± 0.026 |
| block | 0.50 | 0.844 ± 0.031 |
| block_shift | 0.30 | 0.850 ± 0.045 |
| block_shift | 0.50 | 0.808 ± 0.046 |
| none | 0.00 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.728 ± 0.042 |
| block | 0.50 | 0.703 ± 0.076 |
| block_shift | 0.30 | 0.697 ± 0.070 |
| block_shift | 0.50 | 0.673 ± 0.092 |
| none | 0.00 | 0.816 ± 0.023 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.992 ± 0.009 |
| block | 0.50 | 0.991 ± 0.009 |
| block_shift | 0.30 | 0.989 ± 0.009 |
| block_shift | 0.50 | 0.921 ± 0.059 |
| none | 0.00 | 1.000 ± 0.000 |
