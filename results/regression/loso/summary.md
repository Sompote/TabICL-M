# Missingness ablation

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 62.626 ± 2.835 | 62.725 ± 2.981 | 62.517 ± 2.857 | 62.552 ± 2.864 | 62.661 ± 2.843 |
| block | 0.50 | 64.111 ± 2.602 | 63.725 ± 1.749 | 64.040 ± 2.344 | 64.073 ± 2.338 | 64.134 ± 2.600 |
| block_shift | 0.30 | 65.879 ± 8.590 | 66.534 ± 10.572 | 65.914 ± 8.602 | 65.941 ± 8.575 | 65.908 ± 8.546 |
| block_shift | 0.50 | 65.124 ± 4.380 | 65.204 ± 4.144 | 65.058 ± 4.465 | 65.061 ± 4.424 | 65.136 ± 4.349 |
| none | 0.00 | 56.017 ± 3.526 | 56.213 ± 3.770 | 56.058 ± 3.544 | 56.077 ± 3.556 | 56.042 ± 3.546 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.74 | 0.74 | 0.74 | 0.74 | 0.74 |
| block | 0.50 | 0.81 | 0.81 | 0.81 | 0.81 | 0.81 |
| block_shift | 0.30 | 0.71 | 0.71 | 0.71 | 0.71 | 0.71 |
| block_shift | 0.50 | 0.81 | 0.81 | 0.81 | 0.81 | 0.81 |
| none | 0.00 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.214 ± 0.030 | 0.214 ± 0.033 | 0.214 ± 0.030 | 0.214 ± 0.030 | 0.214 ± 0.030 |
| block | 0.50 | 0.249 ± 0.008 | 0.249 ± 0.008 | 0.249 ± 0.008 | 0.249 ± 0.008 | 0.249 ± 0.008 |
| block_shift | 0.30 | 0.236 ± 0.030 | 0.237 ± 0.032 | 0.236 ± 0.030 | 0.235 ± 0.030 | 0.236 ± 0.030 |
| block_shift | 0.50 | 0.234 ± 0.018 | 0.235 ± 0.019 | 0.234 ± 0.018 | 0.234 ± 0.018 | 0.234 ± 0.018 |
| none | 0.00 | 0.076 ± 0.002 | 0.076 ± 0.002 | 0.075 ± 0.002 | 0.075 ± 0.002 | 0.076 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.76 | 0.76 | 0.76 | 0.76 | 0.76 |
| block | 0.50 | 0.79 | 0.79 | 0.80 | 0.80 | 0.79 |
| block_shift | 0.30 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 |
| block_shift | 0.50 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| none | 0.00 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 2422.381 ± 1141.600 | 2576.389 ± 1154.651 | 2438.584 ± 1159.641 | 2365.000 ± 1172.928 | 2357.281 ± 1157.678 |
| block | 0.50 | 1463.375 ± 180.788 | 1538.244 ± 243.441 | 1425.110 ± 127.767 | 1416.240 ± 130.281 | 1452.023 ± 176.951 |
| block_shift | 0.30 | 2027.128 ± 481.190 | 2070.753 ± 600.779 | 2017.122 ± 478.221 | 1994.755 ± 478.494 | 2004.679 ± 475.527 |
| block_shift | 0.50 | 2207.693 ± 535.617 | 2191.633 ± 669.055 | 2169.169 ± 475.558 | 2171.965 ± 471.595 | 2201.133 ± 531.125 |
| none | 0.00 | 621.500 ± 74.491 | 627.859 ± 77.715 | 616.556 ± 69.307 | 615.503 ± 71.607 | 619.299 ± 75.081 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| block | 0.50 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 |
| block_shift | 0.30 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.76 | 0.76 | 0.76 | 0.76 | 0.76 |
| none | 0.00 | 0.80 | 0.80 | 0.81 | 0.81 | 0.80 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 1.068 ± 0.136 | 1.070 ± 0.137 | 1.067 ± 0.137 | 1.067 ± 0.137 | 1.068 ± 0.137 |
| block | 0.50 | 1.132 ± 0.114 | 1.127 ± 0.115 | 1.133 ± 0.113 | 1.134 ± 0.113 | 1.132 ± 0.114 |
| block_shift | 0.30 | 1.150 ± 0.093 | 1.165 ± 0.097 | 1.150 ± 0.093 | 1.150 ± 0.093 | 1.150 ± 0.093 |
| block_shift | 0.50 | 1.346 ± 0.039 | 1.339 ± 0.044 | 1.346 ± 0.041 | 1.347 ± 0.041 | 1.346 ± 0.040 |
| none | 0.00 | 0.840 ± 0.015 | 0.844 ± 0.013 | 0.839 ± 0.014 | 0.839 ± 0.014 | 0.840 ± 0.015 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.83 | 0.83 | 0.83 | 0.83 | 0.83 |
| block | 0.50 | 0.82 | 0.82 | 0.82 | 0.82 | 0.82 |
| block_shift | 0.30 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| block_shift | 0.50 | 0.70 | 0.70 | 0.70 | 0.70 | 0.70 |
| none | 0.00 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.195 ± 0.069 | 0.181 ± 0.047 | 0.196 ± 0.073 | 0.190 ± 0.061 | 0.189 ± 0.058 |
| block | 0.50 | 0.185 ± 0.017 | 0.185 ± 0.017 | 0.185 ± 0.016 | 0.185 ± 0.016 | 0.185 ± 0.017 |
| block_shift | 0.30 | 0.205 ± 0.064 | 0.195 ± 0.047 | 0.209 ± 0.065 | 0.214 ± 0.067 | 0.210 ± 0.066 |
| block_shift | 0.50 | 0.186 ± 0.013 | 0.186 ± 0.016 | 0.186 ± 0.013 | 0.186 ± 0.013 | 0.186 ± 0.013 |
| none | 0.00 | 0.108 ± 0.012 | 0.108 ± 0.012 | 0.108 ± 0.012 | 0.108 ± 0.012 | 0.108 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.83 | 0.83 | 0.83 | 0.83 | 0.83 |
| block | 0.50 | 0.80 | 0.80 | 0.81 | 0.81 | 0.80 |
| block_shift | 0.30 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |
| block_shift | 0.50 | 0.78 | 0.78 | 0.79 | 0.79 | 0.78 |
| none | 0.00 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 5.310 ± 0.761 | 5.367 ± 0.737 | 5.219 ± 0.765 | 5.222 ± 0.778 | 5.313 ± 0.773 |
| block | 0.50 | 5.675 ± 0.562 | 5.863 ± 0.509 | 5.668 ± 0.569 | 5.688 ± 0.552 | 5.699 ± 0.540 |
| block_shift | 0.30 | 5.624 ± 0.417 | 5.573 ± 0.198 | 5.639 ± 0.431 | 5.665 ± 0.448 | 5.648 ± 0.430 |
| block_shift | 0.50 | 6.716 ± 1.213 | 7.031 ± 1.249 | 6.722 ± 1.236 | 6.718 ± 1.259 | 6.711 ± 1.241 |
| none | 0.00 | 2.697 ± 0.477 | 2.697 ± 0.496 | 2.683 ± 0.468 | 2.681 ± 0.462 | 2.693 ± 0.468 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.76 | 0.76 | 0.77 | 0.77 | 0.76 |
| block | 0.50 | 0.81 | 0.81 | 0.82 | 0.82 | 0.81 |
| block_shift | 0.30 | 0.76 | 0.76 | 0.77 | 0.77 | 0.76 |
| block_shift | 0.50 | 0.82 | 0.82 | 0.81 | 0.81 | 0.82 |
| none | 0.00 | 0.77 | 0.77 | 0.78 | 0.78 | 0.77 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 4.369 ± 3.188 | 4.452 ± 3.412 | 4.247 ± 2.998 | 4.247 ± 2.998 | 4.368 ± 3.189 |
| block | 0.50 | 5.044 ± 2.128 | 4.983 ± 2.255 | 4.955 ± 2.104 | 4.955 ± 2.110 | 5.046 ± 2.126 |
| block_shift | 0.30 | 3.825 ± 2.774 | 3.823 ± 2.805 | 3.871 ± 2.762 | 3.884 ± 2.755 | 3.836 ± 2.768 |
| block_shift | 0.50 | 5.651 ± 1.962 | 5.640 ± 1.980 | 5.613 ± 1.939 | 5.613 ± 1.938 | 5.648 ± 1.959 |
| none | 0.00 | 1.622 ± 0.556 | 1.680 ± 0.619 | 1.621 ± 0.560 | 1.622 ± 0.575 | 1.623 ± 0.571 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.58 | 0.58 | 0.64 | 0.64 | 0.58 |
| block | 0.50 | 0.76 | 0.76 | 0.78 | 0.78 | 0.76 |
| block_shift | 0.30 | 0.68 | 0.68 | 0.68 | 0.68 | 0.68 |
| block_shift | 0.50 | 0.72 | 0.72 | 0.71 | 0.71 | 0.72 |
| none | 0.00 | 0.87 | 0.87 | 0.88 | 0.88 | 0.87 |
