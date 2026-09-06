# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.993 ± 0.002 |
| block | 0.50 | 0.991 ± 0.005 |
| block_shift | 0.30 | 0.987 ± 0.003 |
| block_shift | 0.50 | 0.982 ± 0.015 |
| none | 0.00 | 0.997 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 62.256 ± 2.366 |
| block | 0.50 | 63.980 ± 3.155 |
| block_shift | 0.30 | 67.586 ± 8.423 |
| block_shift | 0.50 | 65.454 ± 3.846 |
| none | 0.00 | 56.309 ± 3.404 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.871 ± 0.025 |
| block | 0.50 | 0.849 ± 0.028 |
| block_shift | 0.30 | 0.841 ± 0.060 |
| block_shift | 0.50 | 0.812 ± 0.046 |
| none | 0.00 | 0.911 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.727 ± 0.046 |
| block | 0.50 | 0.686 ± 0.069 |
| block_shift | 0.30 | 0.706 ± 0.063 |
| block_shift | 0.50 | 0.673 ± 0.087 |
| none | 0.00 | 0.816 ± 0.021 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 4.732 ± 0.984 |
| block | 0.50 | 4.942 ± 0.698 |
| block_shift | 0.30 | 6.463 ± 1.656 |
| block_shift | 0.50 | 6.814 ± 1.170 |
| none | 0.00 | 2.709 ± 0.493 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.996 ± 0.006 |
| block | 0.50 | 0.991 ± 0.010 |
| block_shift | 0.30 | 0.990 ± 0.008 |
| block_shift | 0.50 | 0.925 ± 0.051 |
| none | 0.00 | 1.000 ± 0.000 |
