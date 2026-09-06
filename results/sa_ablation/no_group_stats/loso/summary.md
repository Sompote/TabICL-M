# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.989 ± 0.006 |
| block | 0.50 | 0.988 ± 0.007 |
| block_shift | 0.30 | 0.984 ± 0.005 |
| block_shift | 0.50 | 0.983 ± 0.010 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.869 ± 0.025 |
| block | 0.50 | 0.845 ± 0.033 |
| block_shift | 0.30 | 0.850 ± 0.047 |
| block_shift | 0.50 | 0.810 ± 0.044 |
| none | 0.00 | 0.912 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.729 ± 0.040 |
| block | 0.50 | 0.701 ± 0.081 |
| block_shift | 0.30 | 0.702 ± 0.069 |
| block_shift | 0.50 | 0.680 ± 0.089 |
| none | 0.00 | 0.818 ± 0.023 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.995 ± 0.006 |
| block | 0.50 | 0.992 ± 0.007 |
| block_shift | 0.30 | 0.989 ± 0.008 |
| block_shift | 0.50 | 0.929 ± 0.052 |
| none | 0.00 | 1.000 ± 0.000 |
