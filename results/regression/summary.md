# Regression against TabPFN-3

7 regression datasets, block and block_shift at 0.3 / 0.5, 5 seeds; rank 1 = best (lower RMSE). `block_shift` (a held-out source with its own measurement offset) is the case the source-aware parts target.

## Leave-one-source-out, all: 140 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabicl_aware_n32_ypow_4c3500` | 5.42 | 12 | 67/73 | 3/7 | 140 |
| `tabpfn3_n32` | 5.47 | 28 | 78/62 | 5/7 | 140 |
| `tabpfn3` | 5.68 | 32 | — | — | 140 |
| `tabicl_aware_n32_ypow` | 5.78 | 2 | 69/71 | 3/7 | 140 |
| `tabicl_aware_n32` | 5.86 | 0 | 67/73 | 3/7 | 140 |
| `tabicl_aware_4c3500` | 5.89 | 6 | 67/73 | 3/7 | 140 |
| `tabicl_aware` | 5.97 | 1 | 67/73 | 3/7 | 140 |
| `tabicl_aware_ypow` | 5.97 | 4 | 66/74 | 3/7 | 140 |
| `tabicl_aware_n32_bar` | 6.56 | 8 | 56/84 | 2/7 | 140 |
| `tabicl_aware_med` | 6.61 | 33 | 61/79 | 3/7 | 140 |
| `tabicl_aware_bar` | 6.78 | 11 | 57/83 | 2/7 | 140 |

Best of ours `tabicl_aware_n32_ypow_4c3500` vs `tabpfn3_n32`: 70/70 paired, datasets won 3/7, mean RMSE -2.85 % (positive = ours lower) -> **BEHIND**

## Leave-one-source-out, with source offset: 70 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabicl_aware_4c3500` | 5.13 | 4 | 46/24 | 5/7 | 70 |
| `tabicl_aware_n32_ypow_4c3500` | 5.19 | 8 | 45/25 | 5/7 | 70 |
| `tabicl_aware` | 5.58 | 1 | 44/26 | 5/7 | 70 |
| `tabicl_aware_n32` | 5.65 | 0 | 44/26 | 5/7 | 70 |
| `tabicl_aware_n32_ypow` | 5.85 | 0 | 44/26 | 5/7 | 70 |
| `tabicl_aware_ypow` | 5.88 | 1 | 44/26 | 5/7 | 70 |
| `tabicl_aware_med` | 6.14 | 21 | 40/30 | 4/7 | 70 |
| `tabicl_aware_n32_bar` | 6.22 | 5 | 37/33 | 4/7 | 70 |
| `tabicl_aware_bar` | 6.42 | 9 | 38/32 | 4/7 | 70 |
| `tabpfn3_n32` | 6.91 | 8 | 40/30 | 4/7 | 70 |
| `tabpfn3` | 7.03 | 10 | — | — | 70 |

Best of ours `tabicl_aware_n32_ypow_4c3500` vs `tabpfn3_n32`: 49/21 paired, datasets won 4/7, mean RMSE +2.15 % (positive = ours lower) -> **AHEAD**

## Leave-one-source-out, no offset: 70 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabpfn3_n32` | 4.03 | 20 | 38/32 | 5/7 | 70 |
| `tabpfn3` | 4.33 | 22 | — | — | 70 |
| `tabicl_aware_n32_ypow_4c3500` | 5.66 | 4 | 22/48 | 2/7 | 70 |
| `tabicl_aware_n32_ypow` | 5.71 | 2 | 25/45 | 2/7 | 70 |
| `tabicl_aware_ypow` | 6.06 | 3 | 22/48 | 2/7 | 70 |
| `tabicl_aware_n32` | 6.08 | 0 | 23/47 | 2/7 | 70 |
| `tabicl_aware` | 6.36 | 0 | 23/47 | 2/7 | 70 |
| `tabicl_aware_4c3500` | 6.66 | 2 | 21/49 | 2/7 | 70 |
| `tabicl_aware_n32_bar` | 6.89 | 3 | 19/51 | 2/7 | 70 |
| `tabicl_aware_med` | 7.09 | 12 | 21/49 | 3/7 | 70 |
| `tabicl_aware_bar` | 7.14 | 2 | 19/51 | 2/7 | 70 |

