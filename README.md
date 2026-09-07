# TabICL-M: a tabular foundation model for incomplete tables

TabICL-M (M for missingness) extends [TabICLv2](https://github.com/soda-inria/tabicl)
so that it learns from tables in which not every row has every feature. It targets
the case that is common in engineering databases: the table is a merge of several
sources, and each source measured its own subset of the features. That is
block-structured missingness, not random gaps.

This repository is a fork of TabICL by Qu, Holzmüller, Varoquaux and Le Morvan.
All of TabICLv2 is still here and works unchanged. TabICL-M adds three parts on top,
each behind a flag, so each can be switched off for ablation.

**Status.** Research code, two generations of checkpoints, all in this repository
under git LFS (`git lfs pull`). The first stage-4 checkpoints
(`checkpoints/tabicl-m/<task>/step-3000.ckpt`) add the value-level parts only and
tie the mean-imputation baseline. The **source-aware** checkpoints
(`checkpoints/tabicl-m-sa-20k/<task>/step-10000.ckpt`, 20k steps in total) add a
representation of the *source* a row comes from. On 20 datasets they are the best
model when a held-out source carries a measurement offset (mean rank 2.22 against
2.45 for TabPFN-3 and 2.53 for TabPFN 2.5, 14 of 20 datasets won against TabPFN-3),
a close second to TabPFN-3 over all leave-one-source-out conditions (2.32 against
2.28), and second on random splits. See
[Source-aware TabICL-M](#source-aware-tabicl-m-what-was-done-and-what-it-shows)
and [What remains](#what-remains).

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

TabICL-M is trained by continuing from the released TabICLv2 weights with the new
parts switched on. They are zero at step 0, so the run starts exactly at the
released model on complete data. One GPU with 32 GB is enough with `DTYPE=bfloat16`.

```bash
pip install -e ".[pretrain]"
python -c "from tabicl import TabICLClassifier, TabICLRegressor; TabICLClassifier()._load_model(); TabICLRegressor()._load_model()"
bash scripts/train_v2_missing_stage4.sh clf                       # value-level parts (first checkpoints)
ARCH=source_aware bash scripts/train_v2_missing_stage4.sh clf     # source-aware parts (recommended)
```

The recipe, the prior regime, the loss trajectories of the runs, stage 4b, the
ablation recipe, the self-driving pipelines, and hardware and timing are in
[docs/training.md](./docs/training.md). All `--missing_*` options are listed by
`python -m tabicl.train --help`.

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

### Results of the first stage-4 checkpoint

Before training, the released weights inside the three TabICL paths did not differ,
as expected with the new parameters at zero. After the first stage 4 (value-level
parts only, 3000 steps) the model matched the released TabICLv2 within 0.001 AUC and
0.01 RMSE on complete data, tied the mean-imputation baseline within seed noise
under injected missingness, and both beat XGBoost and CatBoost on five of six
datasets. That result located the headroom in a held-out source with its own
feature subset and offset, which is what the source-aware model targets. Tables:
[docs/results.md](./docs/results.md).

## Source-aware TabICL-M: what was done and what it shows

The first stage-4 checkpoint told us where the headroom is
([Results of the first stage-4 checkpoint](#results-of-the-first-stage-4-checkpoint)): not under random gaps, where mean imputation
inside an in-context learner is already near the information limit, but when the
test rows come from a **source the context has never seen**, with its own feature
subset and its own measurement offset. There, every existing model, TabPFN-3
included, loses 0.02 to 0.08 AUC or 1 to 3 RMSE beyond the loss from the gaps
themselves (`results/headroom/`). The source-aware model is built for that case.

**The principle.** In a merged table, rows that share a missingness pattern come
from the same source. That is free, label-free provenance, and it is used at every
stage (all additions are zero-initialised or identity on complete data, so the run
still starts exactly at the released model; `tests/test_source_aware.py`):

| stage | addition | flag |
|---|---|---|
| column embedder | every observed cell is also fed standardised within the rows of its own pattern group (source-relative value) | `col_group_stats` |
| row interaction | feature tokens whose cells are all missing are excluded from the attention keys (observed-only rows) | `row_missing_aware` |
| row interaction | a learned query reads out which features a row lacks and adds it to the row representation (pattern token) | `pattern_token` |
| training | a pseudo-source loses a block of columns and the model reconstructs it; a view with per-source offset and noise must give the same predictions as the clean view | `--recon_mode`, `--consistency_weight` |
| prior | most incomplete tables are block-structured, shifted, with a source that appears only in the test rows; stage 4b uses stronger shifts and sources with as few as 20 % of the features | `ARCH=source_aware` |

**The result** (`results/broad/summary.md`; 20 datasets, block and block_shift
missingness at 30 % and 50 %, 5 seeds, ~400 conditions per split; mean rank over
five models, 1 = best):

| split | condition | **source-aware TabICL-M** | TabPFN-3 | TabPFN 2.5 | TabICLv2 + mean imputation | CatBoost |
|---|---|---|---|---|---|---|
| leave-one-source-out | with source offset | **2.22** | 2.45 | 2.53 | 3.21 | 4.59 |
| leave-one-source-out | all | 2.32 | **2.28** | 2.59 | 3.15 | 4.66 |
| leave-one-source-out | no offset | 2.42 | **2.11** | 2.65 | 3.09 | 4.73 |
| random split | all | 2.51 | **2.22** | 2.71 | 2.85 | 4.71 |

Paired against TabPFN-3 (same seeds, same deleted cells): with a source offset
105 wins / 95 losses and **14 of 20 datasets won**; over all leave-one-source-out
conditions 190 / 206 and 12 of 20; on random splits 173 / 218. Against TabPFN 2.5
the source-aware model wins in every summary (219 / 177 on leave-one-source-out,
16 of 20 datasets). Against the released TabICLv2 it wins 281 / 116 and 18 of 20.

Three sentences of interpretation. The model is the best available when a new
source arrives with its own calibration, which is the case it was built for, and
it holds that lead on 14 of 20 datasets against the strongest current tabular
foundation model. It is a close second to TabPFN-3 in general, and behind it when
a held-out source has no offset, which is a matter of base-model strength rather
than of the missingness mechanism. On random splits, where no source-aware
mechanism can help, the ordering is TabPFN-3, then this model, then TabPFN 2.5.

**What each part contributes** (`results/sa_ablation/summary.md`; classifier, 3000
steps each, win rate against mean imputation on held-out sources with offset):
all parts 0.73; without source-relative values 0.70; without the training
objectives 0.70; without observed-only rows 0.68; without the pattern token 0.65;
all parts off, new prior only 0.62; the first stage-4 checkpoint 0.62; all parts at
10k steps 0.77. Every part helps, the pattern token and the observed-only rows
most, the prior alone not at all, and more steps help.

**What did not work.** Two test-time options were tried on the trained model and
are negative results (`results/sa_eval/tt/`): letting the test rows attend in the
column set transformer is a coin flip (46 wins / 66 losses against the plain
model), and filling absent cells with the reconstruction head before predicting
hurts (29 / 83). Both are implemented (`embed_with_test`, `self_impute` on the
estimators) and off by default.

All tables, including those generated by the training pipeline, are in
[docs/results.md](./docs/results.md).



<!-- regression:start -->

### Regression against TabPFN-3 (auto-generated)

Regression is the half of the benchmark where TabPFN-3 leads, so it was attacked separately on the seven regression datasets. Test-time levers: 32 ensemble members (`_n32`), the median instead of the mean (`_med`), a target power-transform ensemble (`_ypow`), an extra quantile-normalisation member (`_qn`). Training lever: the regressor continued on a prior with half the tables complete (`_4c3500`, a 3500-step probe). None of them changes the head-to-head outside the source-offset case: the probe moved the random split by nothing (85 wins / 90 losses against the 20k model), so the planned full continuation runs were stopped rather than spend 25 GPU-hours on a flat curve. TabPFN-3 gains nothing from 32 members either (74/66), so the comparison is saturated on both sides. The residual gap is base regression strength inherited from TabICLv2, whose released regressor is itself far behind TabPFN-3 here (mean rank 6.43 against 3.95). Two more probes closed the question (`results/regression/probes_summary.md`): a weight soup of the 10k and 20k regressors gains nothing, and the gap on kin8nm exists at every training-set size and narrows with data, so it is not a sample-efficiency problem of in-context learning. Test-time fine-tuning on the context rows, with TabPFN-3 given the same treatment, recovers a third of the kin8nm gap and then plateaus; TabPFN-3 gets slightly worse when fine-tuned and its zero-shot model stays the best on both datasets, so fine-tuning is a shared lever that does not change the ordering. Full tables: `results/regression/summary.md`.

#### Leave-one-source-out, all: 140 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabicl_aware_n32_ypow_4c3500` | 4.60 | 13 | 67/73 | 3/7 | 140 |
| `tabpfn3_n32` | 4.69 | 32 | 78/62 | 5/7 | 140 |
| `tabpfn3` | 4.87 | 34 | — | — | 140 |
| `tabicl_aware_n32_ypow` | 4.95 | 2 | 69/71 | 3/7 | 140 |
| `tabicl_aware_n32` | 5.02 | 0 | 67/73 | 3/7 | 140 |
| `tabicl_aware_4c3500` | 5.05 | 12 | 67/73 | 3/7 | 140 |
| `tabicl_aware_ypow` | 5.13 | 5 | 66/74 | 3/7 | 140 |
| `tabicl_aware` | 5.15 | 3 | 67/73 | 3/7 | 140 |
| `tabicl_aware_med` | 5.54 | 38 | 61/79 | 3/7 | 140 |

Best of ours `tabicl_aware_n32_ypow_4c3500` vs `tabpfn3_n32`: 70/70 paired, datasets won 3/7, mean RMSE -2.85 % (positive = ours lower) -> **BEHIND**


#### Leave-one-source-out, with source offset: 70 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabicl_aware_4c3500` | 4.34 | 10 | 46/24 | 5/7 | 70 |
| `tabicl_aware_n32_ypow_4c3500` | 4.36 | 9 | 45/25 | 5/7 | 70 |
| `tabicl_aware_n32` | 4.71 | 0 | 44/26 | 5/7 | 70 |
| `tabicl_aware` | 4.71 | 3 | 44/26 | 5/7 | 70 |
| `tabicl_aware_n32_ypow` | 4.94 | 0 | 44/26 | 5/7 | 70 |
| `tabicl_aware_ypow` | 5.01 | 2 | 44/26 | 5/7 | 70 |
| `tabicl_aware_med` | 5.09 | 24 | 40/30 | 4/7 | 70 |
| `tabpfn3_n32` | 5.90 | 10 | 40/30 | 4/7 | 70 |
| `tabpfn3` | 5.96 | 11 | — | — | 70 |

Best of ours `tabicl_aware_n32_ypow_4c3500` vs `tabpfn3_n32`: 49/21 paired, datasets won 4/7, mean RMSE +2.15 % (positive = ours lower) -> **AHEAD**


#### Leave-one-source-out, no offset: 70 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabpfn3_n32` | 3.47 | 22 | 38/32 | 5/7 | 70 |
| `tabpfn3` | 3.79 | 23 | — | — | 70 |
| `tabicl_aware_n32_ypow_4c3500` | 4.84 | 4 | 22/48 | 2/7 | 70 |
| `tabicl_aware_n32_ypow` | 4.96 | 2 | 25/45 | 2/7 | 70 |
| `tabicl_aware_ypow` | 5.25 | 3 | 22/48 | 2/7 | 70 |
| `tabicl_aware_n32` | 5.34 | 0 | 23/47 | 2/7 | 70 |
| `tabicl_aware` | 5.59 | 0 | 23/47 | 2/7 | 70 |
| `tabicl_aware_4c3500` | 5.76 | 2 | 21/49 | 2/7 | 70 |
| `tabicl_aware_med` | 6.00 | 14 | 21/49 | 3/7 | 70 |

Best of ours `tabicl_aware_n32_ypow` vs `tabpfn3_n32`: 21/49 paired, datasets won 2/7, mean RMSE -8.31 % (positive = ours lower) -> **BEHIND**


#### Leave-one-source-out: per-dataset means at rate 0.5

| dataset | mechanism | `tabicl_aware` | `tabicl_aware_4c3500` | `tabicl_aware_med` | `tabicl_aware_n32` | `tabicl_aware_n32_ypow` | `tabicl_aware_n32_ypow_4c3500` | `tabicl_aware_ypow` | `tabpfn3` | `tabpfn3_n32` |
|---|---|---|---|---|---|---|---|---|---|---|
| diabetes | block | 64.111 | 64.274 | **63.725** | 64.040 | 64.073 | 64.200 | 64.134 | 63.980 | 63.840 |
| diabetes | block_shift | 65.124 | 65.077 | 65.204 | 65.058 | 65.061 | **65.053** | 65.136 | 65.454 | 65.558 |
| openml:189 | block | 0.249 | 0.250 | 0.249 | 0.249 | **0.249** | 0.249 | 0.249 | 0.250 | 0.250 |
| openml:189 | block_shift | 0.234 | 0.235 | 0.235 | 0.234 | **0.234** | 0.234 | 0.234 | 0.235 | 0.235 |
| openml:42225 | block | 1463.375 | 1444.566 | 1538.244 | 1425.110 | 1416.240 | 1405.651 | 1452.023 | 1292.578 | **1291.293** |
| openml:42225 | block_shift | 2207.693 | 2181.016 | 2191.633 | 2169.169 | 2171.965 | 2158.415 | 2201.133 | 2162.967 | **2087.939** |
| openml:44970 | block | 1.132 | 1.136 | **1.127** | 1.133 | 1.134 | 1.138 | 1.132 | 1.135 | 1.133 |
| openml:44970 | block_shift | 1.346 | **1.339** | 1.339 | 1.346 | 1.347 | 1.341 | 1.346 | 1.347 | 1.346 |
| openml:507 | block | 0.185 | **0.185** | 0.185 | 0.185 | 0.185 | 0.185 | 0.185 | 0.211 | 0.209 |
| openml:507 | block_shift | 0.186 | 0.186 | **0.186** | 0.186 | 0.186 | 0.186 | 0.186 | 0.199 | 0.200 |
| openml:531 | block | 5.675 | 5.593 | 5.863 | 5.668 | 5.688 | 5.585 | 5.699 | **4.942** | 4.946 |
| openml:531 | block_shift | 6.716 | **6.689** | 7.031 | 6.722 | 6.718 | 6.694 | 6.711 | 6.814 | 6.822 |
| openml:560 | block | 5.044 | 5.035 | 4.983 | 4.955 | 4.955 | 4.958 | 5.046 | **4.526** | 4.540 |
| openml:560 | block_shift | 5.651 | 5.623 | 5.640 | 5.613 | 5.613 | 5.589 | 5.648 | 5.359 | **5.302** |

#### Random split, all: 138 conditions

| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won | conditions |
|---|---|---|---|---|---|
| `tabpfn3` | 3.51 | 42 | — | — | 140 |
| `tabpfn3_n32` | 3.58 | 50 | 74/66 | 5/7 | 140 |
| `tabicl_aware_n32_ypow_4c3500` | 4.70 | 8 | 43/97 | 1/7 | 140 |
| `tabicl_aware_n32_ypow` | 4.73 | 9 | 42/98 | 1/7 | 140 |
| `tabicl_aware_ypow` | 5.07 | 8 | 42/98 | 1/7 | 140 |
| `tabicl_aware_n32` | 5.09 | 4 | 40/98 | 0/7 | 138 |
| `tabicl_aware_4c3500` | 5.33 | 7 | 41/99 | 1/7 | 140 |
| `tabicl_aware` | 5.42 | 2 | 42/98 | 1/7 | 140 |
| `tabicl_aware_med` | 7.57 | 8 | 30/110 | 0/7 | 140 |
| `tabicl_aware_n32_ypow_qn` | — | — | 31/53 | 3/7 | 84 |

Best of ours `tabicl_aware_n32_ypow_qn` vs `tabpfn3_n32`: 30/54 paired, datasets won 3/7, mean RMSE -0.55 % (positive = ours lower) -> **BEHIND**


Verdict (best of ours against TabPFN-3 at its best setting): **loso=BEHIND loso[with_source_offset]=AHEAD loso[no_offset]=BEHIND random_split=BEHIND**.

<!-- regression:end -->

## What remains

1. **Plain block missingness on a held-out source.** TabPFN-3 leads there (mean
   rank 2.11 against 2.42). The gap is base-model strength, not the missingness
   mechanism; closing it needs a stronger base or a longer stage 4 on the full
   TabICL prior.
2. **Real multi-source data.** All source structure so far is synthetic (sources
   drawn on complete tables). The compaction database with its provenance groups,
   leave-one-lab-out, is the intended test and has not been run.
3. **Significance.** Five seeds and 20 datasets give paired win rates of 52 to
   57 % against TabPFN-3 under source offset. More seeds, and datasets with
   natural source structure, are needed before the claim is stated as a
   difference rather than a rank.
4. **Base regression strength.** TabPFN-3 leads on regression wherever no source
   offset is involved, and the gap is inherited: the released TabICLv2 regressor is
   itself far behind it on these datasets. Test-time ensembling, a target power
   transform and a continuation on a more complete prior all failed to move it
   (see the regression section above); so did test-time fine-tuning on the
   context rows, which recovers a third of the gap and plateaus while TabPFN-3
   gains nothing from it. Closing it needs a stronger base regressor, not more
   missingness training or adaptation.
5. **Intervals.** Under a held-out source the source-aware regressor is calibrated
   (80 % coverage 0.81, width 1.6 target standard deviations) where the released
   model over-covers (0.87, width 2.1). TabPFN's quantiles were not recorded; the
   comparison of interval quality is open.

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
checkpoints/tabicl-m/                 first stage-4 checkpoints (git LFS) and the launcher that produced them
checkpoints/tabicl-m-sa/              source-aware stage 4: launcher, self-driving pipelines (training, ablation, stage 4b, benchmark), 10k checkpoints
checkpoints/tabicl-m-sa-20k/          source-aware checkpoints after stage 4b (git LFS): the ones to use
results/headroom/                     where the headroom is: split by source vs random, shift vs none, every baseline incl. TabPFN 2.5 / 2.6 / 3
results/sa_eval/, results/sa_eval_20k/ source-aware checkpoints against the baselines (10k, 20k)
results/sa_ablation/                  per-part ablation
results/broad/                        20-dataset benchmark against TabPFN 2.5 and TabPFN-3
results/ablation_v2/                  evaluation of the released weights before stage 4
results/ablation_m/                   evaluation of the trained checkpoints, with the runner script
tests/test_prior_missingness.py       11 tests: rates, mechanisms, source structure, safety rules of the prior
tests/test_missing_aware_embedding.py 22 tests: column embedding equals TabICLv2 on complete data, NaN handling, KV cache
tests/test_reconstruction_head.py     11 tests: hide-mask sampling, reconstruction loss, head dropped at inference
tests/test_source_aware.py            15 tests: group statistics, observed-only rows, pattern token, block reconstruction, consistency
tests/test_ablation_runner.py         24 tests: injection mechanisms, source split, pattern normalisation, scoring
docs/training.md                      training recipes, runs, pipelines, hardware and timing
docs/results.md                       all result tables
docs/tabicl_m_architecture.md         architecture, objective, and file-by-file revisions
docs/figures/missingness_prior/       diagrams: architecture, prior mechanism, pipeline (PNG and SVG)
```

Run the tests with `pytest tests/`. The five TabICL-M files (83 tests) need no
checkpoint and run on the CPU in a few seconds. On
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
