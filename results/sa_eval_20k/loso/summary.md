# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.990 ± 0.005 | 0.983 ± 0.015 | 0.984 ± 0.013 |
| block | 0.50 | 0.989 ± 0.007 | 0.975 ± 0.016 | 0.968 ± 0.030 |
| block_shift | 0.30 | 0.986 ± 0.003 | 0.980 ± 0.006 | 0.982 ± 0.005 |
| block_shift | 0.50 | 0.985 ± 0.010 | 0.969 ± 0.022 | 0.963 ± 0.037 |
| none | 0.00 | 0.997 ± 0.003 | 0.996 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 62.626 ± 2.835 | 63.938 ± 4.124 | 63.942 ± 3.954 |
| block | 0.50 | 64.111 ± 2.602 | 66.142 ± 5.227 | 66.360 ± 5.361 |
| block_shift | 0.30 | 65.879 ± 8.590 | 67.509 ± 10.011 | 67.577 ± 10.084 |
| block_shift | 0.50 | 65.124 ± 4.380 | 68.936 ± 5.409 | 69.102 ± 5.585 |
| none | 0.00 | 56.017 ± 3.526 | 55.789 ± 3.367 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.74 | 0.75 | 0.76 |
| block | 0.50 | 0.81 | 0.79 | 0.80 |
| block_shift | 0.30 | 0.71 | 0.73 | 0.74 |
| block_shift | 0.50 | 0.81 | 0.82 | 0.83 |
| none | 0.00 | 0.78 | 0.78 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.870 ± 0.027 | 0.869 ± 0.024 | 0.868 ± 0.026 |
| block | 0.50 | 0.847 ± 0.034 | 0.845 ± 0.030 | 0.847 ± 0.033 |
| block_shift | 0.30 | 0.856 ± 0.044 | 0.835 ± 0.059 | 0.832 ± 0.058 |
| block_shift | 0.50 | 0.815 ± 0.042 | 0.813 ± 0.049 | 0.800 ± 0.060 |
| none | 0.00 | 0.913 ± 0.003 | 0.912 ± 0.004 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.727 ± 0.039 | 0.727 ± 0.047 | 0.728 ± 0.043 |
| block | 0.50 | 0.701 ± 0.081 | 0.706 ± 0.078 | 0.704 ± 0.084 |
| block_shift | 0.30 | 0.702 ± 0.067 | 0.699 ± 0.068 | 0.700 ± 0.067 |
| block_shift | 0.50 | 0.685 ± 0.089 | 0.680 ± 0.076 | 0.683 ± 0.080 |
| none | 0.00 | 0.817 ± 0.024 | 0.814 ± 0.024 | 0.814 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 5.310 ± 0.761 | 5.510 ± 1.077 | 5.537 ± 1.193 |
| block | 0.50 | 5.675 ± 0.562 | 6.047 ± 0.727 | 5.840 ± 0.690 |
| block_shift | 0.30 | 5.624 ± 0.417 | 6.349 ± 0.852 | 6.617 ± 1.083 |
| block_shift | 0.50 | 6.716 ± 1.213 | 6.999 ± 0.950 | 7.076 ± 0.633 |
| none | 0.00 | 2.697 ± 0.477 | 2.712 ± 0.497 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.76 | 0.76 | 0.77 |
| block | 0.50 | 0.81 | 0.84 | 0.87 |
| block_shift | 0.30 | 0.76 | 0.79 | 0.80 |
| block_shift | 0.50 | 0.82 | 0.87 | 0.87 |
| none | 0.00 | 0.77 | 0.80 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_zero | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.997 ± 0.004 | 0.977 ± 0.042 | 0.980 ± 0.038 |
| block | 0.50 | 0.992 ± 0.008 | 0.989 ± 0.011 | 0.990 ± 0.011 |
| block_shift | 0.30 | 0.989 ± 0.007 | 0.989 ± 0.008 | 0.989 ± 0.008 |
| block_shift | 0.50 | 0.941 ± 0.052 | 0.905 ± 0.061 | 0.914 ± 0.062 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |
