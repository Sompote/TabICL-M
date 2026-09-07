# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.992 ± 0.003 | 0.993 ± 0.002 |
| block | 0.50 | 0.991 ± 0.005 | 0.991 ± 0.005 |
| block_shift | 0.30 | 0.988 ± 0.002 | 0.987 ± 0.003 |
| block_shift | 0.50 | 0.984 ± 0.010 | 0.982 ± 0.015 |
| none | 0.00 | 0.996 ± 0.004 | 0.997 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 62.798 ± 3.200 | 62.256 ± 2.366 |
| block | 0.50 | 63.649 ± 2.537 | 63.980 ± 3.155 |
| block_shift | 0.30 | 66.638 ± 8.981 | 67.586 ± 8.423 |
| block_shift | 0.50 | 65.559 ± 3.932 | 65.454 ± 3.846 |
| none | 0.00 | 56.326 ± 3.379 | 56.309 ± 3.404 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1063 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.834 ± 0.039 | 0.834 ± 0.036 |
| block | 0.50 | 0.872 ± 0.045 | 0.876 ± 0.049 |
| block_shift | 0.30 | 0.836 ± 0.052 | 0.834 ± 0.054 |
| block_shift | 0.50 | 0.857 ± 0.065 | 0.866 ± 0.058 |
| none | 0.00 | 0.845 ± 0.046 | 0.841 ± 0.046 |

## openml:1067 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.805 ± 0.018 | 0.815 ± 0.012 |
| block | 0.50 | 0.800 ± 0.037 | 0.819 ± 0.025 |
| block_shift | 0.30 | 0.788 ± 0.029 | 0.792 ± 0.027 |
| block_shift | 0.50 | 0.803 ± 0.033 | 0.803 ± 0.031 |
| none | 0.00 | 0.833 ± 0.023 | 0.842 ± 0.026 |

## openml:1461 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.808 ± 0.098 | 0.801 ± 0.099 |
| block | 0.50 | 0.777 ± 0.084 | 0.769 ± 0.088 |
| block_shift | 0.30 | 0.815 ± 0.101 | 0.827 ± 0.103 |
| block_shift | 0.50 | 0.734 ± 0.101 | 0.734 ± 0.105 |
| none | 0.00 | 0.934 ± 0.008 | 0.932 ± 0.007 |

## openml:1480 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.712 ± 0.021 | 0.710 ± 0.015 |
| block | 0.50 | 0.711 ± 0.028 | 0.707 ± 0.027 |
| block_shift | 0.30 | 0.684 ± 0.028 | 0.696 ± 0.036 |
| block_shift | 0.50 | 0.703 ± 0.038 | 0.679 ± 0.034 |
| none | 0.00 | 0.749 ± 0.016 | 0.760 ± 0.019 |

## openml:1494 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.905 ± 0.010 | 0.911 ± 0.013 |
| block | 0.50 | 0.884 ± 0.032 | 0.899 ± 0.028 |
| block_shift | 0.30 | 0.903 ± 0.005 | 0.906 ± 0.005 |
| block_shift | 0.50 | 0.886 ± 0.024 | 0.887 ± 0.030 |
| none | 0.00 | 0.942 ± 0.017 | 0.942 ± 0.016 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.871 ± 0.021 | 0.871 ± 0.025 |
| block | 0.50 | 0.845 ± 0.030 | 0.849 ± 0.028 |
| block_shift | 0.30 | 0.838 ± 0.060 | 0.841 ± 0.060 |
| block_shift | 0.50 | 0.822 ± 0.040 | 0.812 ± 0.046 |
| none | 0.00 | 0.915 ± 0.004 | 0.911 ± 0.003 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.218 ± 0.031 | 0.214 ± 0.031 |
| block | 0.50 | 0.248 ± 0.007 | 0.250 ± 0.008 |
| block_shift | 0.30 | 0.235 ± 0.022 | 0.238 ± 0.030 |
| block_shift | 0.50 | 0.238 ± 0.015 | 0.235 ± 0.019 |
| none | 0.00 | 0.077 ± 0.002 | 0.071 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:23 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.680 ± 0.021 | 0.687 ± 0.015 |
| block | 0.50 | 0.661 ± 0.076 | 0.664 ± 0.073 |
| block_shift | 0.30 | 0.691 ± 0.043 | 0.692 ± 0.043 |
| block_shift | 0.50 | 0.653 ± 0.059 | 0.643 ± 0.067 |
| none | 0.00 | 0.757 ± 0.014 | 0.758 ± 0.016 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.717 ± 0.051 | 0.727 ± 0.046 |
| block | 0.50 | 0.693 ± 0.071 | 0.686 ± 0.069 |
| block_shift | 0.30 | 0.696 ± 0.076 | 0.706 ± 0.063 |
| block_shift | 0.50 | 0.679 ± 0.090 | 0.673 ± 0.087 |
| none | 0.00 | 0.815 ± 0.024 | 0.816 ± 0.021 |

