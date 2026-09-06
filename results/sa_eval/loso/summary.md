# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.990 ± 0.005 | 0.983 ± 0.015 | 0.984 ± 0.013 | 0.986 ± 0.012 | 0.984 ± 0.014 |
| block | 0.50 | 0.989 ± 0.007 | 0.975 ± 0.016 | 0.968 ± 0.030 | 0.972 ± 0.022 | 0.967 ± 0.033 |
| block_shift | 0.30 | 0.986 ± 0.004 | 0.980 ± 0.006 | 0.982 ± 0.005 | 0.983 ± 0.005 | 0.983 ± 0.008 |
| block_shift | 0.50 | 0.984 ± 0.010 | 0.969 ± 0.022 | 0.963 ± 0.037 | 0.970 ± 0.021 | 0.960 ± 0.026 |
| none | 0.00 | 0.997 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 62.801 ± 2.781 | 63.938 ± 4.124 | 63.942 ± 3.954 | 63.718 ± 3.769 | 65.017 ± 5.421 |
| block | 0.50 | 63.990 ± 2.647 | 66.142 ± 5.227 | 66.360 ± 5.361 | 66.034 ± 4.307 | 66.960 ± 5.555 |
| block_shift | 0.30 | 66.684 ± 9.124 | 67.509 ± 10.011 | 67.577 ± 10.084 | 67.391 ± 10.182 | 60.953 ± 1.837 |
| block_shift | 0.50 | 65.152 ± 3.829 | 68.936 ± 5.409 | 69.102 ± 5.585 | 68.495 ± 5.349 | 69.508 ± 3.643 |
| none | 0.00 | 56.065 ± 3.550 | 55.789 ± 3.367 | 55.789 ± 3.367 | 55.789 ± 3.367 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.75 | 0.75 | 0.76 | 0.75 | 0.74 |
| block | 0.50 | 0.80 | 0.79 | 0.80 | 0.79 | 0.80 |
| block_shift | 0.30 | 0.71 | 0.73 | 0.74 | 0.74 | 0.80 |
| block_shift | 0.50 | 0.82 | 0.82 | 0.83 | 0.82 | 0.82 |
| none | 0.00 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.870 ± 0.027 | 0.869 ± 0.024 | 0.868 ± 0.026 | 0.871 ± 0.024 | 0.857 ± 0.032 |
| block | 0.50 | 0.847 ± 0.032 | 0.845 ± 0.030 | 0.847 ± 0.033 | 0.844 ± 0.035 | 0.841 ± 0.035 |
| block_shift | 0.30 | 0.851 ± 0.047 | 0.835 ± 0.059 | 0.832 ± 0.058 | 0.833 ± 0.060 | 0.870 ± 0.028 |
| block_shift | 0.50 | 0.810 ± 0.046 | 0.813 ± 0.049 | 0.800 ± 0.060 | 0.816 ± 0.045 | 0.813 ± 0.027 |
| none | 0.00 | 0.913 ± 0.003 | 0.912 ± 0.004 | 0.912 ± 0.004 | 0.912 ± 0.003 | 0.908 ± 0.006 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.727 ± 0.039 | 0.727 ± 0.047 | 0.728 ± 0.043 | 0.726 ± 0.041 | 0.719 ± 0.039 |
| block | 0.50 | 0.702 ± 0.082 | 0.706 ± 0.078 | 0.704 ± 0.084 | 0.705 ± 0.082 | 0.690 ± 0.090 |
| block_shift | 0.30 | 0.701 ± 0.068 | 0.699 ± 0.068 | 0.700 ± 0.067 | 0.698 ± 0.066 | 0.695 ± 0.070 |
| block_shift | 0.50 | 0.683 ± 0.086 | 0.680 ± 0.076 | 0.683 ± 0.080 | 0.677 ± 0.088 | 0.680 ± 0.094 |
| none | 0.00 | 0.817 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 5.325 ± 0.773 | 5.510 ± 1.077 | 5.537 ± 1.193 | 5.504 ± 1.147 | 6.218 ± 1.139 |
| block | 0.50 | 5.477 ± 0.738 | 6.047 ± 0.727 | 5.840 ± 0.690 | 5.837 ± 0.657 | 6.149 ± 0.852 |
| block_shift | 0.30 | 5.869 ± 0.618 | 6.349 ± 0.852 | 6.617 ± 1.083 | 6.566 ± 1.054 | 5.813 ± 1.186 |
| block_shift | 0.50 | 6.721 ± 1.095 | 6.999 ± 0.950 | 7.076 ± 0.633 | 7.161 ± 0.848 | 6.879 ± 1.297 |
| none | 0.00 | 2.730 ± 0.500 | 2.712 ± 0.497 | 2.712 ± 0.497 | 2.712 ± 0.497 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.73 | 0.76 | 0.77 | 0.77 | 0.79 |
| block | 0.50 | 0.80 | 0.84 | 0.87 | 0.89 | 0.88 |
| block_shift | 0.30 | 0.75 | 0.79 | 0.80 | 0.80 | 0.82 |
| block_shift | 0.50 | 0.81 | 0.87 | 0.87 | 0.86 | 0.82 |
| none | 0.00 | 0.79 | 0.80 | 0.80 | 0.80 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute | tabicl_indicator | tabicl_patternnorm |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.996 ± 0.004 | 0.977 ± 0.042 | 0.980 ± 0.038 | 0.979 ± 0.039 | 0.971 ± 0.054 |
| block | 0.50 | 0.992 ± 0.008 | 0.989 ± 0.011 | 0.990 ± 0.011 | 0.990 ± 0.007 | 0.988 ± 0.012 |
| block_shift | 0.30 | 0.989 ± 0.008 | 0.989 ± 0.008 | 0.989 ± 0.008 | 0.989 ± 0.009 | 0.992 ± 0.008 |
| block_shift | 0.50 | 0.932 ± 0.055 | 0.905 ± 0.061 | 0.914 ± 0.062 | 0.923 ± 0.045 | 0.971 ± 0.032 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |
