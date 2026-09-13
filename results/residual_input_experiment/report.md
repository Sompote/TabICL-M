# Residual input encoder: ordinary regression experiment

Equal-step comparison: 2,000 continuation steps per arm, same starting weights and training seeds.
Seven development datasets, three evaluation seeds, 3,000-row cap, eight estimators.
Positive gain means lower RMSE for the residual encoder; average paired gains within each dataset, then equally across datasets.
No fresh TabPFN-3 comparison. One training seed and reused development data; independent validation is still required.

| Split | Condition | RMSE gain (%) | Datasets won | Coverage change | Width ratio | Control / new seconds |
|---|---|---:|---:|---:|---:|---:|
| random | block | -0.031 | 3/7 | -0.001 | 0.998 | 0.385 / 0.389 |
| random | block_shift | +0.045 | 3/7 | -0.003 | 0.997 | 0.382 / 0.367 |
| random | none | +0.076 | 4/7 | +0.001 | 1.001 | 0.388 / 0.390 |
| source | block | -0.459 | 2/7 | -0.002 | 1.005 | 0.382 / 0.382 |
| source | block_shift | +0.591 | 7/7 | +0.003 | 0.990 | 0.378 / 0.380 |

Meets advancement criteria: **False**.
Criteria: complete-data mean gain ≥1%, wins on ≥5/7 datasets, and no held-out-source mean degradation >2%.
80% interval coverage and width are diagnostics, not optimized selection metrics.
See manifest.json for parameter counts and timing_*.json for elapsed training time (includes startup and data generation).
