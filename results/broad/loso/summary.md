# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.983 ± 0.006 | 0.990 ± 0.005 | 0.984 ± 0.013 |
| block | 0.50 | 0.972 ± 0.015 | 0.989 ± 0.007 | 0.968 ± 0.030 |
| block_shift | 0.30 | 0.964 ± 0.012 | 0.986 ± 0.003 | 0.982 ± 0.005 |
| block_shift | 0.50 | 0.955 ± 0.046 | 0.985 ± 0.010 | 0.963 ± 0.037 |
| none | 0.00 | 0.996 ± 0.003 | 0.997 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 68.616 ± 3.763 | 62.626 ± 2.835 | 63.942 ± 3.954 |
| block | 0.50 | 73.235 ± 3.921 | 64.111 ± 2.602 | 66.360 ± 5.361 |
| block_shift | 0.30 | 69.752 ± 5.656 | 65.879 ± 8.590 | 67.577 ± 10.084 |
| block_shift | 0.50 | 78.813 ± 17.294 | 65.124 ± 4.380 | 69.102 ± 5.585 |
| none | 0.00 | 59.548 ± 3.316 | 56.017 ± 3.526 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.74 | 0.76 |
| block | 0.50 | 0.81 | 0.80 |
| block_shift | 0.30 | 0.71 | 0.74 |
| block_shift | 0.50 | 0.81 | 0.83 |
| none | 0.00 | 0.78 | 0.78 |

## openml:1063 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.808 ± 0.040 | 0.836 ± 0.042 | 0.830 ± 0.039 |
| block | 0.50 | 0.680 ± 0.300 | 0.875 ± 0.046 | 0.868 ± 0.048 |
| block_shift | 0.30 | 0.782 ± 0.093 | 0.832 ± 0.055 | 0.831 ± 0.052 |
| block_shift | 0.50 | 0.600 ± 0.283 | 0.869 ± 0.058 | 0.858 ± 0.057 |
| none | 0.00 | 0.783 ± 0.061 | 0.835 ± 0.049 | 0.843 ± 0.044 |

## openml:1067 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.794 ± 0.017 | 0.813 ± 0.016 | 0.790 ± 0.045 |
| block | 0.50 | 0.777 ± 0.061 | 0.822 ± 0.029 | 0.679 ± 0.178 |
| block_shift | 0.30 | 0.748 ± 0.042 | 0.787 ± 0.037 | 0.728 ± 0.091 |
| block_shift | 0.50 | 0.745 ± 0.019 | 0.803 ± 0.032 | 0.789 ± 0.042 |
| none | 0.00 | 0.801 ± 0.021 | 0.844 ± 0.022 | 0.847 ± 0.024 |

## openml:1461 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.767 ± 0.113 | 0.796 ± 0.103 | 0.790 ± 0.109 |
| block | 0.50 | 0.693 ± 0.126 | 0.780 ± 0.084 | 0.775 ± 0.094 |
| block_shift | 0.30 | 0.774 ± 0.116 | 0.831 ± 0.091 | 0.821 ± 0.112 |
| block_shift | 0.50 | 0.634 ± 0.120 | 0.744 ± 0.100 | 0.748 ± 0.093 |
| none | 0.00 | 0.911 ± 0.008 | 0.928 ± 0.007 | 0.931 ± 0.008 |

## openml:1480 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.629 ± 0.034 | 0.721 ± 0.026 | 0.729 ± 0.044 |
| block | 0.50 | 0.628 ± 0.079 | 0.705 ± 0.018 | 0.696 ± 0.029 |
| block_shift | 0.30 | 0.558 ± 0.066 | 0.683 ± 0.028 | 0.676 ± 0.028 |
| block_shift | 0.50 | 0.537 ± 0.129 | 0.682 ± 0.058 | 0.694 ± 0.045 |
| none | 0.00 | 0.728 ± 0.026 | 0.757 ± 0.012 | 0.772 ± 0.025 |

