# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.997 ± 0.003 |
| block | 0.50 | 0.995 ± 0.005 |
| block_shift | 0.30 | 0.994 ± 0.004 |
| block_shift | 0.50 | 0.994 ± 0.005 |
| none | 0.00 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 59.448 ± 3.123 |
| block | 0.50 | 64.931 ± 3.553 |
| block_shift | 0.30 | 59.486 ± 1.066 |
| block_shift | 0.50 | 64.656 ± 3.066 |
| none | 0.00 | 56.195 ± 3.086 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.901 ± 0.013 |
| block | 0.50 | 0.869 ± 0.010 |
| block_shift | 0.30 | 0.895 ± 0.004 |
| block_shift | 0.50 | 0.861 ± 0.028 |
| none | 0.00 | 0.916 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.759 ± 0.056 |
| block | 0.50 | 0.731 ± 0.032 |
| block_shift | 0.30 | 0.765 ± 0.025 |
| block_shift | 0.50 | 0.716 ± 0.033 |
| none | 0.00 | 0.806 ± 0.028 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 3.711 ± 0.458 |
| block | 0.50 | 4.868 ± 0.614 |
| block_shift | 0.30 | 4.361 ± 0.618 |
| block_shift | 0.50 | 4.773 ± 0.787 |
| none | 0.00 | 2.698 ± 0.423 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.997 ± 0.005 |
| block | 0.50 | 0.995 ± 0.007 |
| block_shift | 0.30 | 0.993 ± 0.008 |
| block_shift | 0.50 | 0.986 ± 0.024 |
| none | 0.00 | 1.000 ± 0.001 |