Best of ours `tabicl_aware_n32_ypow` vs `tabpfn3_n32`: 21/49 paired, datasets won 2/7, mean RMSE -8.31 % (positive = ours lower) -> **BEHIND**

### Leave-one-source-out: per-dataset means at rate 0.5

| dataset | mechanism | `tabicl_aware` | `tabicl_aware_4c3500` | `tabicl_aware_bar` | `tabicl_aware_med` | `tabicl_aware_n32` | `tabicl_aware_n32_bar` | `tabicl_aware_n32_ypow` | `tabicl_aware_n32_ypow_4c3500` | `tabicl_aware_ypow` | `tabpfn3` | `tabpfn3_n32` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diabetes | block | 64.111 | 64.274 | 64.597 | **63.725** | 64.040 | 64.534 | 64.073 | 64.200 | 64.134 | 63.980 | 63.840 |
| diabetes | block_shift | 65.124 | 65.077 | 65.571 | 65.204 | 65.058 | 65.515 | 65.061 | **65.053** | 65.136 | 65.454 | 65.558 |
| openml:189 | block | 0.249 | 0.250 | 0.249 | 0.249 | 0.249 | **0.249** | 0.249 | 0.249 | 0.249 | 0.250 | 0.250 |
| openml:189 | block_shift | 0.234 | 0.235 | 0.236 | 0.235 | 0.234 | 0.235 | **0.234** | 0.234 | 0.234 | 0.235 | 0.235 |
| openml:42225 | block | 1463.375 | 1444.566 | 1448.076 | 1538.244 | 1425.110 | 1412.699 | 1416.240 | 1405.651 | 1452.023 | 1292.578 | **1291.293** |
| openml:42225 | block_shift | 2207.693 | 2181.016 | 2132.385 | 2191.633 | 2169.169 | **2072.457** | 2171.965 | 2158.415 | 2201.133 | 2162.967 | 2087.939 |
| openml:44970 | block | 1.132 | 1.136 | 1.137 | **1.127** | 1.133 | 1.140 | 1.134 | 1.138 | 1.132 | 1.135 | 1.133 |
| openml:44970 | block_shift | 1.346 | **1.339** | 1.352 | 1.339 | 1.346 | 1.352 | 1.347 | 1.341 | 1.346 | 1.347 | 1.346 |
| openml:507 | block | 0.185 | 0.185 | **0.185** | 0.185 | 0.185 | 0.185 | 0.185 | 0.185 | 0.185 | 0.211 | 0.209 |
| openml:507 | block_shift | 0.186 | 0.186 | 0.187 | **0.186** | 0.186 | 0.187 | 0.186 | 0.186 | 0.186 | 0.199 | 0.200 |
| openml:531 | block | 5.675 | 5.593 | 5.548 | 5.863 | 5.668 | 5.543 | 5.688 | 5.585 | 5.699 | **4.942** | 4.946 |
| openml:531 | block_shift | 6.716 | 6.689 | 6.629 | 7.031 | 6.722 | **6.610** | 6.718 | 6.694 | 6.711 | 6.814 | 6.822 |
| openml:560 | block | 5.044 | 5.035 | 4.971 | 4.983 | 4.955 | 4.868 | 4.955 | 4.958 | 5.046 | **4.526** | 4.540 |
| openml:560 | block_shift | 5.651 | 5.623 | 5.595 | 5.640 | 5.613 | 5.551 | 5.613 | 5.589 | 5.648 | 5.359 | **5.302** |

## Random split, all: 138 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabpfn3` | 4.04 | 36 | — | — | 140 |
| `tabpfn3_n32` | 4.09 | 46 | 74/66 | 5/7 | 140 |
| `tabicl_aware_n32_ypow_4c3500` | 5.37 | 6 | 43/97 | 1/7 | 140 |
| `tabicl_aware_n32_ypow` | 5.46 | 8 | 42/98 | 1/7 | 140 |
| `tabicl_aware_ypow` | 5.80 | 3 | 42/98 | 1/7 | 140 |
| `tabicl_aware_n32` | 5.81 | 2 | 40/98 | 0/7 | 138 |
| `tabicl_aware_4c3500` | 6.03 | 5 | 41/99 | 1/7 | 140 |
| `tabicl_aware` | 6.14 | 2 | 42/98 | 1/7 | 140 |
| `tabicl_aware_n32_bar` | 7.26 | 9 | 36/104 | 0/7 | 140 |
| `tabicl_aware_bar` | 7.38 | 13 | 37/103 | 0/7 | 140 |
| `tabicl_aware_med` | 8.62 | 8 | 30/110 | 0/7 | 140 |
| `tabicl_aware_n32_ypow_qn` | — | — | 31/53 | 3/7 | 84 |

