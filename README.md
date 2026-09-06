# TabICL-M: a tabular foundation model for incomplete tables

TabICL-M (M for missingness) extends [TabICLv2](https://github.com/soda-inria/tabicl)
so that it learns from tables in which not every row has every feature. It targets
the case that is common in engineering databases: the table is a merge of several
sources, and each source measured its own subset of the features. That is
block-structured missingness, not random gaps.

This repository is a fork of TabICL by Qu, Holzmüller, Varoquaux and Le Morvan.
All of TabICLv2 is still here and works unchanged. TabICL-M adds three parts on top,
each behind a flag, so each can be switched off for ablation.

**Status.** Research code. The three parts are implemented and tested, and the
first stage-4 run is done: the classifier and the regressor were each trained for
3000 steps from the released TabICLv2 weights on one GPU. The checkpoints are in
this repository under `checkpoints/tabicl-m/<task>/step-3000.ckpt` (git LFS, run
`git lfs pull`). On complete data they reproduce TabICLv2 exactly. Under injected
missingness they tie the mean-imputation baseline within seed noise, and both beat
XGBoost and CatBoost. See [Results so far](#results-so-far) and
[What remains](#what-remains).

**Workflow in three commands.** Install, run continued pre-training on one GPU,
evaluate against the baselines:

```bash
pip install -e ".[pretrain]"
bash scripts/train_v2_missing_stage4.sh clf          # and: reg
python scripts/ablation_missingness.py --out results/ablation \
    --aware_ckpt checkpoints/tabicl-m/clf/step-3000.ckpt --plot
```

## What is new

![TabICL-M architecture: the three stages of TabICLv2 with the missing-aware column embedding and the reconstruction head added](./docs/figures/missingness_prior/architecture.svg)

*The three stages of TabICLv2 with the TabICL-M additions in green. The full
description of the architecture, the training objective, and every revised file
with its size is in [docs/tabicl_m_architecture.md](./docs/tabicl_m_architecture.md).*

![How a complete synthetic table becomes an incomplete one](./docs/figures/missingness_prior/mechanism.svg)

*How the prior turns a complete synthetic table into an incomplete one: block
masking by source on the left, cell-wise masking on the right, then the union,
the safety rules, and the optional source-id column.*

**1. A block-structured missingness prior.** The synthetic tables used for
pre-training are split into 2 to 8 sources. Each source observes its own subset of
features, with an optional core set seen by all. Sources can carry an additive
offset and extra noise on numeric features, and the source id can be appended as a
categorical column. Cell-wise gaps under MCAR, MAR, and MNAR mechanisms, including
detection-limit censoring, are layered on top. Every mechanism hits a sampled target
rate. The target is never masked. Code: `src/tabicl/prior/_missingness.py`.

**2. An observed-only column embedding with a learned absence vector.** TabICL
embeds each column with a set transformer over its rows. In TabICL-M, missing
cells are hidden from the keys of the inducing-point attention, so the column
statistics come from observed cells only. A missing indicator is projected into the
input token and a learned absence vector is added to the output embedding. Both new
parameters start at zero, so on complete data the model reproduces TabICLv2
exactly. Flag: `col_missing_aware`. Code: `src/tabicl/_model/embedding.py`.

**3. A joint prediction and reconstruction objective.** During pre-training a
fraction of the observed cells is hidden. The model predicts the target as usual and
reconstructs the hidden cells from the per-feature outputs of the row-wise
interaction through a small head. The head is dropped at inference. Flag:
`reconstruction`, trainer option `--recon_weight`. Code:
`src/tabicl/train/_reconstruction.py`.

### What is not new

Three ideas close to this work are published and are not claimed here.
[TabPFN v2](https://www.nature.com/articles/s41586-024-08328-6) injects cell-wise
missingness into its prior and adds a missing indicator to its encoder.
[NAIM](https://arxiv.org/abs/2407.11540) masks missing features out of attention
instead of imputing. [ReMasker](https://arxiv.org/abs/2309.13793) and
[VIME](https://arxiv.org/abs/2006.06731) train tabular models with masked-cell
reconstruction. All three treat missingness as cell-wise and random. None is an
in-context learner. The contribution of TabICL-M is the source-structured prior,
the column-level masking inside an inducing-point set transformer, and the joint
objective inside a tabular in-context learner.

## Installation

```bash
git clone https://github.com/Sompote/tabicl-m.git && cd tabicl-m
pip install -e .
```

The distribution is named `tabicl-m`, so it does not collide with the upstream
`tabicl` package on PyPI. The import name stays `tabicl`, so upstream code, the
released checkpoints, and the tutorials work unchanged. Do not install both in the
same environment.

Optional dependencies:

```bash
pip install -e ".[pretrain]"   # continued pre-training (wandb, transformers, xgboost)
pip install -e ".[finetune]"   # fine-tuning on a single dataset
pip install -e ".[forecast]"   # time series forecasting
pip install -e ".[shap]"       # SHAP explanations
pip install -e ".[all]"
```

## Basic usage

The estimators are scikit-learn compatible. With the released TabICLv2 checkpoint,
missing numeric values are mean-imputed and missing categories get their own code,
exactly as in upstream TabICL.

```python
from tabicl import TabICLClassifier, TabICLRegressor

clf = TabICLClassifier()          # downloads the TabICLv2 checkpoint on first use
clf.fit(X_train, y_train)
clf.predict(X_test)               # in-context learning happens here

reg = TabICLRegressor()
reg.fit(X_train, y_train)
reg.predict(X_test)
```

With a checkpoint trained with `col_missing_aware=True`, the same estimators pass
NaN straight through to the model. No imputation is applied, in numeric or
categorical columns. Nothing changes in the calling code:

```python
clf = TabICLClassifier(model_path="checkpoints/tabicl-m/clf/step-3000.ckpt")
clf.fit(X_train, y_train)         # X_train may contain NaN in any column
clf.predict(X_test)
print(clf.X_encoder_.impute)      # False: the model saw the gaps
```

KV caching, save and load, the full parameter list, fine-tuning, forecasting, and
SHAP work as in upstream TabICL. See [Inherited features](#inherited-features).

## Missing values: how each path treats them

| Path | Numeric NaN | Categorical NaN | Column statistics | Seen in pre-training |
|---|---|---|---|---|
| TabICLv2, released | mean-imputed | own category | include imputed values | no |
| TabICLv2 + indicator columns | mean-imputed | own category | include imputed values | no |
| TabICL-M, `col_missing_aware` | kept as NaN | kept as NaN | observed cells only | yes |

## Continued pre-training (stage 4)

TabICL-M is trained by continuing from the released TabICLv2 weights with the
three parts switched on. The new parameters are zero at step 0, so the run starts
exactly at the released model on complete data. One GPU with 32 GB is enough for
the default settings with `DTYPE=bfloat16`; in float32 the attention falls back to
memory-hungry kernels when FlashAttention-3 is not available and runs out of memory
at `--max_seq_len 8192`.

```bash
pip install -e ".[pretrain]"
python -c "from tabicl import TabICLClassifier, TabICLRegressor; TabICLClassifier()._load_model(); TabICLRegressor()._load_model()"
bash scripts/train_v2_missing_stage4.sh clf
bash scripts/train_v2_missing_stage4.sh reg
```

The script copies the stage-3 recipe of TabICLv2 and adds:

```
--missing_enabled True        # block-structured and cell-wise missingness in the prior
--col_missing_aware True      # observed-only column embedding with absence vector
--recon_weight 0.1            # masked-cell reconstruction, hide up to 30 % of observed cells
--checkpoint_path <released>  --only_load_model True
```

Environment variables override the defaults, for example `STEPS=6000 BATCH=64
NUM_GPUS=4 RECON_WEIGHT=0.05 DTYPE=bfloat16 RECOMPUTE=True`. The trainer logs the task loss and the
reconstruction loss separately. The task loss should stay near its starting value.
The reconstruction loss should fall. Checkpoints are written to
`checkpoints/tabicl-m/<task>/step-*.ckpt` and load directly into the estimators.

The run that produced the committed checkpoints (`checkpoints/tabicl-m/run_stage4.sh`,
one RTX 5090, bfloat16, 3000 steps, batch 32, `--max_seq_len 8192`, 2 h 20 min per
task) behaved as intended. Averaged over 250-step windows:

| Task | Task loss, steps 0 to 249 | Task loss, steps 2750 to 2999 | Reconstruction, first window | Reconstruction, last window |
|---|---|---|---|---|
| classifier | cross-entropy 0.82 (accuracy 0.73) | 0.55 (0.78) | 0.24 | 0.19 |
| regressor | pinball 0.084 | 0.080 | 0.24 | 0.20 |

The classifier's task loss falls at first because the released model has never seen
tables with gaps; the regressor's stays flat. The reconstruction loss falls in both.

All `--missing_*` options are listed by `python -m tabicl.train --help`. The
same options apply to `python -m tabicl.prior` when tables are pre-generated to
disk, and the missingness configuration is written to the dataset `metadata.json`.

![Where the missingness transform sits in the pre-training pipeline](./docs/figures/missingness_prior/pipeline.svg)

*The missingness transform runs on every batch right after the structural causal
model prior, whether tables are generated on the fly or written to disk. It is a
bypass unless `--missing_enabled True` is passed.*

## Evaluation

`scripts/ablation_missingness.py` deletes cells from complete tables under a
stated mechanism at a stated rate and compares:

| Model name | What it is |
|---|---|
| `tabicl_impute` | released TabICLv2, NaN mean-imputed (the baseline) |
| `tabicl_indicator` | as above, plus one 0/1 indicator column per incomplete feature |
| `tabicl_aware_zero` | released weights inside the TabICL-M architecture, new parameters at zero |
| `tabicl_aware` | a TabICL-M checkpoint from stage 4 |
| `xgboost`, `catboost`, `tabpfn` | baselines with native NaN handling |

Mechanisms are `mcar`, `mar`, `mnar`, and `block`. Metrics are AUC, accuracy, and
log loss for classification, and RMSE, R², and the coverage and width of the
80 % prediction interval for regression. A CSV with a source column runs
leave-one-source-out splits on its natural gaps.

```bash
# synthetic ablation
python scripts/ablation_missingness.py --out results/ablation \
    --datasets diabetes openml:1590 --aware_ckpt checkpoints/tabicl-m/clf/step-3000.ckpt \
    --aware_ckpt_reg checkpoints/tabicl-m/reg/step-3000.ckpt --plot

# real multi-source table, leave-one-source-out, natural missingness
python scripts/ablation_missingness.py --out results/loso \
    --datasets csv:data/compaction.csv --target rho_d_max --source_col lab \
    --task regression --loso --natural --aware_ckpt_reg checkpoints/tabicl-m/reg/step-3000.ckpt
```

Outputs are `results.csv` with one row per fit, `summary.csv` and `summary.md`
with mean and spread over seeds, and plots. `--resummarize` rebuilds the tables
from a saved results file.

### Results so far

**Before training** (`results/ablation_v2/`), the released TabICLv2 weights inside
the three TabICL paths did not differ, as expected with the new parameters at zero.
That established that the architecture change does not hurt and that the baseline
is strong: mean imputation inside an in-context learner already absorbs most of the
damage.

**After stage 4** (`results/ablation_m/`, `results/ablation_m/run.sh`): six
datasets, four mechanisms, three rates, three seeds, six models, 1404 fits. The
three built-in datasets are those of the first evaluation. The three OpenML
datasets were added because the built-in classification sets sit at AUC 0.98 to
1.00 and cannot separate the models: `credit-g` (31), `adult` (1590, subsampled to
3000 rows), and Boston housing (531). `tabicl_aware` is the committed step-3000
checkpoint. Mean over seeds at the highest deletion rate:

`adult`, AUC (2100 training rows, 14 features):

| Mechanism | Rate | `tabicl_impute` | `tabicl_indicator` | `tabicl_aware_zero` | `tabicl_aware` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|
| complete | 0.0 | 0.912 | 0.911 | 0.912 | 0.912 | 0.897 | 0.896 |
| mcar | 0.5 | 0.858 | 0.856 | 0.857 | 0.857 | 0.841 | 0.836 |
| mar | 0.5 | 0.850 | 0.848 | 0.849 | 0.849 | 0.837 | 0.839 |
| mnar | 0.5 | 0.859 | 0.855 | 0.858 | 0.859 | 0.838 | 0.839 |
| block | 0.5 | 0.860 | 0.856 | 0.862 | 0.865 | 0.849 | 0.855 |

`credit-g`, AUC (700 training rows, 20 features):

| Mechanism | Rate | `tabicl_impute` | `tabicl_indicator` | `tabicl_aware_zero` | `tabicl_aware` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|
| complete | 0.0 | 0.828 | 0.828 | 0.828 | 0.828 | 0.801 | 0.807 |
| mcar | 0.5 | 0.696 | 0.689 | 0.696 | 0.701 | 0.674 | 0.664 |
| mar | 0.5 | 0.725 | 0.721 | 0.727 | 0.724 | 0.679 | 0.664 |
| mnar | 0.5 | 0.760 | 0.758 | 0.758 | 0.759 | 0.728 | 0.707 |
| block | 0.5 | 0.729 | 0.729 | 0.728 | 0.729 | 0.691 | 0.692 |

Boston housing, RMSE (354 training rows, 13 features):

| Mechanism | Rate | `tabicl_impute` | `tabicl_indicator` | `tabicl_aware_zero` | `tabicl_aware` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|
| complete | 0.0 | 3.01 | 3.01 | 3.01 | 3.02 | 3.34 | 2.99 |
| mcar | 0.5 | 5.90 | 5.88 | 5.83 | 5.68 | 6.04 | 6.17 |
| mar | 0.5 | 4.97 | 5.09 | 5.11 | 4.89 | 5.71 | 5.39 |
| mnar | 0.5 | 5.08 | 5.09 | 5.04 | 4.98 | 5.09 | 5.16 |
| block | 0.5 | 4.79 | 4.80 | 4.80 | 4.80 | 4.89 | 4.67 |

Diabetes, RMSE:

| Mechanism | Rate | `tabicl_impute` | `tabicl_indicator` | `tabicl_aware_zero` | `tabicl_aware` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|
| complete | 0.0 | 56.6 | 56.6 | 56.6 | 56.7 | 62.1 | 59.7 |
| mcar | 0.5 | 65.6 | 65.5 | 65.5 | 65.1 | 69.9 | 69.8 |
| mar | 0.5 | 61.5 | 61.9 | 62.7 | 61.6 | 67.4 | 63.4 |
| mnar | 0.5 | 62.7 | 62.2 | 63.4 | 62.6 | 71.0 | 67.6 |
| block | 0.5 | 63.6 | 63.6 | 63.4 | 63.2 | 69.7 | 66.1 |

Paired over all 39 conditions per dataset (same seed, same deleted cells):

| Dataset | Metric | wins / losses vs `tabicl_impute` | mean gain (higher AUC, lower RMSE) | wins / losses vs `xgboost` | mean gain |
|---|---|---|---|---|---|
| breast_cancer | AUC | 28 / 10 | +0.0004 AUC | 29 / 9 | +0.003 AUC |
| wine | AUC | 12 / 8 | +0.0004 AUC | 30 / 2 | +0.010 AUC |
| credit-g | AUC | 21 / 18 | +0.0003 AUC | 35 / 4 | +0.034 AUC |
| adult | AUC | 15 / 24 | -0.0006 AUC | 38 / 1 | +0.016 AUC |
| diabetes | RMSE | 28 / 11 | +0.21 RMSE | 39 / 0 | +5.70 RMSE |
| Boston | RMSE | 25 / 14 | +0.07 RMSE | 30 / 9 | +0.31 RMSE |

Three things follow.

1. **Training did not hurt.** On complete data the trained model matches the
   released model within 0.001 AUC and 0.01 RMSE on every dataset.
2. **TabICL-M ties mean imputation.** It wins about 60 % of the paired comparisons
   against `tabicl_impute`, but the mean gain is inside the seed spread everywhere.
   The only consistent edge is regression under MAR and MCAR on Boston housing
   (RMSE 4.89 against 4.97 and 5.68 against 5.90 at rate 0.5). The trained
   parameters do something, since `tabicl_aware` also edges out `tabicl_aware_zero`,
   but not much on these tables. This is the fallback outcome stated below:
   TabICLv2 with mean imputation is already robust to random gaps.
3. **Both TabICL paths beat the tree baselines with native NaN handling** on five
   of the six datasets, by 0.016 AUC on `adult`, 0.034 to 0.038 AUC on `credit-g`
   (39 wins, 0 losses against CatBoost on both), and 3.6 to 5.7 RMSE on diabetes.
   The exception is Boston housing under block missingness, where CatBoost is
   slightly ahead.

The block mechanism here removes column blocks per source but injects no per-source
offset or noise, and the split is random, not by source. That is the mild version of
the case TabICL-M is built for. Full tables and plots:
`results/ablation_m/builtin/summary.md`, `results/ablation_m/openml/summary.md`.

<!-- sa-results:start -->

## Source-aware TabICL-M: results

*Auto-generated by the training pipeline (`checkpoints/tabicl-m-sa/pipeline.sh`). Full tables: `results/sa_eval/summary_vs_baselines.md`, `results/sa_ablation/summary.md`; training logs under `checkpoints/tabicl-m-sa/`.*

### Source-aware checkpoint (10k steps) against the baselines

`tabicl_m_sa` = source-aware stage-4 checkpoint (`checkpoints/tabicl-m-sa/*/step-10000.ckpt`); `tabicl_aware` = first stage-4 checkpoint (3000 steps, value-level parts only); `tabicl_impute` = released TabICLv2 with mean imputation; `tabpfn` = TabPFN v2, `tabpfn25` / `tabpfn26` / `tabpfn3` = TabPFN 2.5 / 2.6 / 3 default checkpoints. Mean over 5 seeds; bold = best in row.

### Leave-one-source-out (held-out synthetic source)

| dataset | condition | `tabicl_impute` | `tabicl_indicator` | `tabicl_patternnorm` | `tabicl_iterimpute` | `tabicl_knnimpute` | `tabicl_aware_zero` | `tabicl_aware` | `tabicl_m_sa` | `tabpfn` | `tabpfn25` | `tabpfn26` | `tabpfn3` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | complete@0.0 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.997 | **0.997** | 0.996 | 0.996 | 0.996 | 0.997 | 0.995 | 0.996 |
| breast_cancer (AUC) | block@0.5 | 0.968 | 0.972 | 0.967 | 0.953 | 0.984 | 0.975 | 0.977 | 0.989 | 0.980 | 0.991 | 0.988 | **0.991** | 0.964 | 0.972 |
| breast_cancer (AUC) | block_shift@0.5 | 0.963 | 0.970 | 0.960 | 0.881 | 0.961 | 0.969 | 0.973 | 0.984 | 0.980 | **0.984** | 0.977 | 0.982 | 0.964 | 0.955 |
| wine (AUC) | complete@0.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 | 1.000 | 0.999 | 1.000 | 0.997 | 0.998 |
| wine (AUC) | block@0.5 | 0.990 | 0.990 | 0.988 | 0.938 | 0.990 | 0.989 | 0.989 | 0.992 | **0.992** | 0.991 | 0.990 | 0.991 | 0.968 | 0.958 |
| wine (AUC) | block_shift@0.5 | 0.914 | 0.923 | **0.971** | 0.807 | 0.870 | 0.905 | 0.905 | 0.932 | 0.927 | 0.935 | 0.929 | 0.925 | 0.897 | 0.806 |
| diabetes (RMSE) | complete@0.0 | 55.79 | 55.79 | **55.79** | 55.79 | 55.79 | 55.79 | 55.90 | 56.06 | 56.20 | 56.33 | 56.23 | 56.31 | 62.92 | 59.55 |
| diabetes (RMSE) | block@0.5 | 66.36 | 66.03 | 66.96 | 71.24 | 66.77 | 66.14 | 64.52 | 63.99 | 65.61 | **63.65** | 65.41 | 63.98 | 79.42 | 73.23 |
| diabetes (RMSE) | block_shift@0.5 | 69.10 | 68.49 | 69.51 | 72.81 | 67.93 | 68.94 | 67.73 | **65.15** | 66.95 | 65.56 | 67.54 | 65.45 | 79.01 | 78.81 |
| credit-g (AUC) | complete@0.0 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.815 | 0.817 | 0.806 | 0.815 | **0.817** | 0.816 | 0.798 | 0.802 |
| credit-g (AUC) | block@0.5 | 0.704 | 0.705 | 0.690 | 0.637 | 0.658 | **0.706** | 0.704 | 0.702 | 0.683 | 0.693 | 0.694 | 0.686 | 0.633 | 0.603 |
| credit-g (AUC) | block_shift@0.5 | 0.683 | 0.677 | 0.680 | 0.652 | 0.682 | 0.680 | 0.673 | **0.683** | 0.665 | 0.679 | 0.663 | 0.673 | 0.637 | 0.624 |
| adult (AUC) | complete@0.0 | 0.912 | 0.912 | 0.908 | 0.912 | 0.912 | 0.912 | 0.912 | 0.913 | **0.916** | 0.915 | 0.912 | 0.911 | 0.897 | 0.896 |
| adult (AUC) | block@0.5 | 0.847 | 0.844 | 0.841 | 0.780 | 0.821 | 0.845 | 0.846 | 0.847 | 0.842 | 0.845 | 0.841 | **0.849** | 0.823 | 0.802 |
| adult (AUC) | block_shift@0.5 | 0.800 | 0.816 | 0.813 | 0.677 | 0.774 | 0.813 | 0.806 | 0.810 | 0.816 | **0.822** | 0.811 | 0.812 | 0.793 | 0.783 |
| boston (RMSE) | complete@0.0 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.72 | 2.73 | **2.70** | 2.72 | 2.76 | 2.71 | 3.23 | 2.82 |
| boston (RMSE) | block@0.5 | 5.84 | 5.84 | 6.15 | 10.22 | 5.89 | 6.05 | 5.98 | 5.48 | 6.29 | 5.86 | 6.04 | **4.94** | 11.48 | 8.03 |
| boston (RMSE) | block_shift@0.5 | 7.08 | 7.16 | 6.88 | 7.91 | 7.54 | 7.00 | 6.81 | **6.72** | 7.20 | 6.75 | 6.95 | 6.81 | 8.64 | 9.49 |

#### loso: `tabicl_m_sa` vs `tabicl_impute`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 18 / 2 | +0.0129 |
| wine | AUC | 12 / 6 | +0.0089 |
| diabetes | RMSE | 19 / 1 | +2.0886 |
| credit-g | AUC | 8 / 12 | -0.0005 |
| adult | AUC | 14 / 6 | +0.0078 |
| boston | RMSE | 13 / 7 | +0.4194 |

#### loso: `tabicl_m_sa` vs `tabicl_aware`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 17 / 2 | +0.0076 |
| wine | AUC | 14 / 4 | +0.0104 |
| diabetes | RMSE | 14 / 6 | +1.1846 |
| credit-g | AUC | 11 / 9 | +0.0025 |
| adult | AUC | 10 / 10 | +0.0043 |
| boston | RMSE | 15 / 5 | +0.2611 |

#### loso: `tabicl_m_sa` vs `tabpfn`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 19 / 1 | +0.0062 |
| wine | AUC | 10 / 8 | +0.0056 |
| diabetes | RMSE | 14 / 6 | +1.2450 |
| credit-g | AUC | 16 / 4 | +0.0139 |
| adult | AUC | 13 / 7 | +0.0042 |
| boston | RMSE | 14 / 6 | +0.6287 |

#### loso: `tabicl_m_sa` vs `tabpfn25`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 6 / 14 | -0.0016 |
| wine | AUC | 10 / 8 | -0.0004 |
| diabetes | RMSE | 13 / 7 | +0.0041 |
| credit-g | AUC | 12 / 8 | +0.0070 |
| adult | AUC | 13 / 7 | +0.0007 |
| boston | RMSE | 12 / 8 | +0.2167 |

#### loso: `tabicl_m_sa` vs `tabpfn3`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 6 / 14 | -0.0014 |
| wine | AUC | 9 / 9 | +0.0019 |
| diabetes | RMSE | 9 / 11 | +0.1620 |
| credit-g | AUC | 11 / 9 | +0.0053 |
| adult | AUC | 9 / 11 | +0.0013 |
| boston | RMSE | 5 / 15 | -0.1103 |

#### loso: `tabicl_m_sa` vs `tabicl_patternnorm`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 17 / 3 | +0.0132 |
| wine | AUC | 10 / 9 | -0.0033 |
| diabetes | RMSE | 16 / 4 | +0.9524 |
| credit-g | AUC | 14 / 6 | +0.0072 |
| adult | AUC | 14 / 6 | -0.0007 |
| boston | RMSE | 13 / 7 | +0.4167 |

#### loso: `tabicl_m_sa` vs `tabicl_impute`, block_shift only

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 10 / 0 | +0.0125 |
| wine | AUC | 8 / 2 | +0.0089 |
| diabetes | RMSE | 10 / 0 | +2.4218 |
| credit-g | AUC | 4 / 6 | +0.0005 |
| adult | AUC | 7 / 3 | +0.0147 |
| boston | RMSE | 7 / 3 | +0.5517 |

#### loso: 80 % interval coverage / width, regression, block_shift@0.5

|                                    |   coverage80 |   width80 |
|:-----------------------------------|-------------:|----------:|
| ('boston', 'tabicl_aware')         |        0.83  |     1.777 |
| ('boston', 'tabicl_aware_zero')    |        0.865 |     2.017 |
| ('boston', 'tabicl_impute')        |        0.867 |     2.138 |
| ('boston', 'tabicl_indicator')     |        0.863 |     2.149 |
| ('boston', 'tabicl_iterimpute')    |        0.916 |     3.19  |
| ('boston', 'tabicl_knnimpute')     |        0.759 |     1.811 |
| ('boston', 'tabicl_m_sa')          |        0.81  |     1.598 |
| ('boston', 'tabicl_patternnorm')   |        0.824 |     1.668 |
| ('diabetes', 'tabicl_aware')       |        0.787 |     2.184 |
| ('diabetes', 'tabicl_aware_zero')  |        0.819 |     2.327 |
| ('diabetes', 'tabicl_impute')      |        0.827 |     2.361 |
| ('diabetes', 'tabicl_indicator')   |        0.824 |     2.361 |
| ('diabetes', 'tabicl_iterimpute')  |        0.813 |     2.384 |
| ('diabetes', 'tabicl_knnimpute')   |        0.759 |     2.016 |
| ('diabetes', 'tabicl_m_sa')        |        0.818 |     2.24  |
| ('diabetes', 'tabicl_patternnorm') |        0.818 |     2.376 |

### Random split

| dataset | condition | `tabicl_impute` | `tabicl_indicator` | `tabicl_patternnorm` | `tabicl_iterimpute` | `tabicl_knnimpute` | `tabicl_aware_zero` | `tabicl_aware` | `tabicl_m_sa` | `tabpfn` | `tabpfn25` | `tabpfn26` | `tabpfn3` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | complete@0.0 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.997 | **0.997** | 0.996 | 0.996 | 0.996 | 0.997 | 0.995 | 0.996 |
| breast_cancer (AUC) | block@0.5 | 0.995 | 0.996 | 0.996 | 0.994 | 0.994 | 0.995 | 0.995 | 0.996 | 0.995 | 0.996 | 0.995 | **0.996** | 0.991 | 0.993 |
| breast_cancer (AUC) | block_shift@0.5 | 0.994 | 0.994 | 0.994 | 0.994 | 0.991 | 0.994 | 0.994 | 0.994 | 0.994 | 0.995 | 0.993 | **0.995** | 0.987 | 0.990 |
| wine (AUC) | complete@0.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 | 1.000 | 0.999 | 1.000 | 0.997 | 0.998 |
| wine (AUC) | block@0.5 | 0.996 | 0.996 | 0.995 | 0.994 | 0.993 | **0.997** | 0.996 | 0.996 | 0.995 | 0.995 | 0.996 | 0.994 | 0.989 | 0.984 |
| wine (AUC) | block_shift@0.5 | 0.989 | 0.988 | 0.989 | 0.984 | 0.985 | 0.989 | **0.990** | 0.989 | 0.986 | 0.989 | 0.988 | 0.986 | 0.976 | 0.981 |
| diabetes (RMSE) | complete@0.0 | 55.79 | 55.79 | **55.79** | 55.79 | 55.79 | 55.79 | 55.90 | 56.06 | 56.20 | 56.33 | 56.23 | 56.31 | 62.92 | 59.55 |
| diabetes (RMSE) | block@0.5 | 65.34 | 65.37 | 65.46 | 64.95 | 65.89 | 65.12 | 64.87 | 64.76 | 64.93 | 64.84 | 64.97 | **64.21** | 71.66 | 68.76 |
| diabetes (RMSE) | block_shift@0.5 | 64.78 | 64.67 | 65.21 | 64.49 | 66.59 | 65.06 | 64.78 | 64.23 | 64.66 | 64.11 | 64.83 | **63.72** | 74.13 | 69.41 |
| credit-g (AUC) | complete@0.0 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.815 | 0.817 | 0.806 | 0.815 | **0.817** | 0.816 | 0.798 | 0.802 |
| credit-g (AUC) | block@0.5 | 0.722 | 0.723 | 0.726 | 0.721 | 0.705 | 0.721 | 0.723 | 0.721 | **0.731** | 0.728 | 0.727 | 0.726 | 0.698 | 0.695 |
| credit-g (AUC) | block_shift@0.5 | 0.727 | 0.727 | 0.726 | 0.698 | 0.709 | 0.726 | **0.728** | 0.725 | 0.716 | 0.727 | 0.726 | 0.720 | 0.677 | 0.695 |
| adult (AUC) | complete@0.0 | 0.912 | 0.912 | 0.908 | 0.912 | 0.912 | 0.912 | 0.912 | 0.913 | **0.916** | 0.915 | 0.912 | 0.911 | 0.897 | 0.896 |
| adult (AUC) | block@0.5 | 0.865 | 0.851 | 0.864 | 0.839 | 0.853 | 0.866 | 0.868 | 0.869 | **0.869** | 0.868 | 0.863 | 0.866 | 0.850 | 0.853 |
| adult (AUC) | block_shift@0.5 | 0.859 | 0.838 | 0.857 | 0.834 | 0.849 | 0.859 | 0.861 | 0.860 | **0.861** | 0.859 | 0.858 | 0.858 | 0.836 | 0.843 |
| boston (RMSE) | complete@0.0 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.72 | 2.73 | **2.70** | 2.72 | 2.76 | 2.71 | 3.23 | 2.82 |
| boston (RMSE) | block@0.5 | 4.84 | 4.86 | 4.84 | 5.07 | 5.21 | 4.83 | 4.82 | **4.79** | 4.87 | 4.93 | 4.95 | 4.90 | 5.19 | 4.98 |
| boston (RMSE) | block_shift@0.5 | 4.70 | 4.66 | 4.76 | 5.13 | 4.86 | 4.67 | 4.68 | 4.66 | 4.77 | 4.67 | 4.72 | **4.63** | 5.41 | 5.08 |

#### random_split: `tabicl_m_sa` vs `tabicl_impute`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 9 / 10 | +0.0001 |
| wine | AUC | 5 / 8 | +0.0002 |
| diabetes | RMSE | 14 / 6 | +0.4158 |
| credit-g | AUC | 11 / 9 | +0.0007 |
| adult | AUC | 14 / 6 | +0.0018 |
| boston | RMSE | 12 / 8 | +0.0503 |

#### random_split: `tabicl_m_sa` vs `tabicl_aware`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 10 / 8 | +0.0001 |
| wine | AUC | 4 / 9 | -0.0002 |
| diabetes | RMSE | 9 / 11 | +0.1621 |
| credit-g | AUC | 9 / 11 | +0.0002 |
| adult | AUC | 12 / 8 | +0.0005 |
| boston | RMSE | 10 / 10 | +0.0079 |

#### random_split: `tabicl_m_sa` vs `tabpfn`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 14 / 6 | +0.0005 |
| wine | AUC | 13 / 3 | +0.0019 |
| diabetes | RMSE | 14 / 6 | +0.3619 |
| credit-g | AUC | 11 / 9 | +0.0047 |
| adult | AUC | 10 / 10 | -0.0003 |
| boston | RMSE | 16 / 4 | +0.0659 |

#### random_split: `tabicl_m_sa` vs `tabpfn25`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 8 / 12 | -0.0003 |
| wine | AUC | 11 / 4 | +0.0009 |
| diabetes | RMSE | 9 / 11 | +0.0085 |
| credit-g | AUC | 13 / 7 | +0.0005 |
| adult | AUC | 13 / 7 | +0.0009 |
| boston | RMSE | 13 / 7 | +0.0706 |

#### random_split: `tabicl_m_sa` vs `tabpfn3`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 8 / 11 | -0.0002 |
| wine | AUC | 10 / 5 | +0.0013 |
| diabetes | RMSE | 4 / 16 | -0.4324 |
| credit-g | AUC | 11 / 9 | +0.0030 |
| adult | AUC | 14 / 6 | +0.0016 |
| boston | RMSE | 8 / 12 | -0.0054 |

#### random_split: `tabicl_m_sa` vs `tabicl_patternnorm`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 7 / 10 | +0.0002 |
| wine | AUC | 7 / 7 | +0.0005 |
| diabetes | RMSE | 13 / 7 | +0.5290 |
| credit-g | AUC | 11 / 9 | +0.0022 |
| adult | AUC | 15 / 5 | +0.0036 |
| boston | RMSE | 14 / 6 | +0.0480 |

#### random_split: `tabicl_m_sa` vs `tabicl_impute`, block_shift only

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 5 / 4 | +0.0003 |
| wine | AUC | 2 / 5 | -0.0003 |
| diabetes | RMSE | 8 / 2 | +0.3889 |
| credit-g | AUC | 5 / 5 | -0.0002 |
| adult | AUC | 7 / 3 | +0.0018 |
| boston | RMSE | 4 / 6 | +0.0174 |

#### random_split: 80 % interval coverage / width, regression, block_shift@0.5

|                                    |   coverage80 |   width80 |
|:-----------------------------------|-------------:|----------:|
| ('boston', 'tabicl_aware')         |        0.779 |     1.151 |
| ('boston', 'tabicl_aware_zero')    |        0.771 |     1.135 |
| ('boston', 'tabicl_impute')        |        0.776 |     1.164 |
| ('boston', 'tabicl_indicator')     |        0.779 |     1.169 |
| ('boston', 'tabicl_iterimpute')    |        0.745 |     1.196 |
| ('boston', 'tabicl_knnimpute')     |        0.811 |     1.298 |
| ('boston', 'tabicl_m_sa')          |        0.763 |     1.12  |
| ('boston', 'tabicl_patternnorm')   |        0.778 |     1.173 |
| ('diabetes', 'tabicl_aware')       |        0.767 |     2.014 |
| ('diabetes', 'tabicl_aware_zero')  |        0.758 |     2.013 |
| ('diabetes', 'tabicl_impute')      |        0.785 |     2.049 |
| ('diabetes', 'tabicl_indicator')   |        0.78  |     2.053 |
| ('diabetes', 'tabicl_iterimpute')  |        0.785 |     2.109 |
| ('diabetes', 'tabicl_knnimpute')   |        0.791 |     2.116 |
| ('diabetes', 'tabicl_m_sa')        |        0.783 |     2.016 |
| ('diabetes', 'tabicl_patternnorm') |        0.783 |     2.052 |

### Standard ablation (random split, mcar / mar / mnar / block at 0.5)

| dataset | condition | `tabicl_impute` | `tabicl_aware` | `tabicl_m_sa` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|
| breast_cancer (AUC) | complete@0.0 | 0.996 | **0.996** | 0.996 | 0.995 | 0.995 |
| breast_cancer (AUC) | mcar@0.5 | 0.989 | 0.990 | **0.991** | 0.987 | 0.980 |
| breast_cancer (AUC) | mar@0.5 | 0.990 | 0.989 | **0.991** | 0.987 | 0.987 |
| breast_cancer (AUC) | mnar@0.5 | 0.990 | 0.992 | **0.992** | 0.986 | 0.990 |
| breast_cancer (AUC) | block@0.5 | 0.994 | 0.994 | 0.994 | 0.990 | 0.991 |
| wine (AUC) | complete@0.0 | 1.000 | **1.000** | 1.000 | 0.996 | 0.997 |
| wine (AUC) | mcar@0.5 | 0.980 | 0.981 | **0.985** | 0.948 | 0.949 |
| wine (AUC) | mar@0.5 | 0.985 | 0.985 | **0.987** | 0.973 | 0.965 |
| wine (AUC) | mnar@0.5 | 0.993 | **0.994** | 0.992 | 0.985 | 0.980 |
| wine (AUC) | block@0.5 | 0.994 | **0.998** | 0.995 | 0.989 | 0.982 |
| diabetes (RMSE) | complete@0.0 | 56.57 | 56.65 | 56.88 | 62.05 | 59.74 |
| diabetes (RMSE) | mcar@0.5 | 65.60 | 65.10 | **64.14** | 69.93 | 69.84 |
| diabetes (RMSE) | mar@0.5 | **61.47** | 61.60 | 61.91 | 67.37 | 63.41 |
| diabetes (RMSE) | mnar@0.5 | 62.69 | 62.59 | 63.52 | 70.99 | 67.63 |
| diabetes (RMSE) | block@0.5 | 64.54 | **63.19** | 64.01 | 69.72 | 66.10 |
| credit-g (AUC) | complete@0.0 | 0.828 | 0.828 | **0.831** | 0.801 | 0.807 |
| credit-g (AUC) | mcar@0.5 | 0.696 | 0.701 | **0.708** | 0.674 | 0.664 |
| credit-g (AUC) | mar@0.5 | 0.725 | 0.724 | 0.726 | 0.679 | 0.664 |
| credit-g (AUC) | mnar@0.5 | **0.760** | 0.759 | — | 0.728 | 0.707 |
| credit-g (AUC) | block@0.5 | **0.729** | 0.729 | 0.724 | 0.691 | 0.692 |
| adult (AUC) | complete@0.0 | 0.912 | 0.912 | **0.912** | 0.897 | 0.896 |
| adult (AUC) | mcar@0.5 | **0.858** | 0.857 | 0.857 | 0.841 | 0.836 |
| adult (AUC) | mar@0.5 | 0.850 | 0.849 | **0.851** | 0.837 | 0.839 |
| adult (AUC) | mnar@0.5 | **0.859** | 0.859 | — | 0.838 | 0.839 |
| adult (AUC) | block@0.5 | 0.866 | 0.865 | **0.871** | 0.849 | 0.855 |
| boston (RMSE) | complete@0.0 | 3.01 | 3.02 | 3.06 | 3.34 | **2.99** |
| boston (RMSE) | mcar@0.5 | 5.90 | 5.68 | **5.52** | 6.04 | 6.17 |
| boston (RMSE) | mar@0.5 | 4.97 | **4.89** | 4.91 | 5.71 | 5.39 |
| boston (RMSE) | mnar@0.5 | 5.08 | **4.98** | 5.30 | 5.09 | 5.16 |
| boston (RMSE) | block@0.5 | 5.08 | 4.80 | 5.04 | 4.89 | **4.67** |

#### `tabicl_m_sa` vs `tabicl_impute`, paired over all mechanisms and rates

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 18 / 16 | +0.0006 |
| wine | AUC | 17 / 7 | +0.0010 |
| diabetes | RMSE | 24 / 12 | +0.2734 |
| credit-g | AUC | 21 / 10 | +0.0026 |
| adult | AUC | 17 / 14 | +0.0001 |
| boston | RMSE | 26 / 7 | +0.1405 |

### Ablation of each part

Each variant: classifier, 3000 steps, lr 5e-5, source-aware prior, one switch off. Cells: mean paired gain over `tabicl_impute` (AUC up / RMSE down) and wins/losses over rates 0.3, 0.5 x 5 seeds. `full_10k` is the main 10k-step checkpoint; `tabicl_aware` the first stage-4 checkpoint (old prior, value-level parts).

- `full_3k`: all parts on (3k steps)
- `no_group_stats`: without col_group_stats
- `no_row_mask`: without row_missing_aware
- `no_pattern_token`: without pattern_token
- `no_objectives`: cell reconstruction, no consistency loss
- `arch_off`: all parts off, new prior only

### Leave-one-source-out, block_shift

| dataset | `full_10k` | `full_3k` | `no_group_stats` | `no_row_mask` | `no_pattern_token` | `no_objectives` | `arch_off` | `tabicl_aware` | `tabpfn` |
|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | +0.012 (10/0) | +0.011 (10/0) | +0.011 (9/1) | +0.011 (9/1) | +0.011 (10/0) | +0.012 (10/0) | +0.011 (9/1) | +0.006 (6/4) | +0.008 (6/4) |
| wine (AUC) | +0.009 (8/2) | +0.008 (7/3) | +0.008 (9/1) | +0.007 (7/3) | +0.006 (6/4) | +0.005 (7/3) | +0.004 (7/3) | -0.004 (6/4) | +0.006 (6/4) |
| diabetes (RMSE) | +2.422 (10/0) | — | — | — | — | — | — | +0.760 (7/3) | +0.935 (6/4) |
| credit-g (AUC) | +0.001 (4/6) | +0.001 (5/5) | -0.001 (3/7) | -0.005 (4/6) | -0.001 (3/7) | -0.002 (4/6) | -0.007 (3/7) | -0.007 (3/7) | -0.014 (1/9) |
| adult (AUC) | +0.015 (7/3) | +0.014 (7/3) | +0.014 (7/3) | +0.015 (7/3) | +0.014 (7/3) | +0.013 (7/3) | +0.013 (6/4) | +0.007 (7/3) | +0.010 (8/2) |
| boston (RMSE) | +0.552 (7/3) | — | — | — | — | — | — | +0.338 (8/2) | -0.125 (5/5) |
| **win rate, all datasets** | **0.77** | **0.73** | **0.70** | **0.68** | **0.65** | **0.70** | **0.62** | **0.62** | **0.53** |

### Leave-one-source-out, block

| dataset | `full_10k` | `full_3k` | `no_group_stats` | `no_row_mask` | `no_pattern_token` | `no_objectives` | `arch_off` | `tabicl_aware` | `tabpfn` |
|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | +0.013 (8/2) | +0.013 (8/2) | +0.013 (8/2) | +0.012 (9/1) | +0.013 (8/2) | +0.013 (8/2) | +0.011 (9/1) | +0.005 (8/1) | +0.005 (4/6) |
| wine (AUC) | +0.009 (4/4) | +0.008 (5/3) | +0.008 (4/4) | +0.007 (4/4) | +0.008 (4/3) | +0.007 (4/3) | +0.007 (4/4) | +0.001 (3/3) | +0.000 (3/5) |
| diabetes (RMSE) | +1.755 (9/1) | — | — | — | — | — | — | +1.048 (7/3) | +0.752 (7/3) |
| credit-g (AUC) | -0.001 (4/6) | -0.001 (4/6) | -0.001 (5/5) | -0.001 (4/6) | -0.002 (4/6) | -0.002 (4/6) | -0.001 (4/6) | +0.001 (5/5) | -0.014 (3/7) |
| adult (AUC) | +0.001 (7/3) | -0.000 (7/3) | -0.000 (7/3) | -0.000 (5/5) | +0.000 (7/3) | -0.001 (6/4) | -0.001 (5/5) | +0.001 (6/4) | -0.003 (4/6) |
| boston (RMSE) | +0.287 (6/4) | — | — | — | — | — | — | -0.022 (4/6) | -0.294 (4/6) |
| **win rate, all datasets** | **0.63** | **0.60** | **0.60** | **0.55** | **0.57** | **0.55** | **0.55** | **0.55** | **0.42** |

### Random split, block_shift

| dataset | `full_10k` | `full_3k` | `no_group_stats` | `no_row_mask` | `no_pattern_token` | `no_objectives` | `arch_off` | `tabicl_aware` | `tabpfn` |
|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | +0.000 (5/4) | +0.000 (5/3) | +0.001 (7/2) | +0.000 (5/4) | +0.000 (5/3) | +0.000 (5/4) | +0.000 (5/2) | +0.000 (5/3) | -0.000 (6/4) |
| wine (AUC) | -0.000 (2/5) | -0.000 (2/3) | -0.001 (1/5) | -0.000 (2/3) | -0.000 (2/4) | -0.000 (2/3) | -0.000 (2/4) | +0.000 (4/1) | -0.003 (0/9) |
| diabetes (RMSE) | +0.389 (8/2) | — | — | — | — | — | — | +0.150 (6/4) | -0.038 (4/6) |
| credit-g (AUC) | -0.000 (5/5) | +0.001 (6/4) | +0.001 (6/4) | +0.001 (6/4) | +0.000 (6/4) | +0.000 (5/5) | +0.001 (4/6) | +0.000 (4/6) | -0.007 (3/7) |
| adult (AUC) | +0.002 (7/3) | +0.001 (7/3) | +0.001 (7/3) | +0.001 (9/1) | +0.001 (7/3) | +0.001 (7/3) | +0.001 (8/2) | +0.001 (7/3) | +0.002 (8/2) |
| boston (RMSE) | +0.017 (4/6) | — | — | — | — | — | — | +0.022 (6/4) | -0.027 (4/6) |
| **win rate, all datasets** | **0.52** | **0.50** | **0.52** | **0.55** | **0.50** | **0.47** | **0.48** | **0.53** | **0.42** |

### Random split, block

| dataset | `full_10k` | `full_3k` | `no_group_stats` | `no_row_mask` | `no_pattern_token` | `no_objectives` | `arch_off` | `tabicl_aware` | `tabpfn` |
|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | -0.000 (4/6) | -0.000 (4/3) | -0.000 (3/4) | -0.000 (3/4) | -0.000 (2/5) | -0.000 (2/3) | +0.000 (4/4) | -0.000 (3/5) | -0.000 (4/6) |
| wine (AUC) | +0.001 (3/3) | +0.001 (4/1) | +0.001 (3/2) | +0.000 (2/3) | +0.001 (4/1) | +0.001 (3/2) | +0.000 (2/3) | +0.000 (3/2) | -0.001 (3/5) |
| diabetes (RMSE) | +0.443 (6/4) | — | — | — | — | — | — | +0.357 (9/1) | +0.146 (5/5) |
| credit-g (AUC) | +0.002 (6/4) | +0.001 (6/4) | +0.002 (7/3) | +0.002 (7/3) | +0.002 (8/2) | +0.002 (9/1) | +0.001 (5/5) | +0.001 (5/5) | -0.001 (5/5) |
| adult (AUC) | +0.002 (7/3) | +0.000 (4/6) | +0.001 (5/5) | +0.001 (5/5) | +0.001 (5/5) | +0.001 (6/4) | +0.001 (6/4) | +0.001 (6/4) | +0.002 (8/2) |
| boston (RMSE) | +0.083 (8/2) | — | — | — | — | — | — | +0.063 (8/2) | -0.004 (4/6) |
| **win rate, all datasets** | **0.57** | **0.45** | **0.45** | **0.42** | **0.48** | **0.50** | **0.43** | **0.57** | **0.48** |

<!-- sa-results:end -->

## What remains

1. **Block missingness with source shift.** Rerun the evaluation with per-source
   offset and noise injected in the block mechanism, and with splits by source.
   The random-split block case above does not exercise the source-structured prior.
2. **Leave-one-source-out on real data.** The compaction database with its
   provenance groups is the target case. Random splits overstate the result,
   because the model can learn the source instead of the physics.
3. **Ablate each part.** Each flag can be switched off. A part that adds nothing
   is dropped from the claim.
4. **A longer run.** 3000 steps at learning rate 1e-5 is a short continuation.
   The reconstruction loss was still falling at the end.

If the trained model does not beat mean imputation on the block case with source
shift, the honest result is that TabICLv2 is already robust to missing cells.

## Repository map

```
src/tabicl/prior/_missingness.py      block-structured and cell-wise missingness for prior tables
src/tabicl/_model/embedding.py        missing-aware column embedding (col_missing_aware)
src/tabicl/_model/layers.py           key padding mask through the induced self-attention block
src/tabicl/_model/interaction.py      per-feature token outputs for reconstruction
src/tabicl/_model/tabicl.py           flags, reconstruction head and loss, tolerant checkpoint loading
src/tabicl/train/_reconstruction.py   hide-mask sampling for the reconstruction objective
src/tabicl/train/_run.py              joint loss in the trainer
src/tabicl/_sklearn/                  NaN pass-through when the model is missing-aware
scripts/train_v2_missing_stage4.sh    continued pre-training recipe
scripts/ablation_missingness.py       evaluation runner
checkpoints/tabicl-m/                 stage-4 checkpoints (git LFS) and the launcher that produced them
results/ablation_v2/                  evaluation of the released weights before stage 4
results/ablation_m/                   evaluation of the trained checkpoints, with the runner script
tests/test_prior_missingness.py       tests for each part (62 in total)
tests/test_missing_aware_embedding.py
tests/test_reconstruction_head.py
tests/test_ablation_runner.py
docs/tabicl_m_architecture.md         architecture, objective, and file-by-file revisions
docs/figures/missingness_prior/       diagrams: architecture, prior mechanism, pipeline (PNG and SVG)
```

Run the tests with `pytest tests/`. The four new files need no checkpoint. On
macOS, XGBoost and torch load two different OpenMP runtimes and can deadlock in one
process; the ablation runner fits tree baselines in a spawned child for that reason.

## Inherited features

Everything below comes from upstream TabICLv2 and is unchanged.

**KV cache and persistence.** `TabICLClassifier(kv_cache=True)` caches the
training context during `fit` for fast repeated `predict`. `clf.save(path)` and
`TabICLClassifier.load(path)` persist a fitted estimator, optionally without the
training data when a cache exists.

**Parameters.** `n_estimators=8`, `norm_methods`, `feat_shuffle_method="latin"`,
`class_shuffle_method="shift"`, `outlier_threshold=4.0`,
`softmax_temperature=0.9`, `average_logits=True`, `support_many_classes=True`,
`batch_size=8`, `model_path`, `checkpoint_version`, `device`, `use_amp="auto"`,
`use_fa3="auto"`, `offload_mode="auto"`, `random_state=42`, `n_jobs`,
`inference_config`. See the class docstrings.

**Available upstream checkpoints.** `tabicl-classifier-v2-20260212.ckpt` and
`tabicl-regressor-v2-20260212.ckpt` (default), plus the v1 and v1.1 classifiers.
They download from Hugging Face on first use.

**Fine-tuning.** `FinetunedTabICLClassifier` and `FinetunedTabICLRegressor`
adapt a checkpoint to one dataset with AdamW, early stopping, and multi-GPU under
`torchrun`. See `tutorials/finetune_classifier.py`.

**Time series.** `TabICLForecaster` does zero-shot forecasting through the
regressor. See `tutorials/time_series_forecasting.py`.

**Explainability.** `tabicl.shap` computes SHAP values using an all-NaN background
row. With the released checkpoints the all-NaN columns are handled by the wrapper.

**Pre-training from scratch.** The three-stage TabICLv2 recipes are in
`scripts/train_v2_{clf,reg}_stage{1,2,3}.sh`. Prior tables can be generated on the
fly or written to disk with `python -m tabicl.prior`.

**Preprocessing.** Categorical columns are ordinal-encoded, outliers clipped,
features scaled and normalised, and features shuffled across ensemble members.
For heterogeneous raw data, [skrub](https://skrub-data.org) `TableVectorizer` in a
scikit-learn pipeline works well in front of the estimators.

## Citation

TabICL-M has no paper yet. If you use this code, cite the upstream TabICL papers:

```bibtex
@inproceedings{qu2025tabicl,
  title={Tab{ICL}: {A} Tabular Foundation Model for In-Context Learning on Large Data},
  author={Qu, Jingang and Holzm{\"u}ller, David and Varoquaux, Ga{\"e}l and Le Morvan, Marine},
  booktitle={International Conference on Machine Learning},
  year={2025}
}

@article{qu2026tabiclv2,
  title={{TabICLv2}: {A} better, faster, scalable, and open tabular foundation model},
  author={Qu, Jingang and Holzm{\"u}ller, David and Varoquaux, Ga{\"e}l and Le Morvan, Marine},
  booktitle={International Conference on Machine Learning},
  year={2026}
}
```

## Authors and license

TabICL-M: Sompote Youwai, King Mongkut's University of Technology Thonburi.

Upstream TabICL: Jingang Qu, David Holzmüller, Marine Le Morvan, and Gaël
Varoquaux (Inria Soda). Both are released under the BSD 3-Clause License, see
`LICENSE`.
