# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.997 ± 0.003 | 0.997 ± 0.004 |
| block | 0.50 | 0.996 ± 0.004 | 0.996 ± 0.003 |
| block_shift | 0.30 | 0.994 ± 0.003 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.995 ± 0.004 | 0.995 ± 0.005 |
| none | 0.00 | 0.996 ± 0.004 | 0.997 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 59.127 ± 2.987 | 58.858 ± 2.757 |
| block | 0.50 | 64.840 ± 3.556 | 64.213 ± 3.481 |
| block_shift | 0.30 | 59.030 ± 0.448 | 58.554 ± 0.245 |
| block_shift | 0.50 | 64.110 ± 2.955 | 63.719 ± 2.751 |
| none | 0.00 | 56.326 ± 3.379 | 56.309 ± 3.404 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1063 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.836 ± 0.048 | 0.839 ± 0.045 |
| block | 0.50 | 0.833 ± 0.044 | 0.830 ± 0.038 |
| block_shift | 0.30 | 0.832 ± 0.034 | 0.830 ± 0.038 |
| block_shift | 0.50 | 0.833 ± 0.045 | 0.832 ± 0.043 |
| none | 0.00 | 0.845 ± 0.046 | 0.841 ± 0.046 |

## openml:1067 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.802 ± 0.034 | 0.819 ± 0.026 |
| block | 0.50 | 0.793 ± 0.020 | 0.811 ± 0.016 |
| block_shift | 0.30 | 0.780 ± 0.026 | 0.781 ± 0.029 |
| block_shift | 0.50 | 0.783 ± 0.030 | 0.780 ± 0.029 |
| none | 0.00 | 0.833 ± 0.023 | 0.842 ± 0.026 |

## openml:1461 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.864 ± 0.042 | 0.867 ± 0.042 |
| block | 0.50 | 0.812 ± 0.018 | 0.812 ± 0.021 |
| block_shift | 0.30 | 0.841 ± 0.031 | 0.842 ± 0.030 |
| block_shift | 0.50 | 0.820 ± 0.071 | 0.818 ± 0.065 |
| none | 0.00 | 0.934 ± 0.008 | 0.932 ± 0.007 |

## openml:1480 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.728 ± 0.016 | 0.731 ± 0.024 |
| block | 0.50 | 0.717 ± 0.035 | 0.716 ± 0.033 |
| block_shift | 0.30 | 0.715 ± 0.032 | 0.714 ± 0.031 |
| block_shift | 0.50 | 0.708 ± 0.035 | 0.710 ± 0.033 |
| none | 0.00 | 0.749 ± 0.016 | 0.760 ± 0.019 |

## openml:1494 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.930 ± 0.020 | 0.932 ± 0.018 |
| block | 0.50 | 0.918 ± 0.023 | 0.924 ± 0.021 |
| block_shift | 0.30 | 0.923 ± 0.019 | 0.924 ± 0.021 |
| block_shift | 0.50 | 0.909 ± 0.014 | 0.909 ± 0.014 |
| none | 0.00 | 0.942 ± 0.017 | 0.942 ± 0.016 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.900 ± 0.012 | 0.899 ± 0.014 |
| block | 0.50 | 0.868 ± 0.012 | 0.866 ± 0.011 |
| block_shift | 0.30 | 0.894 ± 0.005 | 0.895 ± 0.004 |
| block_shift | 0.50 | 0.859 ± 0.027 | 0.858 ± 0.024 |
| none | 0.00 | 0.915 ± 0.004 | 0.911 ± 0.003 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.182 ± 0.017 | 0.179 ± 0.017 |
| block | 0.50 | 0.226 ± 0.009 | 0.225 ± 0.008 |
| block_shift | 0.30 | 0.191 ± 0.012 | 0.187 ± 0.013 |
| block_shift | 0.50 | 0.220 ± 0.007 | 0.219 ± 0.007 |
| none | 0.00 | 0.077 ± 0.002 | 0.071 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:23 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.709 ± 0.013 | 0.708 ± 0.011 |
| block | 0.50 | 0.692 ± 0.037 | 0.693 ± 0.040 |
| block_shift | 0.30 | 0.707 ± 0.034 | 0.710 ± 0.035 |
| block_shift | 0.50 | 0.681 ± 0.016 | 0.678 ± 0.014 |
| none | 0.00 | 0.757 ± 0.014 | 0.758 ± 0.016 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.764 ± 0.055 | 0.764 ± 0.057 |
| block | 0.50 | 0.728 ± 0.036 | 0.726 ± 0.036 |
| block_shift | 0.30 | 0.767 ± 0.029 | 0.767 ± 0.026 |
| block_shift | 0.50 | 0.727 ± 0.038 | 0.720 ± 0.040 |
| none | 0.00 | 0.815 ± 0.024 | 0.816 ± 0.021 |

