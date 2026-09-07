# 20-dataset benchmark

Block and block_shift missingness at rates 0.3 / 0.5, 5 seeds. Rank 1 = best per condition; `tabicl_aware` = source-aware TabICL-M, `_ewt` = transductive column embedding, `_si` = self-imputation.

## Leave-one-source-out, all: 399 conditions

| model | mean rank | times first |
|---|---|---|
| `tabpfn3` | 2.28 | 134 |
| `tabicl_aware` | 2.32 | 112 |
| `tabpfn25` | 2.59 | 84 |
| `tabicl_impute` | 3.15 | 54 |
| `catboost` | 4.66 | 12 |

- `tabicl_aware` paired: vs `tabpfn25`: 219/177 (55%), datasets won 16/20; vs `tabpfn3`: 190/206 (48%), datasets won 12/20; vs `tabicl_impute`: 281/116 (70%), datasets won 18/20

## Leave-one-source-out, block_shift only: 200 conditions

| model | mean rank | times first |
|---|---|---|
| `tabicl_aware` | 2.22 | 64 |
| `tabpfn3` | 2.45 | 53 |
| `tabpfn25` | 2.53 | 51 |
| `tabicl_impute` | 3.21 | 23 |
| `catboost` | 4.59 | 9 |

- `tabicl_aware` paired: vs `tabpfn25`: 115/85 (57%), datasets won 15/20; vs `tabpfn3`: 105/95 (52%), datasets won 14/20; vs `tabicl_impute`: 151/49 (76%), datasets won 18/20

## Leave-one-source-out, block only: 199 conditions

| model | mean rank | times first |
|---|---|---|
| `tabpfn3` | 2.11 | 81 |
| `tabicl_aware` | 2.42 | 48 |
| `tabpfn25` | 2.65 | 33 |
| `tabicl_impute` | 3.09 | 31 |
| `catboost` | 4.73 | 3 |

- `tabicl_aware` paired: vs `tabpfn25`: 104/92 (52%), datasets won 12/20; vs `tabpfn3`: 85/111 (43%), datasets won 9/20; vs `tabicl_impute`: 130/67 (65%), datasets won 18/20

## Leave-one-source-out: per-dataset means, block_shift@0.5

| dataset | `tabicl_impute` | `tabicl_aware` | `tabpfn25` | `tabpfn3` | `catboost` |
|---|---|---|---|---|---|
| breast_cancer | 0.963 | **0.985** | 0.984 | 0.982 | 0.955 |
| diabetes (RMSE) | 69.102 | **65.124** | 65.559 | 65.454 | 78.813 |
| openml:1063 | 0.858 | **0.869** | 0.857 | 0.866 | 0.600 |
| openml:1067 | 0.789 | 0.803 | **0.803** | 0.803 | 0.745 |
| openml:1461 | **0.748** | 0.744 | 0.734 | 0.734 | 0.634 |
| openml:1480 | 0.694 | 0.682 | **0.703** | 0.679 | 0.537 |
| openml:1494 | 0.879 | **0.892** | 0.886 | 0.887 | 0.817 |
| openml:1590 | 0.800 | 0.815 | **0.822** | 0.812 | 0.783 |
| openml:189 (RMSE) | 0.239 | **0.234** | 0.238 | 0.235 | 0.278 |
| openml:23 | 0.642 | **0.655** | 0.653 | 0.643 | 0.591 |
| openml:31 | 0.683 | **0.685** | 0.679 | 0.673 | 0.624 |
| openml:37 | 0.705 | 0.701 | 0.699 | **0.708** | 0.562 |
| openml:40701 | 0.651 | **0.696** | 0.682 | 0.668 | 0.635 |
| openml:40994 | 0.759 | **0.773** | 0.744 | 0.738 | 0.673 |
| openml:42225 (RMSE) | 2934.625 | 2207.693 | 2339.765 | **2162.967** | 3028.898 |
| openml:44970 (RMSE) | 1.430 | **1.346** | 1.388 | 1.347 | 1.511 |
| openml:507 (RMSE) | 0.204 | **0.186** | 0.197 | 0.199 | 0.235 |
| openml:531 (RMSE) | 7.076 | **6.716** | 6.749 | 6.814 | 9.488 |
| openml:560 (RMSE) | 6.159 | 5.651 | 5.559 | **5.359** | 8.318 |
| wine | 0.914 | **0.941** | 0.935 | 0.925 | 0.806 |

## Random split, all: 399 conditions

| model | mean rank | times first |
|---|---|---|
| `tabpfn3` | 2.22 | 144 |
| `tabicl_aware` | 2.51 | 98 |
| `tabpfn25` | 2.71 | 77 |
| `tabicl_impute` | 2.85 | 60 |
| `catboost` | 4.71 | 11 |

- `tabicl_aware` paired: vs `tabpfn25`: 212/179 (53%), datasets won 16/20; vs `tabpfn3`: 173/218 (43%), datasets won 9/20; vs `tabicl_impute`: 224/165 (56%), datasets won 15/20

## Random split, block_shift only: 200 conditions

| model | mean rank | times first |
|---|---|---|
| `tabpfn3` | 2.26 | 69 |
| `tabicl_aware` | 2.47 | 56 |
| `tabpfn25` | 2.62 | 41 |
| `tabicl_impute` | 2.94 | 25 |
| `catboost` | 4.71 | 4 |

- `tabicl_aware` paired: vs `tabpfn25`: 102/94 (51%), datasets won 13/20; vs `tabpfn3`: 90/105 (45%), datasets won 7/20; vs `tabicl_impute`: 120/76 (60%), datasets won 15/20

## Random split, block only: 199 conditions

| model | mean rank | times first |
|---|---|---|
| `tabpfn3` | 2.17 | 75 |
| `tabicl_aware` | 2.55 | 42 |
| `tabicl_impute` | 2.76 | 35 |
| `tabpfn25` | 2.81 | 36 |
| `catboost` | 4.72 | 7 |

- `tabicl_aware` paired: vs `tabpfn25`: 110/85 (55%), datasets won 15/20; vs `tabpfn3`: 83/113 (42%), datasets won 7/20; vs `tabicl_impute`: 104/89 (52%), datasets won 11/20

## Random split: per-dataset means, block_shift@0.5

| dataset | `tabicl_impute` | `tabicl_aware` | `tabpfn25` | `tabpfn3` | `catboost` |
|---|---|---|---|---|---|
| breast_cancer | 0.994 | 0.994 | 0.995 | **0.995** | 0.990 |
| diabetes (RMSE) | 64.778 | 64.148 | 64.110 | **63.719** | 69.409 |
| openml:1063 | 0.828 | **0.836** | 0.833 | 0.832 | 0.764 |
| openml:1067 | 0.779 | 0.783 | **0.783** | 0.780 | 0.755 |
| openml:1461 | 0.816 | 0.819 | **0.820** | 0.818 | 0.794 |
| openml:1480 | 0.708 | 0.708 | 0.708 | **0.710** | 0.677 |
| openml:1494 | 0.910 | **0.913** | 0.909 | 0.909 | 0.888 |
| openml:1590 | 0.859 | **0.860** | 0.859 | 0.858 | 0.843 |
| openml:189 (RMSE) | 0.221 | 0.221 | 0.220 | **0.219** | 0.226 |
| openml:23 | 0.675 | 0.679 | **0.681** | 0.678 | 0.650 |
| openml:31 | 0.727 | 0.725 | **0.727** | 0.720 | 0.695 |
| openml:37 | 0.730 | **0.738** | 0.738 | 0.731 | 0.712 |
| openml:40701 | 0.813 | 0.818 | 0.819 | **0.822** | 0.791 |
| openml:40994 | 0.866 | 0.880 | 0.865 | **0.881** | 0.787 |
| openml:42225 (RMSE) | 1098.751 | 1114.001 | 1096.384 | **1091.354** | 1225.923 |
| openml:44970 (RMSE) | **1.101** | 1.102 | 1.101 | 1.102 | 1.131 |
| openml:507 (RMSE) | 0.168 | 0.169 | 0.167 | **0.166** | 0.172 |
| openml:531 (RMSE) | 4.700 | **4.616** | 4.667 | 4.632 | 5.077 |
| openml:560 (RMSE) | 3.890 | 3.738 | 3.738 | **3.636** | 4.016 |
| wine | **0.989** | 0.988 | 0.989 | 0.986 | 0.981 |
