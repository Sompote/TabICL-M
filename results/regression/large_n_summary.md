# Large tables: neighbour-based context

kin8nm (8 192 rows), space_ga (3 107) and diamonds (subsampled to 20 000), random 70/30 split, complete and block_shift at rate 0.3, 3 seeds. `_knn` = KNNContextRegressor (4 000 nearest training rows per group of test rows, plain estimator below 4 500 training rows); `_20k` = source-aware regressor (20k steps), `_smooth` = continued on the smooth-target prior with the point loss. RMSE, lower is better.

| dataset | train rows | mechanism | `tabicl_aware_20k` | `tabicl_aware_knn_20k` | `tabpfn3` |
|---|---|---|---|---|---|
| openml:189 | 5734 | block_shift | 0.1693 | 0.1704 | **0.1687** |
| openml:189 | 5734 | none | 0.06548 | 0.06606 | **0.06241** |
| openml:42225 | 14000 | block_shift | 1001 | 1011 | **989.9** |
| openml:42225 | 14000 | none | 538.6 | 539.9 | **524.8** |
| openml:507 | 2174 | block_shift | 0.1416 | 0.1416 | **0.1402** |
| openml:507 | 2174 | none | 0.08924 | 0.08924 | **0.08485** |

## Paired against TabPFN-3

| model | wins/losses | mean RMSE difference (%) | datasets won |
|---|---|---|---|
| `tabicl_aware_20k` | 1/17 | -2.54 | 0/3 |
| `tabicl_aware_knn_20k` | 1/17 | -3.01 | 0/3 |

Neighbour context vs plain context (20k regressor): 1 wins / 11 losses, mean RMSE change +0.46 % (negative = knn better).

Median seconds per fit+predict: `tabicl_aware_20k` 0.4, `tabicl_aware_knn_20k` 1.9, `tabpfn3` 1.0.
