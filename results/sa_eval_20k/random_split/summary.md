# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.997 ± 0.003 | 0.997 ± 0.003 | 0.997 ± 0.003 |
| block | 0.50 | 0.995 ± 0.003 | 0.995 ± 0.004 | 0.995 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.004 | 0.994 ± 0.004 | 0.994 ± 0.003 |
| block_shift | 0.50 | 0.994 ± 0.005 | 0.994 ± 0.005 | 0.994 ± 0.005 |
| none | 0.00 | 0.997 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 59.114 ± 2.843 | 59.176 ± 3.079 | 59.326 ± 2.991 |
| block | 0.50 | 64.716 ± 3.998 | 65.119 ± 3.669 | 65.344 ± 3.639 |
| block_shift | 0.30 | 58.938 ± 0.711 | 59.094 ± 1.293 | 59.288 ± 1.304 |
| block_shift | 0.50 | 64.148 ± 3.378 | 65.063 ± 2.137 | 64.778 ± 2.812 |
| none | 0.00 | 56.017 ± 3.526 | 55.789 ± 3.367 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.78 | 0.79 | 0.79 |
| block | 0.50 | 0.76 | 0.78 | 0.78 |
| block_shift | 0.30 | 0.79 | 0.79 | 0.80 |
| block_shift | 0.50 | 0.77 | 0.76 | 0.78 |
| none | 0.00 | 0.78 | 0.78 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.900 ± 0.014 | 0.901 ± 0.013 | 0.900 ± 0.013 |
| block | 0.50 | 0.869 ± 0.010 | 0.866 ± 0.010 | 0.865 ± 0.009 |
| block_shift | 0.30 | 0.897 ± 0.002 | 0.894 ± 0.003 | 0.894 ± 0.004 |
| block_shift | 0.50 | 0.860 ± 0.025 | 0.859 ± 0.028 | 0.859 ± 0.028 |
| none | 0.00 | 0.913 ± 0.003 | 0.912 ± 0.004 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.774 ± 0.053 | 0.768 ± 0.052 | 0.769 ± 0.050 |
| block | 0.50 | 0.722 ± 0.033 | 0.721 ± 0.034 | 0.722 ± 0.034 |
| block_shift | 0.30 | 0.769 ± 0.033 | 0.768 ± 0.032 | 0.769 ± 0.034 |
| block_shift | 0.50 | 0.725 ± 0.033 | 0.726 ± 0.029 | 0.727 ± 0.028 |
| none | 0.00 | 0.817 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 3.653 ± 0.496 | 3.646 ± 0.544 | 3.729 ± 0.543 |
| block | 0.50 | 4.770 ± 0.649 | 4.825 ± 0.583 | 4.842 ± 0.554 |
| block_shift | 0.30 | 4.369 ± 0.620 | 4.356 ± 0.602 | 4.380 ± 0.594 |
| block_shift | 0.50 | 4.616 ± 0.840 | 4.672 ± 0.834 | 4.700 ± 0.889 |
| none | 0.00 | 2.697 ± 0.477 | 2.712 ± 0.497 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.79 | 0.80 | 0.80 |
| block | 0.50 | 0.76 | 0.76 | 0.76 |
| block_shift | 0.30 | 0.80 | 0.82 | 0.81 |
| block_shift | 0.50 | 0.76 | 0.77 | 0.78 |
| none | 0.00 | 0.77 | 0.80 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.999 ± 0.003 | 0.997 ± 0.004 | 0.997 ± 0.005 |
| block | 0.50 | 0.996 ± 0.004 | 0.997 ± 0.006 | 0.996 ± 0.006 |
| block_shift | 0.30 | 0.996 ± 0.005 | 0.996 ± 0.005 | 0.996 ± 0.004 |
| block_shift | 0.50 | 0.988 ± 0.024 | 0.989 ± 0.022 | 0.989 ± 0.024 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |
