# Missingness ablation

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 62.614 ± 2.943 | 62.541 ± 2.926 |
| block | 0.50 | 64.274 ± 2.563 | 64.200 ± 2.307 |
| block_shift | 0.30 | 65.798 ± 8.391 | 65.843 ± 8.435 |
| block_shift | 0.50 | 65.077 ± 4.474 | 65.053 ± 4.493 |
| none | 0.00 | 56.045 ± 3.601 | 56.103 ± 3.641 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.74 | 0.75 |
| block | 0.50 | 0.80 | 0.81 |
| block_shift | 0.30 | 0.71 | 0.71 |
| block_shift | 0.50 | 0.81 | 0.81 |
| none | 0.00 | 0.77 | 0.77 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.214 ± 0.030 | 0.214 ± 0.030 |
| block | 0.50 | 0.250 ± 0.007 | 0.249 ± 0.008 |
| block_shift | 0.30 | 0.234 ± 0.029 | 0.234 ± 0.029 |
| block_shift | 0.50 | 0.235 ± 0.018 | 0.234 ± 0.018 |
| none | 0.00 | 0.076 ± 0.002 | 0.076 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.76 | 0.76 |
| block | 0.50 | 0.79 | 0.79 |
| block_shift | 0.30 | 0.77 | 0.77 |
| block_shift | 0.50 | 0.80 | 0.79 |
| none | 0.00 | 0.81 | 0.81 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 2415.084 ± 1152.750 | 2349.447 ± 1176.370 |
| block | 0.50 | 1444.566 ± 129.027 | 1405.651 ± 104.226 |
| block_shift | 0.30 | 2014.619 ± 483.235 | 1977.873 ± 472.727 |
| block_shift | 0.50 | 2181.016 ± 517.931 | 2158.415 ± 464.383 |
| none | 0.00 | 620.469 ± 69.165 | 614.979 ± 70.142 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.81 | 0.80 |
| block | 0.50 | 0.93 | 0.93 |
| block_shift | 0.30 | 0.79 | 0.80 |
| block_shift | 0.50 | 0.77 | 0.77 |
| none | 0.00 | 0.81 | 0.82 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 1.070 ± 0.136 | 1.069 ± 0.137 |
| block | 0.50 | 1.136 ± 0.114 | 1.138 ± 0.113 |
| block_shift | 0.30 | 1.146 ± 0.087 | 1.146 ± 0.088 |
| block_shift | 0.50 | 1.339 ± 0.035 | 1.341 ± 0.037 |
| none | 0.00 | 0.839 ± 0.012 | 0.838 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.83 | 0.83 |
| block | 0.50 | 0.82 | 0.82 |
| block_shift | 0.30 | 0.81 | 0.80 |
| block_shift | 0.50 | 0.70 | 0.70 |
| none | 0.00 | 0.79 | 0.79 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.194 ± 0.071 | 0.190 ± 0.064 |
| block | 0.50 | 0.185 ± 0.017 | 0.185 ± 0.016 |
| block_shift | 0.30 | 0.206 ± 0.064 | 0.217 ± 0.069 |
| block_shift | 0.50 | 0.186 ± 0.013 | 0.186 ± 0.013 |
| none | 0.00 | 0.108 ± 0.012 | 0.108 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.83 | 0.84 |
| block | 0.50 | 0.80 | 0.80 |
| block_shift | 0.30 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.79 | 0.79 |
| none | 0.00 | 0.78 | 0.78 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 5.330 ± 0.747 | 5.232 ± 0.754 |
| block | 0.50 | 5.593 ± 0.546 | 5.585 ± 0.534 |
| block_shift | 0.30 | 5.610 ± 0.437 | 5.648 ± 0.489 |
| block_shift | 0.50 | 6.689 ± 1.246 | 6.694 ± 1.274 |
| none | 0.00 | 2.693 ± 0.468 | 2.682 ± 0.458 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.77 | 0.77 |
| block | 0.50 | 0.81 | 0.82 |
| block_shift | 0.30 | 0.76 | 0.76 |
| block_shift | 0.50 | 0.81 | 0.81 |
| none | 0.00 | 0.78 | 0.78 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 4.332 ± 3.181 | 4.194 ± 2.981 |
| block | 0.50 | 5.035 ± 2.142 | 4.958 ± 2.125 |
| block_shift | 0.30 | 3.805 ± 2.821 | 3.875 ± 2.788 |
| block_shift | 0.50 | 5.623 ± 1.953 | 5.589 ± 1.926 |
| none | 0.00 | 1.738 ± 0.600 | 1.734 ± 0.620 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.59 | 0.64 |
| block | 0.50 | 0.76 | 0.77 |
| block_shift | 0.30 | 0.70 | 0.67 |
| block_shift | 0.50 | 0.72 | 0.72 |
| none | 0.00 | 0.87 | 0.87 |
