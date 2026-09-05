# TabICL-M: a tabular foundation model for incomplete tables

TabICL-M (M for missingness) extends [TabICLv2](https://github.com/soda-inria/tabicl)
so that it learns from tables in which not every row has every feature. It targets
the case that is common in engineering databases: the table is a merge of several
sources, and each source measured its own subset of the features. That is
block-structured missingness, not random gaps.

This repository is a fork of TabICL by Qu, Holzmüller, Varoquaux and Le Morvan.
All of TabICLv2 is still here and works unchanged. TabICL-M adds three parts on top,
each behind a flag, so each can be switched off for ablation.

**Status.** Research code. The three parts are implemented and tested. The
missing-aware model has not been pre-trained yet, so there is no TabICL-M checkpoint
to download. The evaluation so far compares the released TabICLv2 weights under
injected missingness. See [Results so far](#results-so-far) and
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
| TabICL-M, `col_missing_aware` | kept as NaN | kept as NaN | observed cells only | yes, after stage 4 |

## Continued pre-training (stage 4)

TabICL-M is trained by continuing from the released TabICLv2 weights with the
three parts switched on. The new parameters are zero at step 0, so the run starts
exactly at the released model on complete data. One GPU with 24 GB is enough for
the default settings.

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
NUM_GPUS=4 RECON_WEIGHT=0.05`. The trainer logs the task loss and the
reconstruction loss separately. The task loss should stay near its starting value.
The reconstruction loss should fall. Checkpoints are written to
`checkpoints/tabicl-m/<task>/step-*.ckpt` and load directly into the estimators.

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

Released TabICLv2 weights only, before any stage-4 training. Three datasets, three
mechanisms, three rates, three seeds, 360 fits. Diabetes regression, RMSE, mean
over seeds:

| Mechanism | Rate | `tabicl_impute` | `tabicl_indicator` | `tabicl_aware_zero` | `xgboost` |
|---|---|---|---|---|---|
| complete | 0.0 | 56.6 | 56.6 | 56.6 | 62.1 |
| MCAR | 0.3 | 61.9 | 61.8 | 62.0 | 67.5 |
| MCAR | 0.5 | 65.6 | 65.5 | 65.5 | 69.9 |
| MNAR | 0.5 | 62.6 | 62.2 | 63.3 | 71.0 |
| block | 0.5 | 63.8 | 63.6 | 63.5 | 69.7 |

The seed spread is 1 to 3 RMSE units, so the three TabICL variants do not differ.
This is the expected result before training: the new parameters are zero. It
establishes two facts. The architecture change does not hurt. And the baseline is
strong: mean imputation inside an in-context learner already absorbs most of the
damage, with the 80 % interval widening from 1.75 to 2.09 target standard
deviations as the deletion rate rises to 0.5 and coverage staying between 0.77 and
0.81. Whether TabICL-M improves on this is decided by the stage-4 run and the
leave-one-source-out test. Full tables: `results/ablation_v2/summary.md`.

## What remains

1. **Stage-4 training.** Run `scripts/train_v2_missing_stage4.sh` for the
   classifier and the regressor on a GPU. Check that the task loss stays flat and
   the reconstruction loss falls.
2. **Trained ablation.** Rerun the evaluation with `--aware_ckpt` and
   `--aware_ckpt_reg`, on harder datasets than the built-in ones, and with
   per-source offset and noise injected in the block mechanism. The built-in
   classification sets sit at AUC 0.98 to 1.00 and cannot separate the models.
3. **Leave-one-source-out on real data.** The compaction database with its
   provenance groups is the target case. Random splits overstate the result,
   because the model can learn the source instead of the physics.
4. **Ablate each part.** Each flag can be switched off. A part that adds nothing
   is dropped from the claim.

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
