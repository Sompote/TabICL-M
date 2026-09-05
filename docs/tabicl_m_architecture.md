# TabICL-M: architecture and revisions

This page records what TabICL-M changes in TabICLv2, where each change lives, and
why. Three figures carry the mechanism. The text gives tensor shapes, the training
objective, and a file-by-file list of the edits with their size.

## 1. The architecture

![TabICL-M architecture: three stages of TabICLv2 with the missing-aware column embedding and the reconstruction head added](./figures/missingness_prior/architecture.svg)

TabICLv2 processes a table in three stages. TabICL-M keeps all three and adds to
the first two. Green boxes are new. Every new parameter starts at zero, so on a
table with no missing cell the output is identical to TabICLv2.

**Input.** A table `X` of shape `(B, T, H)`: `B` tables in a batch, `T` rows, `H`
features. The first `train_size` rows carry a label `y`, the rest are test rows.
Cells may be `NaN`. During pre-training a further fraction of the observed cells is
hidden and also fed as `NaN` (orange in the figure).

**Stage 1, column-wise embedding.** Each column is embedded by a set transformer
shared by all columns. TabICLv2 groups three features per token by circular
permutation, so token `g` holds features `g+1`, `g+2`, `g+4` modulo `H`. The
changes:

1. The token's cells are split into a zero-filled value part and a binary missing
   indicator `m`. The input projection becomes `in_linear(x) + mask_linear(m)`.
   `mask_linear` is new and starts at zero.
2. The set transformer uses 128 inducing points that attend to the training rows.
   Tokens whose three cells are all missing are removed from the keys of that
   attention with a key padding mask. The column statistics are therefore
   computed from observed cells only. A guard keeps all keys for a column that has
   no observed training cell at all, so the attention stays defined.
3. A learned absence vector, one per input dimension, is added to the final
   embedding of each missing cell. It starts at zero.

Output: embeddings of shape `(B, T, H + C, E)` with `E = 128` and `C = 4` slots
reserved for CLS tokens.

**Stage 2, row-wise interaction.** A transformer with rotary position encoding
runs over the `H + C` tokens of each row. TabICLv2 queries only the four CLS
tokens in the last block and concatenates them into a row representation of size
`4E = 512`. TabICL-M adds an option to query all tokens in the last block. The CLS
outputs are unchanged, because the output of a query does not depend on which other
queries are present. The extra feature-token outputs, shape `(B, T, H, E)`, go to a
reconstruction head, a linear map from `E` to the three values of the token's
feature group. The head exists only when `reconstruction=True` and is never used at
inference.

**Stage 3, dataset-wise in-context learning.** Unchanged. Twelve transformer
blocks over rows, with test rows attending to training rows, and a head that
outputs class logits or 999 quantiles.

## 2. The training objective

The trainer hides up to 30 % of the observed cells of a table with probability
0.5 per table, feeds the result, and minimises

```
loss = task_loss + recon_weight · reconstruction_loss
```

where `task_loss` is cross-entropy or pinball loss on the test rows as in TabICLv2,
and `reconstruction_loss` is smooth-L1 between the head output and the true value
on hidden cells only. Cells that were `NaN` in the table before hiding are never
part of the loss. `recon_weight` is 0.1 by default. Both losses are logged
separately.

## 3. The pre-training prior

![How a complete synthetic table becomes an incomplete one](./figures/missingness_prior/mechanism.svg)

TabICLv2 pre-trains on complete synthetic tables from structural causal models.
TabICL-M applies a missingness transform to every table after generation, so it
works with every prior type. Two mechanisms are drawn per table and may stack.

**Block-structured.** Rows are split into 2 to 8 sources with Dirichlet row
shares. Each source observes a fraction 0.3 to 1 of the features, with a core set
seen by all. Numeric features can receive a per-source offset up to 0.5 σ and noise
up to 0.3 σ, which imitates laboratories that measure differently. With probability
0.25 the sources occupy contiguous row blocks, so some sources fall entirely in the
test part, like a leave-one-source-out split. With probability 0.5 the source id is
appended as a categorical feature at a random column.

**Cell-wise.** One mechanism per table: MCAR, MAR with a logistic dependence on
another column, or MNAR with a logistic dependence on the cell's own value or
quantile censoring. The logistic intercept is solved by bisection so the mean
missing probability equals the sampled rate. Per-column rates follow
`0.7 · Beta(0.7, 2.5)`, mean about 0.15.

Two safety rules run last: every feature keeps at least two observed training
cells, and every row keeps at least one observed feature. The target is never
masked.

![Where the missingness transform sits in the pre-training pipeline](./figures/missingness_prior/pipeline.svg)

The transform is called once per batch inside `PriorDataset.get_batch`, handles
dense and nested tensors, and returns the same five-tuple as before. Missing cells
survive the sparse on-disk format.

## 4. Revisions, file by file

Line counts are insertions and deletions against the upstream commit.

| File | Change | Lines |
|---|---|---|
| `src/tabicl/prior/_missingness.py` | New. Config, cell-wise and block mechanisms, safety rules, batch wrapper, CLI flags | 564 new |
| `src/tabicl/prior/_dataset.py` | `PriorDataset(missingness=...)` and the call in `get_batch` | +14 −1 |
| `src/tabicl/prior/_genload.py` | Generator CLI flags, config pass-through, config written to `metadata.json` | +5 −0 |
| `src/tabicl/_model/layers.py` | `key_padding_mask` through `InducedSelfAttentionBlock`, including the skip path and the KV-cache path | +31 −9 |
| `src/tabicl/_model/encoders.py` | `key_padding_mask` through `SetTransformer`, including gradient checkpointing | +17 −4 |
| `src/tabicl/_model/embedding.py` | `missing_aware` flag, `mask_linear`, absence vector, observed-only keys, in the training, inference and cache paths | +106 −8 |
| `src/tabicl/_model/interaction.py` | `return_tokens` option: full-query last block, split CLS from feature tokens | +39 −9 |
| `src/tabicl/_model/tabicl.py` | `col_missing_aware` and `reconstruction` flags, `recon_head`, `reconstruction_loss`, `return_tokens`, tolerant `load_pretrained_state_dict` | +110 −6 |
| `src/tabicl/train/_reconstruction.py` | New. Samples the hide mask over observed, active cells | 64 new |
| `src/tabicl/train/_run.py` | Joint loss, separate logging, `col_missing_aware` and `reconstruction` in the model config, tolerant checkpoint loading | +45 −7 |
| `src/tabicl/train/_train_config.py` | `--col_missing_aware`, `--recon_weight`, `--recon_rate_max`, `--recon_p_apply`, `--missing_*` | +29 −0 |
| `src/tabicl/_sklearn/preprocessing.py` | `TransformToNumerical(impute=False)` keeps NaN; scaler, outlier remover and normalisers ignore NaN in their statistics | +38 −21 |
| `src/tabicl/_sklearn/sklearn_utils.py` | NaN-tolerant `check_array` keyword across scikit-learn versions | +12 −0 |
| `src/tabicl/_sklearn/classifier.py`, `regressor.py` | Skip imputation when the loaded model is missing-aware | +4 −1 each |
| `scripts/train_v2_missing_stage4.sh` | New. Continued pre-training recipe from the released checkpoint | new |
| `scripts/ablation_missingness.py` | New. Evaluation runner | 702 new |
| `tests/test_prior_missingness.py` | 11 tests | new |
| `tests/test_missing_aware_embedding.py` | 22 tests | new |
| `tests/test_reconstruction_head.py` | 11 tests | new |
| `tests/test_ablation_runner.py` | 18 tests | new |

Total in `src/`: 14 files, 456 insertions, 68 deletions, plus two new modules.

## 5. Invariants the tests enforce

- With `col_missing_aware=True` and no `NaN` in the input, the output equals
  TabICLv2 to 1e-6, in train and eval mode, for classification and regression.
- Masked keys change nothing for observed rows. Running the block with the masked
  rows removed gives the same output as running it with the mask.
- The KV-cache path with `NaN` matches the plain forward within bfloat16
  tolerance.
- The prediction with `return_tokens=True` equals the prediction without it.
- The reconstruction loss is zero on an empty mask, ignores cells that were `NaN`
  in the target, and its gradient reaches the row-wise block.
- On a table where column 1 equals column 0, 60 optimisation steps halve the
  reconstruction loss.
- A checkpoint trained without the flags loads into a model with the flags on, and
  only `mask_linear`, `absence` and `recon_head` are reported as kept at zero.
- The scikit-learn wrappers pass `NaN` through for a missing-aware model and
  impute for a plain model. The existing upstream tests still pass with the
  released checkpoint.

## 6. Reading the diagrams as a reviewer

The claim of TabICL-M rests on three things that the diagrams make visible.
First, the prior produces tables whose gaps are structured by source, with
measurement shift between sources. Second, the column embedding computes its
statistics from observed cells only, rather than from imputed values. Third, the
row-wise block is trained to fill in absent features explicitly through the
reconstruction head. Each can be switched off, so the ablation can attribute any
gain to one of them. Before stage-4 training, none of the three has an effect,
and the evaluation confirms that the untrained architecture matches TabICLv2.
