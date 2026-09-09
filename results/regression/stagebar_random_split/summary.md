# Missingness ablation

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 59.145 ± 2.788 | 59.142 ± 2.796 |
| block | 0.50 | 64.884 ± 3.645 | 64.841 ± 3.610 |
| block_shift | 0.30 | 58.992 ± 0.606 | 59.051 ± 0.666 |
| block_shift | 0.50 | 64.474 ± 2.930 | 64.517 ± 2.912 |
| none | 0.00 | 56.194 ± 3.480 | 56.228 ± 3.459 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.80 | 0.80 |
| block | 0.50 | 0.79 | 0.79 |
| block_shift | 0.30 | 0.82 | 0.82 |
| block_shift | 0.50 | 0.80 | 0.80 |
| none | 0.00 | 0.80 | 0.80 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.183 ± 0.017 | 0.183 ± 0.017 |
| block | 0.50 | 0.227 ± 0.009 | 0.227 ± 0.009 |
| block_shift | 0.30 | 0.192 ± 0.012 | 0.192 ± 0.012 |
| block_shift | 0.50 | 0.221 ± 0.007 | 0.221 ± 0.007 |
| none | 0.00 | 0.081 ± 0.003 | 0.080 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.79 | 0.79 |
| block | 0.50 | 0.81 | 0.81 |
| block_shift | 0.30 | 0.78 | 0.78 |
| block_shift | 0.50 | 0.79 | 0.79 |
| none | 0.00 | 0.81 | 0.81 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 1019.720 ± 171.607 | 1014.306 ± 173.025 |
| block | 0.50 | 1237.811 ± 94.990 | 1236.616 ± 95.655 |
| block_shift | 0.30 | 1190.042 ± 226.560 | 1187.797 ± 224.876 |
| block_shift | 0.50 | 1151.508 ± 147.723 | 1150.521 ± 143.142 |
| none | 0.00 | 714.564 ± 112.408 | 707.501 ± 100.082 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.82 | 0.82 |
| block | 0.50 | 0.82 | 0.83 |
| block_shift | 0.30 | 0.81 | 0.81 |
| block_shift | 0.50 | 0.81 | 0.81 |
| none | 0.00 | 0.83 | 0.82 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 1.000 ± 0.066 | 1.000 ± 0.066 |
| block | 0.50 | 1.102 ± 0.053 | 1.102 ± 0.052 |
| block_shift | 0.30 | 1.030 ± 0.025 | 1.030 ± 0.025 |
| block_shift | 0.50 | 1.102 ± 0.058 | 1.103 ± 0.059 |
| none | 0.00 | 0.842 ± 0.019 | 0.841 ± 0.019 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.80 | 0.80 |
| block | 0.50 | 0.81 | 0.81 |
| block_shift | 0.30 | 0.81 | 0.81 |
| block_shift | 0.50 | 0.80 | 0.80 |
| none | 0.00 | 0.81 | 0.81 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.134 ± 0.005 | 0.134 ± 0.005 |
| block | 0.50 | 0.156 ± 0.014 | 0.156 ± 0.014 |
| block_shift | 0.30 | 0.159 ± 0.012 | 0.159 ± 0.012 |
| block_shift | 0.50 | 0.169 ± 0.008 | 0.169 ± 0.008 |
| none | 0.00 | 0.108 ± 0.012 | 0.108 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.79 |
| block | 0.50 | 0.79 | 0.79 |
| block_shift | 0.30 | 0.77 | 0.77 |
| block_shift | 0.50 | 0.77 | 0.77 |
| none | 0.00 | 0.78 | 0.79 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 3.700 ± 0.474 | 3.687 ± 0.472 |
| block | 0.50 | 4.835 ± 0.694 | 4.832 ± 0.683 |
| block_shift | 0.30 | 4.344 ± 0.656 | 4.319 ± 0.646 |
| block_shift | 0.50 | 4.766 ± 0.826 | 4.748 ± 0.813 |
| none | 0.00 | 2.816 ± 0.541 | 2.817 ± 0.535 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.81 | 0.81 |
| block | 0.50 | 0.78 | 0.77 |
| block_shift | 0.30 | 0.81 | 0.81 |
| block_shift | 0.50 | 0.78 | 0.77 |
| none | 0.00 | 0.81 | 0.80 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 3.757 ± 0.648 | 3.766 ± 0.632 |
| block | 0.50 | 4.088 ± 0.799 | 4.088 ± 0.818 |
| block_shift | 0.30 | 3.496 ± 0.700 | 3.484 ± 0.703 |
| block_shift | 0.50 | 3.679 ± 1.245 | 3.682 ± 1.251 |
| none | 0.00 | 1.940 ± 0.609 | 1.941 ± 0.608 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.87 | 0.87 |
| block | 0.50 | 0.85 | 0.85 |
| block_shift | 0.30 | 0.81 | 0.81 |
| block_shift | 0.50 | 0.81 | 0.81 |
| none | 0.00 | 0.96 | 0.96 |
