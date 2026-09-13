# Ordinary Large on held-out sources

New model: completed 20k ordinary-regression continuation. Previous Large: its missing-aware starting checkpoint.
Seven development datasets; seeds 0–2; eight estimators; 3,000-row cap; held-out synthetic sources; block missingness at 30% and 50%, with and without measurement shifts.
New scores use CPU inference while the architecture experiment uses the GPU. References reuse previous GPU results under the matching recorded protocol; device/precision differences are a limitation. No runtime comparisons.
Positive gain means lower RMSE for ordinary Large. Average paired gains within datasets, then equally across datasets.
One training seed, reused development datasets, and injected source effects; no generalization claim or automatic model promotion.

| Reference | Held-out condition | New model RMSE gain (%) | Datasets won | Wins / pairs |
|---|---|---:|---:|---:|
| previous_missing_large | block | -9.886 | 1/7 | 16/42 |
| previous_missing_large | block_shift | -12.977 | 0/7 | 6/42 |
| original_tabicl_m | block | -5.715 | 1/7 | 18/42 |
| original_tabicl_m | block_shift | -1.096 | 5/7 | 30/42 |
| tabpfn3_archived | block | -16.080 | 1/7 | 7/42 |
| tabpfn3_archived | block_shift | +5.135 | 7/7 | 33/42 |
