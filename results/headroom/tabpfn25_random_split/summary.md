# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.996 ± 0.004 |
| block_shift | 0.30 | 0.994 ± 0.003 |
| block_shift | 0.50 | 0.995 ± 0.004 |
| none | 0.00 | 0.996 ± 0.004 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 59.127 ± 2.987 |
| block | 0.50 | 64.840 ± 3.556 |
| block_shift | 0.30 | 59.030 ± 0.448 |
| block_shift | 0.50 | 64.110 ± 2.955 |
| none | 0.00 | 56.326 ± 3.379 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.900 ± 0.012 |
| block | 0.50 | 0.868 ± 0.012 |
| block_shift | 0.30 | 0.894 ± 0.005 |
| block_shift | 0.50 | 0.859 ± 0.027 |
| none | 0.00 | 0.915 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.764 ± 0.055 |
| block | 0.50 | 0.728 ± 0.036 |
| block_shift | 0.30 | 0.767 ± 0.029 |
| block_shift | 0.50 | 0.727 ± 0.038 |
| none | 0.00 | 0.815 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 3.766 ± 0.565 |
| block | 0.50 | 4.932 ± 0.581 |
| block_shift | 0.30 | 4.368 ± 0.661 |
| block_shift | 0.50 | 4.667 ± 0.817 |
| none | 0.00 | 2.715 ± 0.463 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.997 ± 0.005 |
| block | 0.50 | 0.995 ± 0.006 |
| block_shift | 0.30 | 0.995 ± 0.006 |
| block_shift | 0.50 | 0.989 ± 0.023 |
| none | 0.00 | 1.000 ± 0.001 |
