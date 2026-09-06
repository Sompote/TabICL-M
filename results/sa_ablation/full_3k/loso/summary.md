# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.989 ± 0.006 |
| block | 0.50 | 0.989 ± 0.007 |
| block_shift | 0.30 | 0.985 ± 0.005 |
| block_shift | 0.50 | 0.983 ± 0.010 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.869 ± 0.025 |
| block | 0.50 | 0.845 ± 0.033 |
| block_shift | 0.30 | 0.849 ± 0.047 |
| block_shift | 0.50 | 0.810 ± 0.044 |
| none | 0.00 | 0.911 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.727 ± 0.043 |
| block | 0.50 | 0.703 ± 0.081 |
| block_shift | 0.30 | 0.703 ± 0.067 |
| block_shift | 0.50 | 0.682 ± 0.090 |
| none | 0.00 | 0.818 ± 0.024 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.994 ± 0.007 |
| block | 0.50 | 0.992 ± 0.007 |
| block_shift | 0.30 | 0.989 ± 0.009 |
| block_shift | 0.50 | 0.929 ± 0.056 |
| none | 0.00 | 1.000 ± 0.000 |
