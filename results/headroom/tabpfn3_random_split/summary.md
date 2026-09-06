# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.997 ± 0.004 |
| block | 0.50 | 0.996 ± 0.003 |
| block_shift | 0.30 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.995 ± 0.005 |
| none | 0.00 | 0.997 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 58.858 ± 2.757 |
| block | 0.50 | 64.213 ± 3.481 |
| block_shift | 0.30 | 58.554 ± 0.245 |
| block_shift | 0.50 | 63.719 ± 2.751 |
| none | 0.00 | 56.309 ± 3.404 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.899 ± 0.014 |
| block | 0.50 | 0.866 ± 0.011 |
| block_shift | 0.30 | 0.895 ± 0.004 |
| block_shift | 0.50 | 0.858 ± 0.024 |
| none | 0.00 | 0.911 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.764 ± 0.057 |
| block | 0.50 | 0.726 ± 0.036 |
| block_shift | 0.30 | 0.767 ± 0.026 |
| block_shift | 0.50 | 0.720 ± 0.040 |
| none | 0.00 | 0.816 ± 0.021 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 3.639 ± 0.559 |
| block | 0.50 | 4.899 ± 0.589 |
| block_shift | 0.30 | 4.258 ± 0.565 |
| block_shift | 0.50 | 4.632 ± 0.803 |
| none | 0.00 | 2.709 ± 0.493 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn3 |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.994 ± 0.006 |
| block_shift | 0.30 | 0.995 ± 0.006 |
| block_shift | 0.50 | 0.986 ± 0.028 |
| none | 0.00 | 1.000 ± 0.000 |
