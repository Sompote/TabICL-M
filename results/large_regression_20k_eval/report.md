# Large 20k regression evaluation

Large: 18 ICL blocks, 41.5M parameters, 20,000 continuation steps. Original: retained 12-block checkpoint.
Both TabICL models evaluated freshly with 8 estimators, seven development datasets, seeds 0–2, and a 3,000-row cap.
TabPFN-3 results are archived under matching recorded protocols; they were not rerun and cannot support runtime comparisons.
Positive gain means lower RMSE for Large. Average paired percentage gains within each dataset, then average equally across datasets.
Complete-data rows are duplicated across the two split reports and must not be counted twice.
This comparison combines extra capacity and 20k extra training; it does not isolate the effect of architecture. One pretraining seed; no untouched test benchmark or automatic promotion.

| Split | Missingness | Reference | RMSE gain (%) | Wins / pairs | Datasets won |
|---|---|---|---:|---:|---:|
| random | block | original | -0.082 | 26/42 | 3/7 |
| random | block_shift | original | -0.167 | 30/42 | 4/7 |
| random | none | original | -2.202 | 4/21 | 2/7 |
| random | block | tabpfn3_archived | -0.583 | 11/42 | 2/7 |
| random | block_shift | tabpfn3_archived | -1.430 | 12/42 | 1/7 |
| random | none | tabpfn3_archived | -3.486 | 7/21 | 2/7 |
| source | block | original | +2.809 | 29/42 | 7/7 |
| source | block_shift | original | +9.195 | 40/42 | 7/7 |
| source | block | tabpfn3_archived | -5.452 | 14/42 | 1/7 |
| source | block_shift | tabpfn3_archived | +13.518 | 36/42 | 7/7 |

## Complete-data RMSE

| Dataset | Original | Large | Archived TabPFN-3 |
|---|---:|---:|---:|
| diabetes | 56.84266 | 56.94541 | 57.02582 |
| openml:189 | 0.07609 | 0.07658 | 0.07212 |
| openml:42225 | 636.22801 | 635.02535 | 617.29730 |
| openml:44970 | 0.84862 | 0.85341 | 0.84355 |
| openml:507 | 0.11404 | 0.11364 | 0.09857 |
| openml:531 | 2.99932 | 3.07335 | 3.04483 |
| openml:560 | 1.87273 | 2.09274 | 2.14137 |