## openml:37 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.832 ± 0.013 | 0.834 ± 0.013 |
| block | 0.50 | 0.777 ± 0.019 | 0.782 ± 0.015 |
| block_shift | 0.30 | 0.814 ± 0.027 | 0.815 ± 0.026 |
| block_shift | 0.50 | 0.738 ± 0.039 | 0.731 ± 0.037 |
| none | 0.00 | 0.846 ± 0.008 | 0.846 ± 0.010 |

## openml:40701 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.907 ± 0.025 | 0.915 ± 0.024 |
| block | 0.50 | 0.825 ± 0.015 | 0.826 ± 0.014 |
| block_shift | 0.30 | 0.889 ± 0.022 | 0.893 ± 0.024 |
| block_shift | 0.50 | 0.819 ± 0.056 | 0.822 ± 0.057 |
| none | 0.00 | 0.930 ± 0.013 | 0.937 ± 0.016 |

## openml:40994 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.923 ± 0.045 | 0.923 ± 0.040 |
| block | 0.50 | 0.826 ± 0.036 | 0.823 ± 0.019 |
| block_shift | 0.30 | 0.918 ± 0.055 | 0.922 ± 0.049 |
| block_shift | 0.50 | 0.865 ± 0.032 | 0.881 ± 0.024 |
| none | 0.00 | 0.960 ± 0.022 | 0.961 ± 0.021 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 1218.930 ± 477.302 | 973.000 ± 170.762 |
| block | 0.50 | 1211.943 ± 85.911 | 1199.662 ± 90.083 |
| block_shift | 0.30 | 1132.543 ± 221.437 | 1131.719 ± 213.363 |
| block_shift | 0.50 | 1096.384 ± 144.041 | 1091.354 ± 142.252 |
| none | 0.00 | 609.340 ± 69.384 | 591.354 ± 72.168 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 1.000 ± 0.068 | 0.998 ± 0.063 |
| block | 0.50 | 1.103 ± 0.047 | 1.099 ± 0.046 |
| block_shift | 0.30 | 1.033 ± 0.034 | 1.030 ± 0.028 |
| block_shift | 0.50 | 1.101 ± 0.062 | 1.102 ± 0.057 |
| none | 0.00 | 0.843 ± 0.013 | 0.841 ± 0.015 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.126 ± 0.009 | 0.126 ± 0.008 |
| block | 0.50 | 0.153 ± 0.013 | 0.153 ± 0.013 |
| block_shift | 0.30 | 0.155 ± 0.011 | 0.152 ± 0.011 |
| block_shift | 0.50 | 0.167 ± 0.007 | 0.166 ± 0.008 |
| none | 0.00 | 0.095 ± 0.007 | 0.094 ± 0.007 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 3.766 ± 0.565 | 3.639 ± 0.559 |
| block | 0.50 | 4.932 ± 0.581 | 4.899 ± 0.589 |
| block_shift | 0.30 | 4.368 ± 0.661 | 4.258 ± 0.565 |
| block_shift | 0.50 | 4.667 ± 0.817 | 4.632 ± 0.803 |
| none | 0.00 | 2.715 ± 0.463 | 2.709 ± 0.493 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 3.711 ± 0.818 | 3.737 ± 0.709 |
| block | 0.50 | 4.038 ± 0.938 | 4.029 ± 0.933 |
| block_shift | 0.30 | 3.513 ± 0.599 | 3.459 ± 0.584 |
| block_shift | 0.50 | 3.738 ± 1.119 | 3.636 ± 1.175 |
| none | 0.00 | 1.939 ± 0.395 | 1.788 ± 0.674 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.997 ± 0.005 | 0.997 ± 0.003 |
| block | 0.50 | 0.995 ± 0.006 | 0.994 ± 0.006 |
| block_shift | 0.30 | 0.995 ± 0.006 | 0.995 ± 0.006 |
| block_shift | 0.50 | 0.989 ± 0.023 | 0.986 ± 0.028 |
| none | 0.00 | 1.000 ± 0.001 | 1.000 ± 0.000 |
