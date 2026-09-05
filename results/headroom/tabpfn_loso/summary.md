# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.982 ± 0.012 |
| block | 0.50 | 0.980 ± 0.011 |
| block_shift | 0.30 | 0.981 ± 0.007 |
| block_shift | 0.50 | 0.980 ± 0.011 |
| none | 0.00 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 63.191 ± 3.417 |
| block | 0.50 | 65.606 ± 3.761 |
| block_shift | 0.30 | 67.857 ± 8.202 |
| block_shift | 0.50 | 66.952 ± 5.313 |
| none | 0.00 | 56.195 ± 3.086 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.867 ± 0.022 |
| block | 0.50 | 0.842 ± 0.034 |
| block_shift | 0.30 | 0.836 ± 0.062 |
| block_shift | 0.50 | 0.816 ± 0.048 |
| none | 0.00 | 0.916 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.720 ± 0.054 |
| block | 0.50 | 0.683 ± 0.067 |
| block_shift | 0.30 | 0.690 ± 0.074 |
| block_shift | 0.50 | 0.665 ± 0.095 |
| none | 0.00 | 0.806 ± 0.028 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 5.672 ± 1.274 |
| block | 0.50 | 6.292 ± 0.809 |
| block_shift | 0.30 | 6.744 ± 1.121 |
| block_shift | 0.50 | 7.199 ± 1.095 |
| none | 0.00 | 2.698 ± 0.423 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn |
|---|---|---|
| block | 0.30 | 0.979 ± 0.035 |
| block | 0.50 | 0.992 ± 0.008 |
| block_shift | 0.30 | 0.988 ± 0.013 |
| block_shift | 0.50 | 0.927 ± 0.061 |
| none | 0.00 | 1.000 ± 0.001 |
