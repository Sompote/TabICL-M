# Regression against TabPFN-3

7 regression datasets, block and block_shift at 0.3 / 0.5, 5 seeds; rank 1 = best (lower RMSE). `block_shift` (a held-out source with its own measurement offset) is the case the source-aware parts target.

## Leave-one-source-out, all: 140 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabicl_aware_n32_ypow_4c3500` | 4.60 | 13 | 67/73 | 3/7 | 140 |
| `tabpfn3_n32` | 4.69 | 32 | 78/62 | 5/7 | 140 |
| `tabpfn3` | 4.87 | 34 | — | — | 140 |
| `tabicl_aware_n32_ypow` | 4.95 | 2 | 69/71 | 3/7 | 140 |
| `tabicl_aware_n32` | 5.02 | 0 | 67/73 | 3/7 | 140 |
| `tabicl_aware_4c3500` | 5.05 | 12 | 67/73 | 3/7 | 140 |
| `tabicl_aware_ypow` | 5.13 | 5 | 66/74 | 3/7 | 140 |
| `tabicl_aware` | 5.15 | 3 | 67/73 | 3/7 | 140 |
| `tabicl_aware_med` | 5.54 | 38 | 61/79 | 3/7 | 140 |

Best of ours `tabicl_aware_n32_ypow_4c3500` vs `tabpfn3_n32`: 70/70 paired, datasets won 3/7, mean RMSE -2.85 % (positive = ours lower) -> **BEHIND**

## Leave-one-source-out, with source offset: 70 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabicl_aware_4c3500` | 4.34 | 10 | 46/24 | 5/7 | 70 |
| `tabicl_aware_n32_ypow_4c3500` | 4.36 | 9 | 45/25 | 5/7 | 70 |
| `tabicl_aware_n32` | 4.71 | 0 | 44/26 | 5/7 | 70 |
| `tabicl_aware` | 4.71 | 3 | 44/26 | 5/7 | 70 |
| `tabicl_aware_n32_ypow` | 4.94 | 0 | 44/26 | 5/7 | 70 |
| `tabicl_aware_ypow` | 5.01 | 2 | 44/26 | 5/7 | 70 |
| `tabicl_aware_med` | 5.09 | 24 | 40/30 | 4/7 | 70 |
| `tabpfn3_n32` | 5.90 | 10 | 40/30 | 4/7 | 70 |
| `tabpfn3` | 5.96 | 11 | — | — | 70 |

Best of ours `tabicl_aware_n32_ypow_4c3500` vs `tabpfn3_n32`: 49/21 paired, datasets won 4/7, mean RMSE +2.15 % (positive = ours lower) -> **AHEAD**

## Leave-one-source-out, no offset: 70 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabpfn3_n32` | 3.47 | 22 | 38/32 | 5/7 | 70 |
| `tabpfn3` | 3.79 | 23 | — | — | 70 |
| `tabicl_aware_n32_ypow_4c3500` | 4.84 | 4 | 22/48 | 2/7 | 70 |
| `tabicl_aware_n32_ypow` | 4.96 | 2 | 25/45 | 2/7 | 70 |
| `tabicl_aware_ypow` | 5.25 | 3 | 22/48 | 2/7 | 70 |
| `tabicl_aware_n32` | 5.34 | 0 | 23/47 | 2/7 | 70 |
| `tabicl_aware` | 5.59 | 0 | 23/47 | 2/7 | 70 |
| `tabicl_aware_4c3500` | 5.76 | 2 | 21/49 | 2/7 | 70 |
| `tabicl_aware_med` | 6.00 | 14 | 21/49 | 3/7 | 70 |

Best of ours `tabicl_aware_n32_ypow` vs `tabpfn3_n32`: 21/49 paired, datasets won 2/7, mean RMSE -8.31 % (positive = ours lower) -> **BEHIND**

### Leave-one-source-out: per-dataset means at rate 0.5

| dataset | mechanism | `tabicl_aware` | `tabicl_aware_4c3500` | `tabicl_aware_med` | `tabicl_aware_n32` | `tabicl_aware_n32_ypow` | `tabicl_aware_n32_ypow_4c3500` | `tabicl_aware_ypow` | `tabpfn3` | `tabpfn3_n32` |
|---|---|---|---|---|---|---|---|---|---|---|
| diabetes | block | 64.111 | 64.274 | **63.725** | 64.040 | 64.073 | 64.200 | 64.134 | 63.980 | 63.840 |
| diabetes | block_shift | 65.124 | 65.077 | 65.204 | 65.058 | 65.061 | **65.053** | 65.136 | 65.454 | 65.558 |
| openml:189 | block | 0.249 | 0.250 | 0.249 | 0.249 | **0.249** | 0.249 | 0.249 | 0.250 | 0.250 |
| openml:189 | block_shift | 0.234 | 0.235 | 0.235 | 0.234 | **0.234** | 0.234 | 0.234 | 0.235 | 0.235 |
| openml:42225 | block | 1463.375 | 1444.566 | 1538.244 | 1425.110 | 1416.240 | 1405.651 | 1452.023 | 1292.578 | **1291.293** |
| openml:42225 | block_shift | 2207.693 | 2181.016 | 2191.633 | 2169.169 | 2171.965 | 2158.415 | 2201.133 | 2162.967 | **2087.939** |
| openml:44970 | block | 1.132 | 1.136 | **1.127** | 1.133 | 1.134 | 1.138 | 1.132 | 1.135 | 1.133 |
| openml:44970 | block_shift | 1.346 | **1.339** | 1.339 | 1.346 | 1.347 | 1.341 | 1.346 | 1.347 | 1.346 |
| openml:507 | block | 0.185 | **0.185** | 0.185 | 0.185 | 0.185 | 0.185 | 0.185 | 0.211 | 0.209 |
| openml:507 | block_shift | 0.186 | 0.186 | **0.186** | 0.186 | 0.186 | 0.186 | 0.186 | 0.199 | 0.200 |
| openml:531 | block | 5.675 | 5.593 | 5.863 | 5.668 | 5.688 | 5.585 | 5.699 | **4.942** | 4.946 |
| openml:531 | block_shift | 6.716 | **6.689** | 7.031 | 6.722 | 6.718 | 6.694 | 6.711 | 6.814 | 6.822 |
| openml:560 | block | 5.044 | 5.035 | 4.983 | 4.955 | 4.955 | 4.958 | 5.046 | **4.526** | 4.540 |
| openml:560 | block_shift | 5.651 | 5.623 | 5.640 | 5.613 | 5.613 | 5.589 | 5.648 | 5.359 | **5.302** |

