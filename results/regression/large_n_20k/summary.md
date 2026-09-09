# Missingness ablation

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_knn |
|---|---|---|---|
| block_shift | 0.30 | 0.169 ± 0.019 | 0.170 ± 0.019 |
| none | 0.00 | 0.065 ± 0.001 | 0.066 ± 0.000 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_knn |
|---|---|---|---|
| block_shift | 0.30 | 0.80 | 0.80 |
| none | 0.00 | 0.80 | 0.80 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_knn |
|---|---|---|---|
| block_shift | 0.30 | 1000.633 ± 105.841 | 1011.040 ± 104.645 |
| none | 0.00 | 538.591 ± 9.941 | 539.923 ± 12.093 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_knn |
|---|---|---|---|
| block_shift | 0.30 | 0.80 | 0.79 |
| none | 0.00 | 0.81 | 0.81 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_knn |
|---|---|---|---|
| block_shift | 0.30 | 0.142 ± 0.006 | 0.142 ± 0.006 |
| none | 0.00 | 0.089 ± 0.002 | 0.089 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_knn |
|---|---|---|---|
| block_shift | 0.30 | 0.78 | 0.78 |
| none | 0.00 | 0.78 | 0.78 |
