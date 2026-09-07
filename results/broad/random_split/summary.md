# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.995 ± 0.005 | 0.997 ± 0.003 | 0.997 ± 0.003 |
| block | 0.50 | 0.993 ± 0.006 | 0.995 ± 0.003 | 0.995 ± 0.004 |
| block_shift | 0.30 | 0.991 ± 0.005 | 0.994 ± 0.004 | 0.994 ± 0.003 |
| block_shift | 0.50 | 0.990 ± 0.007 | 0.994 ± 0.005 | 0.994 ± 0.005 |
| none | 0.00 | 0.996 ± 0.003 | 0.997 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 60.713 ± 3.734 | 59.114 ± 2.843 | 59.326 ± 2.991 |
| block | 0.50 | 68.755 ± 4.360 | 64.716 ± 3.998 | 65.344 ± 3.639 |
| block_shift | 0.30 | 61.406 ± 1.724 | 58.938 ± 0.711 | 59.288 ± 1.304 |
| block_shift | 0.50 | 69.409 ± 2.530 | 64.148 ± 3.378 | 64.778 ± 2.812 |
| none | 0.00 | 59.548 ± 3.316 | 56.017 ± 3.526 | 55.789 ± 3.367 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.79 |
| block | 0.50 | 0.76 | 0.78 |
| block_shift | 0.30 | 0.79 | 0.80 |
| block_shift | 0.50 | 0.77 | 0.78 |
| none | 0.00 | 0.78 | 0.78 |

## openml:1063 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.768 ± 0.045 | 0.839 ± 0.046 | 0.840 ± 0.043 |
| block | 0.50 | 0.768 ± 0.060 | 0.836 ± 0.042 | 0.837 ± 0.043 |
| block_shift | 0.30 | 0.815 ± 0.027 | 0.838 ± 0.036 | 0.831 ± 0.036 |
| block_shift | 0.50 | 0.764 ± 0.062 | 0.836 ± 0.044 | 0.828 ± 0.041 |
| none | 0.00 | 0.783 ± 0.061 | 0.835 ± 0.049 | 0.843 ± 0.044 |

## openml:1067 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.785 ± 0.018 | 0.821 ± 0.029 | 0.816 ± 0.028 |
| block | 0.50 | 0.766 ± 0.014 | 0.808 ± 0.021 | 0.808 ± 0.023 |
| block_shift | 0.30 | 0.764 ± 0.017 | 0.787 ± 0.025 | 0.784 ± 0.026 |
| block_shift | 0.50 | 0.755 ± 0.029 | 0.783 ± 0.031 | 0.779 ± 0.032 |
| none | 0.00 | 0.801 ± 0.021 | 0.844 ± 0.022 | 0.847 ± 0.024 |

## openml:1461 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.832 ± 0.042 | 0.866 ± 0.040 | 0.864 ± 0.042 |
| block | 0.50 | 0.768 ± 0.029 | 0.812 ± 0.022 | 0.805 ± 0.028 |
| block_shift | 0.30 | 0.807 ± 0.040 | 0.841 ± 0.030 | 0.836 ± 0.039 |
| block_shift | 0.50 | 0.794 ± 0.074 | 0.819 ± 0.074 | 0.816 ± 0.069 |
| none | 0.00 | 0.911 ± 0.008 | 0.928 ± 0.007 | 0.931 ± 0.008 |

## openml:1480 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.710 ± 0.034 | 0.737 ± 0.020 | 0.737 ± 0.019 |
| block | 0.50 | 0.677 ± 0.036 | 0.720 ± 0.032 | 0.705 ± 0.038 |
| block_shift | 0.30 | 0.683 ± 0.040 | 0.716 ± 0.033 | 0.713 ± 0.026 |
| block_shift | 0.50 | 0.677 ± 0.030 | 0.708 ± 0.034 | 0.708 ± 0.028 |
| none | 0.00 | 0.728 ± 0.026 | 0.757 ± 0.012 | 0.772 ± 0.025 |