## openml:1494 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.877 ± 0.031 | 0.908 ± 0.010 | 0.892 ± 0.016 |
| block | 0.50 | 0.843 ± 0.025 | 0.875 ± 0.019 | 0.851 ± 0.047 |
| block_shift | 0.30 | 0.877 ± 0.016 | 0.900 ± 0.010 | 0.898 ± 0.005 |
| block_shift | 0.50 | 0.817 ± 0.047 | 0.892 ± 0.028 | 0.879 ± 0.030 |
| none | 0.00 | 0.930 ± 0.018 | 0.943 ± 0.015 | 0.945 ± 0.017 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.826 ± 0.027 | 0.870 ± 0.027 | 0.868 ± 0.026 |
| block | 0.50 | 0.802 ± 0.038 | 0.847 ± 0.034 | 0.847 ± 0.033 |
| block_shift | 0.30 | 0.802 ± 0.059 | 0.856 ± 0.044 | 0.832 ± 0.058 |
| block_shift | 0.50 | 0.783 ± 0.053 | 0.815 ± 0.042 | 0.800 ± 0.060 |
| none | 0.00 | 0.896 ± 0.005 | 0.913 ± 0.003 | 0.912 ± 0.004 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.265 ± 0.039 | 0.214 ± 0.030 | 0.215 ± 0.033 |
| block | 0.50 | 0.315 ± 0.055 | 0.249 ± 0.008 | 0.249 ± 0.007 |
| block_shift | 0.30 | 0.281 ± 0.042 | 0.236 ± 0.030 | 0.237 ± 0.029 |
| block_shift | 0.50 | 0.278 ± 0.006 | 0.234 ± 0.018 | 0.239 ± 0.015 |
| none | 0.00 | 0.120 ± 0.002 | 0.076 ± 0.002 | 0.077 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.76 | 0.75 |
| block | 0.50 | 0.79 | 0.81 |
| block_shift | 0.30 | 0.77 | 0.81 |
| block_shift | 0.50 | 0.80 | 0.82 |
| none | 0.00 | 0.80 | 0.81 |

## openml:23 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.587 ± 0.092 | 0.686 ± 0.012 | 0.684 ± 0.017 |
| block | 0.50 | 0.591 ± 0.069 | 0.660 ± 0.070 | 0.665 ± 0.066 |
| block_shift | 0.30 | 0.611 ± 0.058 | 0.689 ± 0.042 | 0.688 ± 0.046 |
| block_shift | 0.50 | 0.591 ± 0.047 | 0.655 ± 0.050 | 0.642 ± 0.065 |
| none | 0.00 | 0.734 ± 0.013 | 0.752 ± 0.012 | 0.757 ± 0.014 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.670 ± 0.046 | 0.727 ± 0.039 | 0.728 ± 0.043 |
| block | 0.50 | 0.603 ± 0.082 | 0.701 ± 0.081 | 0.704 ± 0.084 |
| block_shift | 0.30 | 0.652 ± 0.067 | 0.702 ± 0.067 | 0.700 ± 0.067 |
| block_shift | 0.50 | 0.624 ± 0.085 | 0.685 ± 0.089 | 0.683 ± 0.080 |
| none | 0.00 | 0.802 ± 0.011 | 0.817 ± 0.024 | 0.814 ± 0.024 |

## openml:37 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.745 ± 0.062 | 0.788 ± 0.054 | 0.780 ± 0.061 |
| block | 0.50 | 0.775 ± 0.045 | 0.817 ± 0.053 | 0.816 ± 0.054 |
| block_shift | 0.30 | 0.739 ± 0.087 | 0.784 ± 0.047 | 0.782 ± 0.051 |
| block_shift | 0.50 | 0.562 ± 0.138 | 0.701 ± 0.099 | 0.705 ± 0.086 |
| none | 0.00 | 0.826 ± 0.018 | 0.846 ± 0.007 | 0.848 ± 0.005 |

## openml:40701 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.815 ± 0.109 | 0.842 ± 0.097 | 0.816 ± 0.111 |
| block | 0.50 | 0.713 ± 0.066 | 0.757 ± 0.072 | 0.759 ± 0.064 |
| block_shift | 0.30 | 0.786 ± 0.129 | 0.811 ± 0.123 | 0.809 ± 0.122 |
| block_shift | 0.50 | 0.635 ± 0.116 | 0.696 ± 0.130 | 0.651 ± 0.121 |
| none | 0.00 | 0.927 ± 0.014 | 0.929 ± 0.015 | 0.934 ± 0.016 |