## Random split, all: 138 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabpfn3` | 3.51 | 42 | — | — | 140 |
| `tabpfn3_n32` | 3.58 | 50 | 74/66 | 5/7 | 140 |
| `tabicl_aware_n32_ypow_4c3500` | 4.70 | 8 | 43/97 | 1/7 | 140 |
| `tabicl_aware_n32_ypow` | 4.73 | 9 | 42/98 | 1/7 | 140 |
| `tabicl_aware_ypow` | 5.07 | 8 | 42/98 | 1/7 | 140 |
| `tabicl_aware_n32` | 5.09 | 4 | 40/98 | 0/7 | 138 |
| `tabicl_aware_4c3500` | 5.33 | 7 | 41/99 | 1/7 | 140 |
| `tabicl_aware` | 5.42 | 2 | 42/98 | 1/7 | 140 |
| `tabicl_aware_med` | 7.57 | 8 | 30/110 | 0/7 | 140 |
| `tabicl_aware_n32_ypow_qn` | — | — | 31/53 | 3/7 | 84 |

Best of ours `tabicl_aware_n32_ypow_qn` vs `tabpfn3_n32`: 30/54 paired, datasets won 3/7, mean RMSE -0.55 % (positive = ours lower) -> **BEHIND**

### Random split: per-dataset means at rate 0.5

| dataset | mechanism | `tabicl_aware` | `tabicl_aware_4c3500` | `tabicl_aware_med` | `tabicl_aware_n32` | `tabicl_aware_n32_ypow` | `tabicl_aware_n32_ypow_4c3500` | `tabicl_aware_n32_ypow_qn` | `tabicl_aware_ypow` | `tabpfn3` | `tabpfn3_n32` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| diabetes | block | 64.716 | 64.757 | 65.527 | 64.685 | 64.668 | 64.730 | **63.998** | 64.696 | 64.213 | 64.230 |
| diabetes | block_shift | 64.148 | 64.221 | 64.466 | 64.231 | 64.237 | 64.330 | **63.499** | 64.159 | 63.719 | 63.698 |
| openml:189 | block | 0.226 | 0.226 | 0.227 | 0.226 | 0.226 | 0.226 | **0.223** | 0.226 | 0.225 | 0.225 |
| openml:189 | block_shift | 0.221 | 0.221 | 0.222 | 0.221 | 0.221 | 0.221 | 0.220 | 0.221 | 0.219 | **0.219** |
| openml:42225 | block | 1214.415 | 1217.512 | 1233.445 | 1214.177 | 1211.412 | 1213.542 | 1234.509 | 1212.760 | 1199.662 | **1198.890** |
| openml:42225 | block_shift | 1114.001 | 1118.183 | 1130.054 | 1112.568 | 1110.906 | 1114.159 | 1174.397 | 1112.571 | 1091.354 | **1090.677** |
| openml:44970 | block | 1.102 | 1.102 | 1.109 | 1.102 | 1.102 | 1.102 | **1.098** | 1.102 | 1.099 | 1.098 |
| openml:44970 | block_shift | 1.102 | 1.103 | 1.108 | 1.101 | 1.101 | 1.102 | **1.069** | 1.101 | 1.102 | 1.101 |
| openml:507 | block | 0.155 | 0.155 | 0.156 | 0.155 | 0.155 | 0.155 | 0.163 | 0.155 | 0.153 | **0.153** |
| openml:507 | block_shift | 0.169 | 0.168 | 0.169 | 0.169 | 0.169 | 0.168 | 0.173 | 0.169 | **0.166** | 0.166 |
| openml:531 | block | 4.770 | 4.771 | 4.797 | 4.764 | 4.756 | **4.753** | 4.948 | 4.763 | 4.899 | 4.890 |
| openml:531 | block_shift | 4.616 | 4.623 | 4.663 | **4.599** | 4.605 | 4.614 | 4.805 | 4.615 | 4.632 | 4.614 |
| openml:560 | block | **4.026** | 4.028 | 4.043 | 4.029 | 4.032 | 4.032 | 4.494 | 4.028 | 4.029 | 4.030 |
| openml:560 | block_shift | 3.738 | 3.751 | 3.770 | 3.751 | 3.733 | 3.749 | **3.412** | 3.721 | 3.636 | 3.655 |
