"""Large-table regression (up to 20k rows): plain context vs neighbour-based context vs TabPFN-3.

Reads results/regression/large_n_{20k,smooth,tabpfn}/results.csv and writes large_n_summary.md.
"""
import glob
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
frames = []
for d in sorted(glob.glob(f"{ROOT}/large_n_*")):
    f = f"{d}/results.csv"
    if not os.path.exists(f):
        continue
    tag = os.path.basename(d)[len("large_n_"):]
    df = pd.read_csv(f)
    df = df[df.error.isna()].copy()
    if tag != "tabpfn":
        df["model"] = df.model + "_" + tag
    frames.append(df)
lines = ["# Large tables: neighbour-based context", "",
         "kin8nm (8 192 rows), space_ga (3 107) and diamonds (subsampled to 20 000), random 70/30 split, complete and "
         "block_shift at rate 0.3, 3 seeds. `_knn` = KNNContextRegressor (4 000 nearest training rows per group of test rows, "
         "plain estimator below 4 500 training rows); `_20k` = source-aware regressor (20k steps), `_smooth` = continued on the "
         "smooth-target prior with the point loss. RMSE, lower is better.", ""]
if not frames:
    lines.append("No results yet.")
else:
    df = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")
    models = sorted(df.model.unique(), key=lambda m: (m.startswith("tabpfn"), m))
    piv = df.pivot_table(index=["dataset", "mechanism", "seed"], columns="model", values="rmse")
    mean = piv.groupby(level=["dataset", "mechanism"]).mean()
    ntr = df.groupby("dataset").n_train.max()
    lines += ["| dataset | train rows | mechanism | " + " | ".join(f"`{m}`" for m in models) + " |", "|---|---|---|" + "---|" * len(models)]
    for (ds, mech), r in mean.iterrows():
        best = r[models].idxmin()
        cells = [(f"**{r[m]:.4g}**" if m == best else f"{r[m]:.4g}") if pd.notna(r.get(m)) else "—" for m in models]
        lines.append(f"| {ds} | {int(ntr[ds])} | {mech} | " + " | ".join(cells) + " |")
    lines.append("")
    if "tabpfn3" in piv:
        lines += ["## Paired against TabPFN-3", "", "| model | wins/losses | mean RMSE difference (%) | datasets won |", "|---|---|---|---|"]
        for m in models:
            if m == "tabpfn3":
                continue
            q = piv[[m, "tabpfn3"]].dropna()
            if q.empty:
                continue
            d = q["tabpfn3"] - q[m]
            rel = 100 * d / q["tabpfn3"]
            per = d.groupby(level="dataset").mean()
            lines.append(f"| `{m}` | {int((d > 0).sum())}/{int((d < 0).sum())} | {rel.mean():+.2f} | {int((per > 0).sum())}/{len(per)} |")
        lines.append("")
    for tag in ("20k", "smooth"):
        a, b = f"tabicl_aware_{tag}", f"tabicl_aware_knn_{tag}"
        if a in piv and b in piv:
            q = piv[[a, b]].dropna()
            d = 100 * (q[a] - q[b]) / q[a]
            lines.append(f"Neighbour context vs plain context ({tag} regressor): {int((d > 0).sum())} wins / {int((d < 0).sum())} losses, "
                         f"mean RMSE change {-d.mean():+.2f} % (negative = knn better).")
    t = df.groupby("model").seconds.median()
    lines += ["", "Median seconds per fit+predict: " + ", ".join(f"`{m}` {t[m]:.1f}" for m in models if m in t) + "."]
open(f"{ROOT}/large_n_summary.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
