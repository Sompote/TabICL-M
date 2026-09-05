# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.985 ± 0.008 |
| block | 0.50 | 0.982 ± 0.010 |
| block_shift | 0.30 | 0.979 ± 0.009 |
| block_shift | 0.50 | 0.977 ± 0.012 |
| none | 0.00 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 64.042 ± 3.566 |
| block | 0.50 | 66.024 ± 4.043 |
| block_shift | 0.30 | 65.768 ± 6.280 |
| block_shift | 0.50 | 70.078 ± 7.782 |
| none | 0.00 | 56.195 ± 3.086 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.862 ± 0.022 |
| block | 0.50 | 0.839 ± 0.034 |
| block_shift | 0.30 | 0.844 ± 0.052 |
| block_shift | 0.50 | 0.815 ± 0.046 |
| none | 0.00 | 0.916 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.719 ± 0.056 |
| block | 0.50 | 0.691 ± 0.074 |
| block_shift | 0.30 | 0.677 ± 0.096 |
| block_shift | 0.50 | 0.664 ± 0.093 |
| none | 0.00 | 0.806 ± 0.028 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 5.719 ± 0.864 |
| block | 0.50 | 6.739 ± 1.096 |
| block_shift | 0.30 | 6.514 ± 1.517 |
| block_shift | 0.50 | 7.128 ± 0.840 |
| none | 0.00 | 2.698 ± 0.423 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.977 ± 0.041 |
| block | 0.50 | 0.990 ± 0.010 |
| block_shift | 0.30 | 0.987 ± 0.012 |
| block_shift | 0.50 | 0.929 ± 0.065 |
| none | 0.00 | 1.000 ± 0.001 |
