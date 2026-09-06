# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.997 ± 0.003 | 0.997 ± 0.003 | 0.997 ± 0.003 | 0.997 ± 0.003 | 0.997 ± 0.003 |
| block | 0.50 | 0.996 ± 0.004 | 0.995 ± 0.004 | 0.995 ± 0.004 | 0.996 ± 0.004 | 0.996 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.004 | 0.994 ± 0.004 | 0.994 ± 0.003 | 0.994 ± 0.004 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.994 ± 0.005 | 0.994 ± 0.005 | 0.994 ± 0.005 | 0.994 ± 0.005 | 0.994 ± 0.006 |
| none | 0.00 | 0.997 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 59.024 ± 2.862 | 59.176 ± 3.079 | 59.326 ± 2.991 | 59.280 ± 2.725 | 59.606 ± 2.558 |
| block | 0.50 | 64.761 ± 3.944 | 65.119 ± 3.669 | 65.344 ± 3.639 | 65.374 ± 3.593 | 65.462 ± 3.633 |
| block_shift | 0.30 | 59.062 ± 0.767 | 59.094 ± 1.293 | 59.288 ± 1.304 | 59.099 ± 1.253 | 58.910 ± 1.076 |
| block_shift | 0.50 | 64.227 ± 3.110 | 65.063 ± 2.137 | 64.778 ± 2.812 | 64.668 ± 2.676 | 65.212 ± 1.961 |
| none | 0.00 | 56.065 ± 3.550 | 55.789 ± 3.367 | 55.789 ± 3.367 | 55.789 ± 3.367 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.79 | 0.79 | 0.79 | 0.80 | 0.79 |
| block | 0.50 | 0.77 | 0.78 | 0.78 | 0.79 | 0.78 |
| block_shift | 0.30 | 0.80 | 0.79 | 0.80 | 0.80 | 0.80 |
| block_shift | 0.50 | 0.78 | 0.76 | 0.78 | 0.78 | 0.78 |
| none | 0.00 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.900 ± 0.014 | 0.901 ± 0.013 | 0.900 ± 0.013 | 0.897 ± 0.014 | 0.895 ± 0.013 |
| block | 0.50 | 0.869 ± 0.010 | 0.866 ± 0.010 | 0.865 ± 0.009 | 0.851 ± 0.016 | 0.864 ± 0.010 |
| block_shift | 0.30 | 0.896 ± 0.003 | 0.894 ± 0.003 | 0.894 ± 0.004 | 0.891 ± 0.006 | 0.894 ± 0.006 |
| block_shift | 0.50 | 0.860 ± 0.025 | 0.859 ± 0.028 | 0.859 ± 0.028 | 0.838 ± 0.030 | 0.857 ± 0.029 |
| none | 0.00 | 0.913 ± 0.003 | 0.912 ± 0.004 | 0.912 ± 0.004 | 0.912 ± 0.003 | 0.908 ± 0.006 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.772 ± 0.053 | 0.768 ± 0.052 | 0.769 ± 0.050 | 0.768 ± 0.051 | 0.763 ± 0.051 |
| block | 0.50 | 0.721 ± 0.035 | 0.721 ± 0.034 | 0.722 ± 0.034 | 0.723 ± 0.037 | 0.726 ± 0.035 |
| block_shift | 0.30 | 0.770 ± 0.034 | 0.768 ± 0.032 | 0.769 ± 0.034 | 0.769 ± 0.032 | 0.766 ± 0.028 |
| block_shift | 0.50 | 0.725 ± 0.033 | 0.726 ± 0.029 | 0.727 ± 0.028 | 0.727 ± 0.028 | 0.726 ± 0.028 |
| none | 0.00 | 0.817 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 3.614 ± 0.425 | 3.646 ± 0.544 | 3.729 ± 0.543 | 3.736 ± 0.561 | 3.689 ± 0.517 |
| block | 0.50 | 4.790 ± 0.639 | 4.825 ± 0.583 | 4.842 ± 0.554 | 4.860 ± 0.556 | 4.838 ± 0.554 |
| block_shift | 0.30 | 4.390 ± 0.568 | 4.356 ± 0.602 | 4.380 ± 0.594 | 4.370 ± 0.592 | 4.354 ± 0.625 |
| block_shift | 0.50 | 4.655 ± 0.858 | 4.672 ± 0.834 | 4.700 ± 0.889 | 4.663 ± 0.917 | 4.760 ± 0.840 |
| none | 0.00 | 2.730 ± 0.500 | 2.712 ± 0.497 | 2.712 ± 0.497 | 2.712 ± 0.497 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.80 | 0.80 | 0.80 | 0.81 | 0.81 |
| block | 0.50 | 0.76 | 0.76 | 0.76 | 0.75 | 0.77 |
| block_shift | 0.30 | 0.81 | 0.82 | 0.81 | 0.81 | 0.80 |
| block_shift | 0.50 | 0.76 | 0.77 | 0.78 | 0.78 | 0.78 |
| none | 0.00 | 0.79 | 0.80 | 0.80 | 0.80 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.999 ± 0.003 | 0.997 ± 0.004 | 0.997 ± 0.005 | 0.997 ± 0.004 | 0.997 ± 0.005 |
| block | 0.50 | 0.996 ± 0.004 | 0.997 ± 0.006 | 0.996 ± 0.006 | 0.996 ± 0.005 | 0.995 ± 0.008 |
| block_shift | 0.30 | 0.996 ± 0.005 | 0.996 ± 0.005 | 0.996 ± 0.004 | 0.996 ± 0.005 | 0.996 ± 0.005 |
| block_shift | 0.50 | 0.989 ± 0.022 | 0.989 ± 0.022 | 0.989 ± 0.024 | 0.988 ± 0.024 | 0.989 ± 0.024 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |
