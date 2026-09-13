# Residual input encoder: controlled ordinary-regression experiment

**Completed September 13, 2026:** both arms trained for 2,000 steps after the
ordinary TabICL-Large continuation, followed by all four evaluations. Neither arm
was interrupted. The experiment did not meet the advancement criteria; no further
full training or checkpoint promotion followed.

| Condition | Encoder RMSE gain over matched control |
|---|---:|
| Complete data | +0.076% |
| Random split, block missingness | −0.031% |
| Random split, block + shift | +0.045% |
| Held-out source, block missingness | −0.459% |
| Held-out source, block + shift | +0.591% |

Positive means lower error. The complete-data gain was below 1% and improved
four of seven datasets, below the required five. Both arms were evaluated freshly
on GPU. Concurrent CPU evaluations may have affected training time, so timings
should not be treated as isolated architecture overhead.
[Full results](../results/residual_input_experiment/report.md).

Local experimental weights (not released):

- Control: `results/residual_input_experiment/checkpoints/control/reg/step-2000.ckpt`
- Encoder: `results/residual_input_experiment/checkpoints/residual/reg/step-2000.ckpt`

## Architecture and compatibility

The experimental column projection is:

```
embedding = existing_projection(x) + Linear(64, 128)(GELU(Linear(group_size, 64)(x)))
```

The MLP is shared across feature groups. Its final weight and bias start at zero;
all existing predictor weights are copied exactly. For the current three-value
groups and embedding width 128, the branch adds **8,576 parameters**. The existing
18-block predictor and quantile head remain unchanged. Existing preprocessing,
categorical encodings, and missing-value zero-filling are reused.

`col_residual_mlp=False` is the default model/checkpoint/training flag. Legacy
checkpoints load unchanged. To create a new variant from an old checkpoint, use
`tabicl.train._residual_input.add_residual_input`; it adds only the new branch and
discards optimizer state. Merely enabling the flag when loading an old state dict
is intentionally insufficient: loading remains strict about missing weights.

The branch is used by both ordinary and cached column projections. CPU tests check
cache equivalence with a nonzero branch and source-relative statistics disabled.
The inherited source-relative statistics depend on the rows supplied together;
cache equivalence for that existing mode is not established by these tests. The
experiment evaluates both arms with the default uncached estimator.

## Training and evaluation

Both arms start from the final ordinary-regression checkpoint and receive 2,000
additional steps with seed 45, fresh optimizers, learning rate 3e-5, and a fresh
cosine schedule with 5% warmup. Batch 32, bf16, 8,192 maximum rows, Muon, and
activation checkpointing match the ordinary run. Missingness, measurement shifts,
reconstruction, consistency, smooth-target replacement, and added MSE are disabled.
The arms run sequentially: control, then residual encoder.

Save every 250 steps, retaining the latest temporary checkpoint and the final
2,000-step checkpoint for each arm. This bounds disk usage. A resumed run is
reported, but cannot automatically qualify for advancement because restarting
workers changes synthetic-data streams. Training timing includes startup and data
generation; the comparison uses equal steps, not equal compute time.

Evaluation uses the existing seven development datasets, seeds 0–2, eight estimators,
and a 3,000-row cap. It includes complete data, random-split block missingness and
block-plus-shift, and both held-out-source conditions. Complete-data rows are counted
once. Report equal-dataset paired RMSE gains, datasets won, 80% interval coverage,
paired interval-width ratios, inference time, parameters, and training time.

Advance to independent validation only if complete-data mean RMSE gain is at least
1%, at least five of seven datasets improve, and neither held-out-source condition
has mean RMSE degradation above 2%. Passing does not promote weights or launch
another full training run. One training seed and reused development datasets do
not establish superiority to TabPFN-3.

## Operation

```bash
python scripts/regression_residual_input_experiment.py --wait-for-source
```

The Supervisor service is `tabicl-residual-input-experiment`. It waits for the
ordinary runner's completion status, final checkpoint, and released process lock;
it stops on failure rather than interrupting or restarting that training. Once the
source completes, full-size checkpoint loading and exact initial prediction checks
run before either experiment arm. Source, initialization, and code hashes prevent
silent mixing of different runs after a restart.

Outputs: `results/residual_input_experiment/`, including `status.json`,
`manifest.json`, `train_<arm>.log`, `timing_<arm>.json`, evaluation directories,
`comparison.csv`, `per_dataset.csv`, `decision.json`, and `report.md`.

Validation command:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m pytest tests/test_residual_input.py tests/test_residual_input_experiment.py tests/test_expand_depth.py tests/test_point_loss.py -q
```