## openml:1494 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.919 ± 0.020 | 0.932 ± 0.018 | 0.934 ± 0.019 |
| block | 0.50 | 0.908 ± 0.026 | 0.932 ± 0.013 | 0.922 ± 0.021 |
| block_shift | 0.30 | 0.905 ± 0.023 | 0.924 ± 0.021 | 0.923 ± 0.023 |
| block_shift | 0.50 | 0.888 ± 0.021 | 0.913 ± 0.014 | 0.910 ± 0.015 |
| none | 0.00 | 0.930 ± 0.018 | 0.943 ± 0.015 | 0.945 ± 0.017 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.885 ± 0.012 | 0.900 ± 0.014 | 0.900 ± 0.013 |
| block | 0.50 | 0.853 ± 0.006 | 0.869 ± 0.010 | 0.865 ± 0.009 |
| block_shift | 0.30 | 0.878 ± 0.006 | 0.897 ± 0.002 | 0.894 ± 0.004 |
| block_shift | 0.50 | 0.843 ± 0.027 | 0.860 ± 0.025 | 0.859 ± 0.028 |
| none | 0.00 | 0.896 ± 0.005 | 0.913 ± 0.003 | 0.912 ± 0.004 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.196 ± 0.012 | 0.181 ± 0.017 | 0.181 ± 0.018 |
| block | 0.50 | 0.230 ± 0.009 | 0.226 ± 0.009 | 0.226 ± 0.009 |
| block_shift | 0.30 | 0.203 ± 0.011 | 0.190 ± 0.012 | 0.190 ± 0.012 |
| block_shift | 0.50 | 0.226 ± 0.006 | 0.221 ± 0.007 | 0.221 ± 0.007 |
| none | 0.00 | 0.120 ± 0.002 | 0.076 ± 0.002 | 0.077 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.79 | 0.81 |
| block | 0.50 | 0.81 | 0.82 |
| block_shift | 0.30 | 0.79 | 0.81 |
| block_shift | 0.50 | 0.79 | 0.80 |
| none | 0.00 | 0.80 | 0.81 |

## openml:23 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.677 ± 0.008 | 0.705 ± 0.011 | 0.703 ± 0.012 |
| block | 0.50 | 0.666 ± 0.036 | 0.687 ± 0.036 | 0.682 ± 0.044 |
| block_shift | 0.30 | 0.676 ± 0.026 | 0.704 ± 0.035 | 0.700 ± 0.038 |
| block_shift | 0.50 | 0.650 ± 0.019 | 0.679 ± 0.015 | 0.675 ± 0.017 |
| none | 0.00 | 0.734 ± 0.013 | 0.752 ± 0.012 | 0.757 ± 0.014 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.736 ± 0.032 | 0.774 ± 0.053 | 0.769 ± 0.050 |
| block | 0.50 | 0.695 ± 0.059 | 0.722 ± 0.033 | 0.722 ± 0.034 |
| block_shift | 0.30 | 0.716 ± 0.048 | 0.769 ± 0.033 | 0.769 ± 0.034 |
| block_shift | 0.50 | 0.695 ± 0.035 | 0.725 ± 0.033 | 0.727 ± 0.028 |
| none | 0.00 | 0.802 ± 0.011 | 0.817 ± 0.024 | 0.814 ± 0.024 |

## openml:37 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.807 ± 0.014 | 0.831 ± 0.012 | 0.831 ± 0.015 |
| block | 0.50 | 0.745 ± 0.044 | 0.781 ± 0.023 | 0.775 ± 0.022 |
| block_shift | 0.30 | 0.787 ± 0.041 | 0.816 ± 0.025 | 0.811 ± 0.025 |
| block_shift | 0.50 | 0.712 ± 0.042 | 0.738 ± 0.044 | 0.730 ± 0.041 |
| none | 0.00 | 0.826 ± 0.018 | 0.846 ± 0.007 | 0.848 ± 0.005 |

## openml:40701 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.895 ± 0.037 | 0.906 ± 0.025 | 0.909 ± 0.030 |
| block | 0.50 | 0.793 ± 0.026 | 0.823 ± 0.015 | 0.822 ± 0.019 |
| block_shift | 0.30 | 0.872 ± 0.037 | 0.889 ± 0.022 | 0.893 ± 0.022 |
| block_shift | 0.50 | 0.791 ± 0.056 | 0.818 ± 0.055 | 0.813 ± 0.058 |
| none | 0.00 | 0.927 ± 0.014 | 0.929 ± 0.015 | 0.934 ± 0.016 |

