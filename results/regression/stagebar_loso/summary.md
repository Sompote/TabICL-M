# Missingness ablation

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 63.628 ± 3.331 | 63.525 ± 3.187 |
| block | 0.50 | 64.597 ± 2.895 | 64.534 ± 2.653 |
| block_shift | 0.30 | 65.870 ± 6.911 | 65.786 ± 6.979 |
| block_shift | 0.50 | 65.571 ± 4.749 | 65.515 ± 4.495 |
| none | 0.00 | 56.194 ± 3.480 | 56.228 ± 3.459 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 |
| block | 0.50 | 0.83 | 0.82 |
| block_shift | 0.30 | 0.77 | 0.77 |
| block_shift | 0.50 | 0.85 | 0.84 |
| none | 0.00 | 0.80 | 0.80 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.215 ± 0.028 | 0.215 ± 0.028 |
| block | 0.50 | 0.249 ± 0.007 | 0.249 ± 0.007 |
| block_shift | 0.30 | 0.234 ± 0.024 | 0.234 ± 0.024 |
| block_shift | 0.50 | 0.236 ± 0.016 | 0.235 ± 0.016 |
| none | 0.00 | 0.081 ± 0.003 | 0.080 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.79 | 0.79 |
| block | 0.50 | 0.80 | 0.80 |
| block_shift | 0.30 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.81 | 0.80 |
| none | 0.00 | 0.81 | 0.81 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 2606.032 ± 1166.730 | 2638.372 ± 1171.323 |
| block | 0.50 | 1448.076 ± 272.839 | 1412.699 ± 228.689 |
| block_shift | 0.30 | 2321.662 ± 808.273 | 2301.160 ± 796.547 |
| block_shift | 0.50 | 2132.385 ± 564.246 | 2072.457 ± 511.203 |
| none | 0.00 | 714.564 ± 112.408 | 707.501 ± 100.082 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.83 | 0.82 |
| block | 0.50 | 0.95 | 0.95 |
| block_shift | 0.30 | 0.80 | 0.82 |
| block_shift | 0.50 | 0.86 | 0.87 |
| none | 0.00 | 0.83 | 0.82 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 1.079 ± 0.131 | 1.079 ± 0.131 |
| block | 0.50 | 1.137 ± 0.113 | 1.140 ± 0.111 |
| block_shift | 0.30 | 1.136 ± 0.091 | 1.136 ± 0.091 |
| block_shift | 0.50 | 1.352 ± 0.047 | 1.352 ± 0.049 |
| none | 0.00 | 0.842 ± 0.019 | 0.841 ± 0.019 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.86 | 0.86 |
| block | 0.50 | 0.87 | 0.87 |
| block_shift | 0.30 | 0.84 | 0.84 |
| block_shift | 0.50 | 0.72 | 0.72 |
| none | 0.00 | 0.81 | 0.81 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.186 ± 0.050 | 0.186 ± 0.049 |
| block | 0.50 | 0.185 ± 0.018 | 0.185 ± 0.018 |
| block_shift | 0.30 | 0.190 ± 0.034 | 0.191 ± 0.036 |
| block_shift | 0.50 | 0.187 ± 0.014 | 0.187 ± 0.014 |
| none | 0.00 | 0.108 ± 0.012 | 0.108 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.83 | 0.83 |
| block | 0.50 | 0.83 | 0.83 |
| block_shift | 0.30 | 0.78 | 0.77 |
| block_shift | 0.50 | 0.80 | 0.80 |
| none | 0.00 | 0.78 | 0.79 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 5.305 ± 0.714 | 5.237 ± 0.705 |
| block | 0.50 | 5.548 ± 0.684 | 5.543 ± 0.674 |
| block_shift | 0.30 | 5.708 ± 0.501 | 5.714 ± 0.504 |
| block_shift | 0.50 | 6.629 ± 1.244 | 6.610 ± 1.252 |
| none | 0.00 | 2.816 ± 0.541 | 2.817 ± 0.535 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.81 | 0.81 |
| block | 0.50 | 0.85 | 0.86 |
| block_shift | 0.30 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.85 | 0.85 |
| none | 0.00 | 0.81 | 0.80 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 4.653 ± 3.542 | 4.469 ± 3.264 |
| block | 0.50 | 4.971 ± 2.542 | 4.868 ± 2.440 |
| block_shift | 0.30 | 3.972 ± 2.737 | 4.044 ± 2.692 |
| block_shift | 0.50 | 5.595 ± 1.957 | 5.551 ± 1.968 |
| none | 0.00 | 1.940 ± 0.609 | 1.941 ± 0.608 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_n32 |
|---|---|---|---|
| block | 0.30 | 0.64 | 0.68 |
| block | 0.50 | 0.81 | 0.83 |
| block_shift | 0.30 | 0.76 | 0.70 |
| block_shift | 0.50 | 0.76 | 0.76 |
| none | 0.00 | 0.96 | 0.96 |
