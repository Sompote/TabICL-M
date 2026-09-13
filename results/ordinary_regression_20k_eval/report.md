# Ordinary Large: complete-data regression evaluation

Fresh CPU evaluations of all three checkpoints: seven development datasets, seeds 0–2, eight estimators, 3,000-row cap, 30% test split.
The new model has 20,000 ordinary-regression continuation steps after the missing-aware Large checkpoint.
Positive gain means lower RMSE for ordinary Large. Average paired percentage gains within each dataset, then equally across datasets.
CPU inference may differ numerically from previous GPU evaluations. All comparisons here use fresh CPU baselines.
Architecture training ran concurrently on GPU; recorded runtime is not a controlled speed benchmark.
One training seed and reused development datasets; this does not establish general superiority or performance under missingness/source shifts.

| Reference | Mean RMSE gain (%) | Datasets won | Wins / pairs |
|---|---:|---:|---:|
| missing_large | -0.375 | 4/7 | 12/21 |
| original | -2.669 | 3/7 | 8/21 |

| Dataset | Ordinary Large | Missing-aware Large | Original TabICL-M |
|---|---:|---:|---:|
| diabetes | 56.83658 | 56.94541 | 56.84266 |
| openml:189 | 0.07790 | 0.07658 | 0.07608 |
| openml:42225 | 644.42278 | 635.39556 | 636.44648 |
| openml:44970 | 0.84767 | 0.85341 | 0.84862 |
| openml:507 | 0.11002 | 0.11364 | 0.11404 |
| openml:531 | 3.00208 | 3.07335 | 2.99932 |
| openml:560 | 2.21935 | 2.09274 | 1.87273 |
