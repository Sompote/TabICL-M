# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.997 ± 0.004 |
| block | 0.50 | 0.995 ± 0.005 |
| block_shift | 0.30 | 0.993 ± 0.005 |
| block_shift | 0.50 | 0.993 ± 0.006 |
| none | 0.00 | 0.996 ± 0.004 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 59.177 ± 2.990 |
| block | 0.50 | 64.971 ± 3.782 |
| block_shift | 0.30 | 59.202 ± 1.006 |
| block_shift | 0.50 | 64.831 ± 2.965 |
| none | 0.00 | 56.235 ± 3.545 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.895 ± 0.013 |
| block | 0.50 | 0.863 ± 0.010 |
| block_shift | 0.30 | 0.892 ± 0.004 |
| block_shift | 0.50 | 0.858 ± 0.025 |
| none | 0.00 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.769 ± 0.057 |
| block | 0.50 | 0.727 ± 0.036 |
| block_shift | 0.30 | 0.772 ± 0.029 |
| block_shift | 0.50 | 0.726 ± 0.031 |
| none | 0.00 | 0.817 ± 0.025 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 3.761 ± 0.529 |
| block | 0.50 | 4.953 ± 0.655 |
| block_shift | 0.30 | 4.380 ± 0.584 |
| block_shift | 0.50 | 4.716 ± 0.867 |
| none | 0.00 | 2.764 ± 0.408 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.997 ± 0.005 |
| block | 0.50 | 0.996 ± 0.006 |
| block_shift | 0.30 | 0.995 ± 0.007 |
| block_shift | 0.50 | 0.988 ± 0.025 |
| none | 0.00 | 0.999 ± 0.001 |
