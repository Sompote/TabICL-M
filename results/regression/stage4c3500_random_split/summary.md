# Missingness ablation

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 59.071 ± 2.876 | 59.096 ± 2.910 |
| block | 0.50 | 64.757 ± 3.984 | 64.730 ± 3.942 |
| block_shift | 0.30 | 58.899 ± 0.688 | 58.952 ± 0.742 |
| block_shift | 0.50 | 64.221 ± 3.231 | 64.330 ± 3.325 |
| none | 0.00 | 56.045 ± 3.601 | 56.103 ± 3.641 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 |
| block | 0.50 | 0.76 | 0.75 |
| block_shift | 0.30 | 0.78 | 0.78 |
| block_shift | 0.50 | 0.76 | 0.77 |
| none | 0.00 | 0.77 | 0.77 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.181 ± 0.017 | 0.181 ± 0.018 |
| block | 0.50 | 0.226 ± 0.009 | 0.226 ± 0.009 |
| block_shift | 0.30 | 0.189 ± 0.012 | 0.189 ± 0.012 |
| block_shift | 0.50 | 0.221 ± 0.007 | 0.221 ± 0.007 |
| none | 0.00 | 0.076 ± 0.002 | 0.076 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.79 | 0.79 |
| block | 0.50 | 0.81 | 0.81 |
| block_shift | 0.30 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.79 | 0.79 |
| none | 0.00 | 0.81 | 0.81 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 980.226 ± 175.447 | 976.897 ± 174.836 |
| block | 0.50 | 1217.512 ± 78.222 | 1213.542 ± 82.699 |
| block_shift | 0.30 | 1161.256 ± 222.786 | 1151.734 ± 222.080 |
| block_shift | 0.50 | 1118.183 ± 153.291 | 1114.159 ± 148.073 |
| none | 0.00 | 620.469 ± 69.165 | 614.979 ± 70.142 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.81 | 0.81 |
| block | 0.50 | 0.80 | 0.80 |
| block_shift | 0.30 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.79 | 0.79 |
| none | 0.00 | 0.81 | 0.82 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.998 ± 0.068 | 0.997 ± 0.068 |
| block | 0.50 | 1.102 ± 0.052 | 1.102 ± 0.052 |
| block_shift | 0.30 | 1.029 ± 0.031 | 1.028 ± 0.031 |
| block_shift | 0.50 | 1.103 ± 0.059 | 1.102 ± 0.059 |
| none | 0.00 | 0.839 ± 0.012 | 0.838 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.77 | 0.77 |
| block | 0.50 | 0.80 | 0.80 |
| block_shift | 0.30 | 0.77 | 0.77 |
| block_shift | 0.50 | 0.78 | 0.78 |
| none | 0.00 | 0.79 | 0.79 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.133 ± 0.006 | 0.133 ± 0.006 |
| block | 0.50 | 0.155 ± 0.013 | 0.155 ± 0.013 |
| block_shift | 0.30 | 0.159 ± 0.012 | 0.159 ± 0.012 |
| block_shift | 0.50 | 0.168 ± 0.008 | 0.168 ± 0.008 |
| none | 0.00 | 0.108 ± 0.012 | 0.108 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 |
| block | 0.50 | 0.79 | 0.79 |
| block_shift | 0.30 | 0.78 | 0.78 |
| block_shift | 0.50 | 0.78 | 0.78 |
| none | 0.00 | 0.78 | 0.78 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 3.658 ± 0.503 | 3.630 ± 0.472 |
| block | 0.50 | 4.771 ± 0.637 | 4.753 ± 0.634 |
| block_shift | 0.30 | 4.375 ± 0.607 | 4.383 ± 0.618 |
| block_shift | 0.50 | 4.623 ± 0.824 | 4.614 ± 0.830 |
| none | 0.00 | 2.693 ± 0.468 | 2.682 ± 0.458 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.79 |
| block | 0.50 | 0.75 | 0.75 |
| block_shift | 0.30 | 0.80 | 0.80 |
| block_shift | 0.50 | 0.75 | 0.76 |
| none | 0.00 | 0.78 | 0.78 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 3.746 ± 0.654 | 3.743 ± 0.660 |
| block | 0.50 | 4.028 ± 0.884 | 4.032 ± 0.896 |
| block_shift | 0.30 | 3.480 ± 0.634 | 3.472 ± 0.629 |
| block_shift | 0.50 | 3.751 ± 1.150 | 3.749 ± 1.159 |
| none | 0.00 | 1.738 ± 0.600 | 1.734 ± 0.620 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32_ypow |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 |
| block | 0.50 | 0.82 | 0.81 |
| block_shift | 0.30 | 0.73 | 0.72 |
| block_shift | 0.50 | 0.72 | 0.73 |
| none | 0.00 | 0.87 | 0.87 |
