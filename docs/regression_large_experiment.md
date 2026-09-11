# TabICL-M-Large depth pilot

**Historical pilot:** stopped before its first checkpoint and replaced by the
[completed 20k run](regression_large_20k.md).

Run `python scripts/regression_large_experiment.py`; use `--prepare-only` to
expand and verify the checkpoint without training. On this instance, the full
pilot is managed by Supervisor as `tabicl-regression-large`. Outputs are in
`results/large_regression`.

The prototype expands the original source-aware regressor from 12 to 18 ICL
blocks: 28,678,754 to 41,539,682 parameters. Embedding width remains 128 and the
four row summary tokens remain unchanged. Six new blocks are inserted after
every second original block. Each copies the preceding block's internal weights
but zeroes its attention output projection and second feedforward projection,
including biases. Pre-norm residual structure makes these blocks identities at
initialization. Original weights are copied exactly, and optimizer state is
discarded. Post-norm expansion is explicitly rejected.

Verification in `expansion_checks.json` covers strict weight loading, exact
prediction equality on sampled complete and incomplete tables, equality through
the public regressor API, nonzero output-projection gradients in all new blocks,
and nonzero input-projection gradients after one optimizer update. Internal branch
gradients are initially blocked by the zero output projections; this is expected.
These checks establish behavior on the tested inputs, not every possible input.

Both the expanded model and a fresh 12-block control receive 1,000 steps, batch 32,
learning rate 3e-5 with a fresh cosine schedule, original graph prior, pinball loss,
and the previous source-aware missingness/reconstruction/consistency settings.
Smooth-target replacement and point loss are disabled. Gradient checkpointing is
enabled for **both** arms to fit the larger model on the 32 GB GPU. Individual
random training tables need not match, because initialization consumes different
amounts of RNG state; distributions and configured seeds are matched.

Checkpoints are saved every 250 steps. After training, checkpoints 250, 500 and
1,000 are evaluated on five synthetic function families at fresh seeds 30–32.
`validation_curve.csv` records normalized RMSE, normalized pinball loss at three
quantiles, and 80% interval coverage. Final checkpoints are evaluated on the seven
existing real development datasets with seeds 0–2, complete and missing tables,
and random/source splits. `comparison.csv` and `report.md` compare the 18-block
model with the matched control and retained starting checkpoint. They also record
inference times for the two freshly evaluated models. `training_time.jsonl`
records successful training-invocation wall time on one GPU, including data
generation overhead; it is not a GPU-kernel-only timer and excludes failed attempts.

This is an equal-step pilot, not an equal-GPU-time comparison. Additional depth
must earn its additional compute cost. The synthetic validation curve and real
development results inform the next decision; no model is automatically promoted,
published, or trained longer. Confirm promising effects on untouched real datasets
and additional pretraining seeds before claiming general improvement. A weak
1,000-step result cannot rule out benefits from longer training.

Short verification: `python scripts/regression_large_experiment.py --smoke --out
results/prior_only_smoke_large`. This uses two steps per arm and diabetes only,
including checkpoint loading, training, inference and comparison generation.
