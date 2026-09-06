# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.989 ± 0.006 |
| block | 0.50 | 0.989 ± 0.007 |
| block_shift | 0.30 | 0.985 ± 0.005 |
| block_shift | 0.50 | 0.982 ± 0.010 |
| none | 0.00 | 0.996 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.869 ± 0.025 |
| block | 0.50 | 0.846 ± 0.032 |
| block_shift | 0.30 | 0.849 ± 0.047 |
| block_shift | 0.50 | 0.811 ± 0.043 |
| none | 0.00 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.727 ± 0.041 |
| block | 0.50 | 0.701 ± 0.083 |
| block_shift | 0.30 | 0.701 ± 0.069 |
| block_shift | 0.50 | 0.679 ± 0.089 |
| none | 0.00 | 0.818 ± 0.022 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.994 ± 0.007 |
| block | 0.50 | 0.992 ± 0.007 |
| block_shift | 0.30 | 0.989 ± 0.009 |
| block_shift | 0.50 | 0.926 ± 0.057 |
| none | 0.00 | 1.000 ± 0.000 |