## openml:40994 (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.879 ± 0.061 | 0.923 ± 0.045 | 0.925 ± 0.043 |
| block | 0.50 | 0.724 ± 0.059 | 0.820 ± 0.037 | 0.831 ± 0.025 |
| block_shift | 0.30 | 0.867 ± 0.061 | 0.915 ± 0.052 | 0.921 ± 0.050 |
| block_shift | 0.50 | 0.787 ± 0.026 | 0.880 ± 0.019 | 0.866 ± 0.026 |
| none | 0.00 | 0.947 ± 0.029 | 0.964 ± 0.024 | 0.961 ± 0.023 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 1093.763 ± 163.105 | 980.346 ± 171.118 | 970.828 ± 197.810 |
| block | 0.50 | 1286.510 ± 80.896 | 1214.415 ± 82.048 | 1218.978 ± 75.313 |
| block_shift | 0.30 | 1222.664 ± 213.723 | 1158.916 ± 225.271 | 1137.949 ± 218.275 |
| block_shift | 0.50 | 1225.923 ± 157.639 | 1114.001 ± 156.714 | 1098.751 ± 155.328 |
| none | 0.00 | 699.489 ± 82.329 | 621.501 ± 74.491 | 618.607 ± 71.584 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.80 | 0.81 |
| block | 0.50 | 0.79 | 0.80 |
| block_shift | 0.30 | 0.78 | 0.80 |
| block_shift | 0.50 | 0.79 | 0.79 |
| none | 0.00 | 0.80 | 0.81 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 1.023 ± 0.070 | 1.000 ± 0.068 | 0.999 ± 0.065 |
| block | 0.50 | 1.113 ± 0.047 | 1.102 ± 0.051 | 1.098 ± 0.049 |
| block_shift | 0.30 | 1.064 ± 0.034 | 1.031 ± 0.031 | 1.030 ± 0.023 |
| block_shift | 0.50 | 1.131 ± 0.053 | 1.102 ± 0.058 | 1.101 ± 0.059 |
| none | 0.00 | 0.860 ± 0.010 | 0.840 ± 0.015 | 0.833 ± 0.019 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.77 | 0.79 |
| block | 0.50 | 0.80 | 0.81 |
| block_shift | 0.30 | 0.78 | 0.80 |
| block_shift | 0.50 | 0.79 | 0.80 |
| none | 0.00 | 0.79 | 0.82 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.143 ± 0.006 | 0.133 ± 0.006 | 0.131 ± 0.007 |
| block | 0.50 | 0.162 ± 0.014 | 0.155 ± 0.013 | 0.155 ± 0.013 |
| block_shift | 0.30 | 0.161 ± 0.011 | 0.160 ± 0.013 | 0.158 ± 0.012 |
| block_shift | 0.50 | 0.172 ± 0.008 | 0.169 ± 0.008 | 0.168 ± 0.008 |
| none | 0.00 | 0.123 ± 0.010 | 0.108 ± 0.012 | 0.102 ± 0.011 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 |
| block | 0.50 | 0.79 | 0.80 |
| block_shift | 0.30 | 0.77 | 0.79 |
| block_shift | 0.50 | 0.77 | 0.78 |
| none | 0.00 | 0.78 | 0.78 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 3.825 ± 0.221 | 3.653 ± 0.496 | 3.729 ± 0.543 |
| block | 0.50 | 4.981 ± 0.582 | 4.770 ± 0.649 | 4.842 ± 0.554 |
| block_shift | 0.30 | 4.626 ± 0.508 | 4.369 ± 0.620 | 4.380 ± 0.594 |
| block_shift | 0.50 | 5.077 ± 0.802 | 4.616 ± 0.840 | 4.700 ± 0.889 |
| none | 0.00 | 2.817 ± 0.329 | 2.697 ± 0.477 | 2.712 ± 0.497 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.79 | 0.80 |
| block | 0.50 | 0.76 | 0.76 |
| block_shift | 0.30 | 0.80 | 0.81 |
| block_shift | 0.50 | 0.76 | 0.78 |
| none | 0.00 | 0.77 | 0.80 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 3.952 ± 0.839 | 3.715 ± 0.657 | 3.802 ± 0.700 |
| block | 0.50 | 4.471 ± 0.815 | 4.026 ± 0.877 | 4.156 ± 1.016 |
| block_shift | 0.30 | 3.833 ± 0.887 | 3.464 ± 0.650 | 3.561 ± 0.653 |
| block_shift | 0.50 | 4.016 ± 1.350 | 3.738 ± 1.162 | 3.890 ± 1.279 |
| none | 0.00 | 1.389 ± 0.260 | 1.622 ± 0.556 | 1.787 ± 0.595 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.30 | 0.77 | 0.79 |
| block | 0.50 | 0.81 | 0.77 |
| block_shift | 0.30 | 0.72 | 0.77 |
| block_shift | 0.50 | 0.72 | 0.77 |
| none | 0.00 | 0.87 | 0.73 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | catboost | tabicl_aware | tabicl_impute |
|---|---|---|---|---|
| block | 0.30 | 0.990 ± 0.010 | 0.999 ± 0.003 | 0.997 ± 0.005 |
| block | 0.50 | 0.984 ± 0.014 | 0.996 ± 0.004 | 0.996 ± 0.006 |
| block_shift | 0.30 | 0.985 ± 0.010 | 0.996 ± 0.005 | 0.996 ± 0.004 |
| block_shift | 0.50 | 0.981 ± 0.031 | 0.988 ± 0.024 | 0.989 ± 0.024 |
| none | 0.00 | 0.998 ± 0.003 | 1.000 ± 0.000 | 1.000 ± 0.000 |

## Failed fits

- openml:1494 / block / 0.5 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.