# Regression probes: what does not close the gap to TabPFN-3

Complete data, random split, 2100 training rows, seeds 0-2, the runner's exact splits. RMSE, mean over seeds.

## Test-time fine-tuning on the context rows

| model | setting | kin8nm | space_ga |
|---|---|---|---|
| source-aware TabICL-M (20k) | zero-shot | 0.0761 | 0.1140 |
|  | 100 epochs, lr 5e-5 | 0.0736 | 0.1076 |
|  | 100 epochs, lr 1e-4 | 0.0749 | 0.1078 |
|  | 100 epochs, lr 1e-4, ICL stage only | 0.0751 | 0.1103 |
|  | 100 epochs, lr 5e-5, no early stopping | 0.0736 | 0.1059 |
|  | 1000 epochs, lr 5e-5, patience 100 | 0.0741 | 0.1086 |
|  | 1000 epochs, lr 2e-5, patience 100 | 0.0742 | 0.1078 |
|  | 1000 epochs, lr 5e-5, no early stopping | 0.0743 | 0.1083 |
| TabPFN-3 | zero-shot | 0.0721 | 0.0986 |
|  | 30 epochs, lr 1e-5 (its defaults) | 0.0724 | 0.1001 |
|  | 100 epochs, lr 5e-5 | 0.0738 | 0.1028 |

Per seed, best fine-tuned TabICL-M (`e100_lr5e-5`) against TabPFN-3:

- kin8nm: beats TabPFN-3 zero-shot on 1/3 seeds, beats fine-tuned TabPFN-3 (its defaults) on 1/3, beats fine-tuned TabPFN-3 (100 epochs) on 2/3
- space_ga: beats TabPFN-3 zero-shot on 0/3 seeds, beats fine-tuned TabPFN-3 (its defaults) on 0/3, beats fine-tuned TabPFN-3 (100 epochs) on 0/3

Fine-tuning recovers about a third of the kin8nm gap (0.0761 to 0.0736 against 0.0721) and half of space_ga's, then plateaus: ten times more epochs gives nothing. TabPFN-3 does not gain from fine-tuning at all (it gets slightly worse), so its zero-shot model stays the best on both datasets. Fine-tuning is a shared lever that does not change the ordering.

## Weight soup (10k + 20k regressors averaged)

16 wins / 8 losses against the 20k model, mean relative gain +0.08 %: nothing.

## Sample-efficiency curve (complete data, `--max_rows` 430 / 860 / 1720 / 3000)

| dataset | rows | TabICLv2 released | source-aware TabICL-M | TabPFN 2.5 | TabPFN-3 | ours vs TabPFN-3 |
|---|---|---|---|---|---|---|
| kin8nm | 430 | 0.1120 | 0.1123 | 0.1369 | 0.0990 | +13.5 % |
| kin8nm | 860 | 0.0993 | 0.0981 | 0.1059 | 0.0917 | +7.0 % |
| kin8nm | 1720 | 0.0838 | 0.0819 | 0.0881 | 0.0781 | +4.8 % |
| kin8nm | 3000 | 0.0771 | 0.0761 | 0.0778 | 0.0721 | +5.5 % |
| space_ga | 430 | 0.1056 | 0.1071 | 0.1026 | 0.1013 | +5.7 % |
| space_ga | 860 | 0.0917 | 0.0948 | 0.0925 | 0.0904 | +4.8 % |
| space_ga | 1720 | 0.0930 | 0.0944 | 0.0929 | 0.0922 | +2.3 % |
| space_ga | 3000 | 0.1077 | 0.1140 | 0.0985 | 0.0986 | +15.7 % |

The gap to TabPFN-3 on kin8nm is present at every size and narrows with more data (13 % at 300 training rows, 5 % at 2100), so it is not a sample-efficiency problem of the in-context learner: TabPFN-3 is a better regressor on that class of smooth functions at any n, and TabPFN 2.5 with 10 M parameters (against 28.7 M here) is worse than us at small n and level at large n, so parameter count is not the cause either. On space_ga the source-aware training itself costs about 6 % against the released TabICLv2 at full size. TabPFN-3 caps at 50 000 rows; TabICL runs to 500 000, which is a structural edge only above that size (diamonds, 54 k rows, is the one benchmark dataset that crosses it).
