# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.992 ± 0.003 |
| block | 0.50 | 0.991 ± 0.005 |
| block_shift | 0.30 | 0.988 ± 0.002 |
| block_shift | 0.50 | 0.984 ± 0.010 |
| none | 0.00 | 0.996 ± 0.004 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 62.798 ± 3.200 |
| block | 0.50 | 63.649 ± 2.537 |
| block_shift | 0.30 | 66.638 ± 8.981 |
| block_shift | 0.50 | 65.559 ± 3.932 |
| none | 0.00 | 56.326 ± 3.379 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.871 ± 0.021 |
| block | 0.50 | 0.845 ± 0.030 |
| block_shift | 0.30 | 0.838 ± 0.060 |
| block_shift | 0.50 | 0.822 ± 0.040 |
| none | 0.00 | 0.915 ± 0.004 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.717 ± 0.051 |
| block | 0.50 | 0.693 ± 0.071 |
| block_shift | 0.30 | 0.696 ± 0.076 |
| block_shift | 0.50 | 0.679 ± 0.090 |
| none | 0.00 | 0.815 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 5.069 ± 0.976 |
| block | 0.50 | 5.862 ± 1.191 |
| block_shift | 0.30 | 6.578 ± 0.832 |
| block_shift | 0.50 | 6.749 ± 0.967 |
| none | 0.00 | 2.715 ± 0.463 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate |  |
|---|---|

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabpfn25 |
|---|---|---|
| block | 0.30 | 0.995 ± 0.007 |
| block | 0.50 | 0.991 ± 0.008 |
| block_shift | 0.30 | 0.990 ± 0.007 |
| block_shift | 0.50 | 0.935 ± 0.051 |
| none | 0.00 | 1.000 ± 0.001 |