Best of ours `tabicl_aware_n32_ypow_qn` vs `tabpfn3_n32`: 30/54 paired, datasets won 3/7, mean RMSE -0.55 % (positive = ours lower) -> **BEHIND**

### Random split: per-dataset means at rate 0.5

| dataset | mechanism | `tabicl_aware` | `tabicl_aware_4c3500` | `tabicl_aware_bar` | `tabicl_aware_med` | `tabicl_aware_n32` | `tabicl_aware_n32_bar` | `tabicl_aware_n32_ypow` | `tabicl_aware_n32_ypow_4c3500` | `tabicl_aware_n32_ypow_qn` | `tabicl_aware_ypow` | `tabpfn3` | `tabpfn3_n32` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diabetes | block | 64.716 | 64.757 | 64.884 | 65.527 | 64.685 | 64.841 | 64.668 | 64.730 | **63.998** | 64.696 | 64.213 | 64.230 |
| diabetes | block_shift | 64.148 | 64.221 | 64.474 | 64.466 | 64.231 | 64.517 | 64.237 | 64.330 | **63.499** | 64.159 | 63.719 | 63.698 |
| openml:189 | block | 0.226 | 0.226 | 0.227 | 0.227 | 0.226 | 0.227 | 0.226 | 0.226 | **0.223** | 0.226 | 0.225 | 0.225 |
| openml:189 | block_shift | 0.221 | 0.221 | 0.221 | 0.222 | 0.221 | 0.221 | 0.221 | 0.221 | 0.220 | 0.221 | 0.219 | **0.219** |
| openml:42225 | block | 1214.415 | 1217.512 | 1237.811 | 1233.445 | 1214.177 | 1236.616 | 1211.412 | 1213.542 | 1234.509 | 1212.760 | 1199.662 | **1198.890** |
| openml:42225 | block_shift | 1114.001 | 1118.183 | 1151.508 | 1130.054 | 1112.568 | 1150.521 | 1110.906 | 1114.159 | 1174.397 | 1112.571 | 1091.354 | **1090.677** |
| openml:44970 | block | 1.102 | 1.102 | 1.102 | 1.109 | 1.102 | 1.102 | 1.102 | 1.102 | **1.098** | 1.102 | 1.099 | 1.098 |
| openml:44970 | block_shift | 1.102 | 1.103 | 1.102 | 1.108 | 1.101 | 1.103 | 1.101 | 1.102 | **1.069** | 1.101 | 1.102 | 1.101 |
| openml:507 | block | 0.155 | 0.155 | 0.156 | 0.156 | 0.155 | 0.156 | 0.155 | 0.155 | 0.163 | 0.155 | 0.153 | **0.153** |
| openml:507 | block_shift | 0.169 | 0.168 | 0.169 | 0.169 | 0.169 | 0.169 | 0.169 | 0.168 | 0.173 | 0.169 | **0.166** | 0.166 |
| openml:531 | block | 4.770 | 4.771 | 4.835 | 4.797 | 4.764 | 4.832 | 4.756 | **4.753** | 4.948 | 4.763 | 4.899 | 4.890 |
| openml:531 | block_shift | 4.616 | 4.623 | 4.766 | 4.663 | **4.599** | 4.748 | 4.605 | 4.614 | 4.805 | 4.615 | 4.632 | 4.614 |
| openml:560 | block | **4.026** | 4.028 | 4.088 | 4.043 | 4.029 | 4.088 | 4.032 | 4.032 | 4.494 | 4.028 | 4.029 | 4.030 |
| openml:560 | block_shift | 3.738 | 3.751 | 3.679 | 3.770 | 3.751 | 3.682 | 3.733 | 3.749 | **3.412** | 3.721 | 3.636 | 3.655 |
