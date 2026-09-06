# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.992 ± 0.003 |
| block | 0.50 | 0.988 ± 0.008 |
| block_shift | 0.30 | 0.985 ± 0.004 |
| block_shift | 0.50 | 0.977 ± 0.017 |
| none | 0.00 | 0.996 ± 0.004 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 63.399 ± 3.847 |
| block | 0.50 | 65.414 ± 3.735 |
| block_shift | 0.30 | 67.615 ± 8.113 |
| block_shift | 0.50 | 67.542 ± 4.055 |
| none | 0.00 | 56.235 ± 3.545 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.868 ± 0.024 |
| block | 0.50 | 0.841 ± 0.027 |
| block_shift | 0.30 | 0.845 ± 0.043 |
| block_shift | 0.50 | 0.811 ± 0.044 |
| none | 0.00 | 0.912 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.721 ± 0.049 |
| block | 0.50 | 0.694 ± 0.073 |
| block_shift | 0.30 | 0.701 ± 0.062 |
| block_shift | 0.50 | 0.663 ± 0.089 |
| none | 0.00 | 0.817 ± 0.025 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 5.627 ± 1.201 |
| block | 0.50 | 6.044 ± 0.774 |
| block_shift | 0.30 | 6.274 ± 0.823 |
| block_shift | 0.50 | 6.954 ± 1.212 |
| none | 0.00 | 2.764 ± 0.408 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn26 |
|---|---|---|
| block | 0.30 | 0.994 ± 0.005 |
| block | 0.50 | 0.990 ± 0.011 |
| block_shift | 0.30 | 0.987 ± 0.008 |
| block_shift | 0.50 | 0.929 ± 0.048 |
| none | 0.00 | 0.999 ± 0.001 |
