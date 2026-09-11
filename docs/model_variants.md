# Model variants

## Naming

**M means Missing**, for training and architecture designed to handle incomplete
tables. **Large** identifies the deeper model. Use **TabICL-M-Large**, not
TabICL-MM, for the completed Large regression model.

| Name | Meaning | Availability |
|---|---|---|
| TabICL-M | Original missing-aware model | Classification and regression |
| TabICL-M-Large | Larger missing-aware model | Regression only |
| TabICL-Large | Ordinary-regression continuation of Large | 20k-step run started; not evaluated |

Repository/package identity remains TabICL-M (`tabicl-m`), with compatible
`tabicl` imports and `TabICLRegressor` / `TabICLClassifier` estimator names.
Checkpoint paths retain their training-run names.

## Checkpoints

Paths are relative to the repository root:

| Model | Task | Checkpoint |
|---|---|---|
| TabICL-M | Regression | `checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt` |
| TabICL-M | Classification | `checkpoints/tabicl-m-sa-20k/clf/step-10000.ckpt` |
| TabICL-M-Large | Regression | `results/large_regression_20k/checkpoints/reg/step-20000.ckpt` |

The original checkpoints use Git LFS. The Large checkpoint is currently a local
training artifact, ignored by Git; pushing the documentation alone does not
publish it. Download or copy that checkpoint to your environment before using
this example. A suggested release filename is `tabicl-m-large-reg-v1.ckpt`.

```python
from tabicl import TabICLRegressor

model = TabICLRegressor(
    model_path="results/large_regression_20k/checkpoints/reg/step-20000.ckpt"
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
q10, q90 = model.predict(
    X_test, output_type="quantiles", alphas=[0.1, 0.9]
).T
```

For classification, use `TabICLClassifier` with the classifier path above and
`predict_proba`. There is no Large classifier checkpoint. Omitting `model_path`
selects the upstream checkpoint rather than either missing-aware variant.

## Architecture and training

The original regressor has 12 ICL blocks and 28,678,754 parameters. Large has
18 blocks and 41,539,682 parameters. Both keep embedding width 128 and four row
summary tokens. Six identity-initialized residual blocks were inserted into the
original regressor, preserving its predictions before further training.

Large completed **20,000 continuation steps** after expansion, in addition to the
training already represented in its starting checkpoint. Its main regression
objective is pinball loss, with reconstruction and consistency auxiliary losses.
It uses the original graph-based synthetic prior and source-aware missingness;
it does not use the experimental smooth-target replacement or added MSE loss.

**70% of generated tables are selected for the missingness transform.** The
fraction of cells hidden within a selected table depends on the sampled pattern
and rate. Approximately 30% bypass that transform; reconstruction can still hide
additional cells. This is not a claim that 70% of every table is missing.

See the [training recipe](regression_large_20k.md) and
[depth expansion details](regression_large_experiment.md).

## Evaluation and model choice

Large's strongest result is on held-out synthetic sources with block missingness
and measurement shifts: 9.20% lower RMSE than the original and 13.52% lower than
archived TabPFN-3 results. On complete data it has 2.20% higher RMSE than the
original and 3.49% higher than TabPFN-3. These are equal-dataset averages of paired
percentage gains, not percentages computed from pooled RMSE.

Keep the original model as a baseline and evaluate Large on your own source
splits. The seven development datasets, injected missingness/source effects,
and one pretraining seed do not establish performance on all real incomplete
tables. Extra capacity and additional training were changed together, so these
results do not isolate the benefit of model size.

[Full results and protocol](../results/large_regression_20k_eval/report.md).
[Ordinary-regression TabICL-Large continuation](regression_large_ordinary_20k.md)
has started separately. It retains the source architecture and pretrained weights,
but disables injected missingness, source shifts, and auxiliary masking/losses.
