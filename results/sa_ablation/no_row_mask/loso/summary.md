# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.988 ± 0.008 |
| block | 0.50 | 0.987 ± 0.007 |
| block_shift | 0.30 | 0.985 ± 0.004 |
| block_shift | 0.50 | 0.981 ± 0.012 |
| none | 0.00 | 0.996 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.869 ± 0.024 |
| block | 0.50 | 0.845 ± 0.031 |
| block_shift | 0.30 | 0.851 ± 0.046 |
| block_shift | 0.50 | 0.811 ± 0.045 |
| none | 0.00 | 0.911 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.729 ± 0.039 |
| block | 0.50 | 0.701 ± 0.077 |
| block_shift | 0.30 | 0.698 ± 0.073 |
| block_shift | 0.50 | 0.676 ± 0.088 |
| none | 0.00 | 0.817 ± 0.023 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.994 ± 0.008 |
| block | 0.50 | 0.991 ± 0.010 |
| block_shift | 0.30 | 0.989 ± 0.009 |
| block_shift | 0.50 | 0.928 ± 0.059 |
| none | 0.00 | 1.000 ± 0.000 |