## openml:40994 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.799 ± 0.098 | 0.901 ± 0.064 | 0.894 ± 0.066 |
| block | 0.50 | 0.652 ± 0.119 | 0.737 ± 0.116 | 0.726 ± 0.132 |
| block_shift | 0.30 | 0.723 ± 0.199 | 0.803 ± 0.185 | 0.812 ± 0.148 |
| block_shift | 0.50 | 0.673 ± 0.106 | 0.773 ± 0.182 | 0.759 ± 0.198 |
| none | 0.00 | 0.947 ± 0.029 | 0.964 ± 0.024 | 0.961 ± 0.023 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 3894.201 ± 1469.307 | 2422.381 ± 1141.600 | 3188.615 ± 1209.645 |
| block | 0.50 | 2589.628 ± 1095.814 | 1463.375 ± 180.788 | 1942.994 ± 829.293 |
| block_shift | 0.30 | 2872.282 ± 1017.869 | 2027.128 ± 481.190 | 2660.944 ± 948.222 |
| block_shift | 0.50 | 3028.898 ± 1366.718 | 2207.693 ± 535.617 | 2934.625 ± 1277.725 |
| none | 0.00 | 699.489 ± 82.329 | 621.500 ± 74.491 | 618.607 ± 71.584 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.80 | 0.48 |
| block | 0.50 | 0.93 | 0.86 |
| block_shift | 0.30 | 0.79 | 0.75 |
| block_shift | 0.50 | 0.76 | 0.74 |
| none | 0.00 | 0.80 | 0.81 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 1.398 ± 0.094 | 1.068 ± 0.136 | 1.129 ± 0.143 |
| block | 0.50 | 1.605 ± 0.254 | 1.132 ± 0.114 | 1.190 ± 0.130 |
| block_shift | 0.30 | 1.463 ± 0.386 | 1.150 ± 0.093 | 1.154 ± 0.043 |
| block_shift | 0.50 | 1.511 ± 0.155 | 1.346 ± 0.039 | 1.430 ± 0.070 |
| none | 0.00 | 0.860 ± 0.010 | 0.840 ± 0.015 | 0.833 ± 0.019 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.83 | 0.84 |
| block | 0.50 | 0.82 | 0.81 |
| block_shift | 0.30 | 0.80 | 0.84 |
| block_shift | 0.50 | 0.70 | 0.68 |
| none | 0.00 | 0.79 | 0.82 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.371 ± 0.311 | 0.195 ± 0.069 | 0.339 ± 0.193 |
| block | 0.50 | 0.246 ± 0.072 | 0.185 ± 0.017 | 0.208 ± 0.017 |
| block_shift | 0.30 | 0.244 ± 0.049 | 0.205 ± 0.064 | 0.351 ± 0.275 |
| block_shift | 0.50 | 0.235 ± 0.072 | 0.186 ± 0.013 | 0.204 ± 0.018 |
| none | 0.00 | 0.123 ± 0.010 | 0.108 ± 0.012 | 0.102 ± 0.011 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.83 | 0.77 |
| block | 0.50 | 0.80 | 0.79 |
| block_shift | 0.30 | 0.78 | 0.76 |
| block_shift | 0.50 | 0.78 | 0.78 |
| none | 0.00 | 0.78 | 0.78 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 8.457 ± 2.244 | 5.310 ± 0.761 | 5.537 ± 1.193 |
| block | 0.50 | 8.031 ± 1.135 | 5.675 ± 0.562 | 5.840 ± 0.690 |
| block_shift | 0.30 | 7.401 ± 1.963 | 5.624 ± 0.417 | 6.617 ± 1.083 |
| block_shift | 0.50 | 9.488 ± 3.789 | 6.716 ± 1.213 | 7.076 ± 0.633 |
| none | 0.00 | 2.817 ± 0.329 | 2.697 ± 0.477 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.76 | 0.77 |
| block | 0.50 | 0.81 | 0.87 |
| block_shift | 0.30 | 0.76 | 0.80 |
| block_shift | 0.50 | 0.82 | 0.87 |
| none | 0.00 | 0.77 | 0.80 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 7.025 ± 3.340 | 4.369 ± 3.188 | 5.063 ± 3.805 |
| block | 0.50 | 7.599 ± 2.059 | 5.044 ± 2.128 | 5.346 ± 3.161 |
| block_shift | 0.30 | 6.514 ± 3.343 | 3.825 ± 2.774 | 4.127 ± 2.928 |
| block_shift | 0.50 | 8.318 ± 2.462 | 5.651 ± 1.962 | 6.159 ± 2.386 |
| none | 0.00 | 1.389 ± 0.260 | 1.622 ± 0.556 | 1.787 ± 0.595 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.58 | 0.52 |
| block | 0.50 | 0.76 | 0.75 |
| block_shift | 0.30 | 0.68 | 0.60 |
| block_shift | 0.50 | 0.72 | 0.62 |
| none | 0.00 | 0.87 | 0.73 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.875 ± 0.139 | 0.997 ± 0.004 | 0.980 ± 0.038 |
| block | 0.50 | 0.958 ± 0.026 | 0.992 ± 0.008 | 0.990 ± 0.011 |
| block_shift | 0.30 | 0.951 ± 0.019 | 0.989 ± 0.007 | 0.989 ± 0.008 |
| block_shift | 0.50 | 0.806 ± 0.122 | 0.941 ± 0.052 | 0.914 ± 0.062 |
| none | 0.00 | 0.998 ± 0.003 | 1.000 ± 0.000 | 1.000 ± 0.000 |

## Failed fits

- openml:1494 / block / 0.5 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.