## openml:37 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.789 ± 0.046 | 0.788 ± 0.049 |
| block | 0.50 | 0.817 ± 0.046 | 0.819 ± 0.046 |
| block_shift | 0.30 | 0.783 ± 0.055 | 0.785 ± 0.052 |
| block_shift | 0.50 | 0.699 ± 0.096 | 0.708 ± 0.091 |
| none | 0.00 | 0.846 ± 0.008 | 0.846 ± 0.010 |

## openml:40701 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.835 ± 0.100 | 0.838 ± 0.117 |
| block | 0.50 | 0.765 ± 0.074 | 0.767 ± 0.082 |
| block_shift | 0.30 | 0.824 ± 0.113 | 0.820 ± 0.105 |
| block_shift | 0.50 | 0.682 ± 0.121 | 0.668 ± 0.113 |
| none | 0.00 | 0.930 ± 0.013 | 0.937 ± 0.016 |

## openml:40994 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.893 ± 0.068 | 0.894 ± 0.069 |
| block | 0.50 | 0.714 ± 0.142 | 0.719 ± 0.136 |
| block_shift | 0.30 | 0.770 ± 0.188 | 0.766 ± 0.207 |
| block_shift | 0.50 | 0.744 ± 0.207 | 0.738 ± 0.220 |
| none | 0.00 | 0.960 ± 0.022 | 0.961 ± 0.021 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 2337.940 ± 1111.119 | 2003.766 ± 1312.164 |
| block | 0.50 | 1447.200 ± 398.847 | 1292.578 ± 102.103 |
| block_shift | 0.30 | 2425.296 ± 1121.178 | 2076.842 ± 630.291 |
| block_shift | 0.50 | 2339.765 ± 842.233 | 2162.967 ± 479.641 |
| none | 0.00 | 609.340 ± 69.384 | 591.354 ± 72.168 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 1.068 ± 0.131 | 1.063 ± 0.130 |
| block | 0.50 | 1.140 ± 0.133 | 1.135 ± 0.136 |
| block_shift | 0.30 | 1.188 ± 0.162 | 1.135 ± 0.077 |
| block_shift | 0.50 | 1.388 ± 0.050 | 1.347 ± 0.055 |
| none | 0.00 | 0.843 ± 0.013 | 0.841 ± 0.015 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.370 ± 0.317 | 0.187 ± 0.085 |
| block | 0.50 | 0.246 ± 0.050 | 0.211 ± 0.057 |
| block_shift | 0.30 | 0.236 ± 0.083 | 0.303 ± 0.263 |
| block_shift | 0.50 | 0.197 ± 0.023 | 0.199 ± 0.021 |
| none | 0.00 | 0.095 ± 0.007 | 0.094 ± 0.007 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 5.069 ± 0.976 | 4.732 ± 0.984 |
| block | 0.50 | 5.862 ± 1.191 | 4.942 ± 0.698 |
| block_shift | 0.30 | 6.578 ± 0.832 | 6.463 ± 1.656 |
| block_shift | 0.50 | 6.749 ± 0.967 | 6.814 ± 1.170 |
| none | 0.00 | 2.715 ± 0.463 | 2.709 ± 0.493 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 4.345 ± 2.983 | 3.323 ± 2.255 |
| block | 0.50 | 4.888 ± 2.191 | 4.526 ± 2.294 |
| block_shift | 0.30 | 3.697 ± 2.503 | 4.034 ± 2.334 |
| block_shift | 0.50 | 5.559 ± 2.182 | 5.359 ± 1.877 |
| none | 0.00 | 1.939 ± 0.395 | 1.788 ± 0.674 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 | tabpfn3 |
|---|---|---|---|
| block | 0.30 | 0.995 ± 0.007 | 0.996 ± 0.006 |
| block | 0.50 | 0.991 ± 0.008 | 0.991 ± 0.010 |
| block_shift | 0.30 | 0.990 ± 0.007 | 0.990 ± 0.008 |
| block_shift | 0.50 | 0.935 ± 0.051 | 0.925 ± 0.051 |
| none | 0.00 | 1.000 ± 0.001 | 1.000 ± 0.000 |
