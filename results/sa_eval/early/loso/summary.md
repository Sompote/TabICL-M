# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.991 ± 0.002 | 0.991 ± 0.004 |
| block | 0.50 | 0.990 ± 0.005 | 0.956 ± 0.034 |
| block_shift | 0.30 | 0.985 ± 0.005 | 0.983 ± 0.007 |
| block_shift | 0.50 | 0.983 ± 0.006 | 0.974 ± 0.003 |
| none | 0.00 | 0.996 ± 0.003 | 0.996 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.878 ± 0.018 | 0.873 ± 0.022 |
| block | 0.50 | 0.864 ± 0.032 | 0.863 ± 0.034 |
| block_shift | 0.30 | 0.856 ± 0.060 | 0.841 ± 0.075 |
| block_shift | 0.50 | 0.791 ± 0.052 | 0.798 ± 0.060 |
| none | 0.00 | 0.912 ± 0.004 | 0.912 ± 0.005 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.744 ± 0.016 | 0.748 ± 0.007 |
| block | 0.50 | 0.655 ± 0.014 | 0.656 ± 0.019 |
| block_shift | 0.30 | 0.666 ± 0.067 | 0.668 ± 0.071 |
| block_shift | 0.50 | 0.644 ± 0.021 | 0.650 ± 0.017 |
| none | 0.00 | 0.831 ± 0.009 | 0.828 ± 0.007 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.999 ± 0.001 | 0.999 ± 0.001 |
| block | 0.50 | 0.992 ± 0.007 | 0.988 ± 0.013 |
| block_shift | 0.30 | 0.986 ± 0.008 | 0.986 ± 0.010 |
| block_shift | 0.50 | 0.946 ± 0.043 | 0.927 ± 0.055 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 |
