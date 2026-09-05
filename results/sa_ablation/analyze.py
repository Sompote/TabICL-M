"""Per-part ablation: each variant trained 3000 steps on the source-aware prior, evaluated on
leave-one-source-out and random splits. Writes results/sa_ablation/summary.md."""
import os, glob
import pandas as pd, numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(ROOT))
names = {"openml:1590": "adult", "openml:31": "credit-g", "openml:531": "boston"}
VARIANTS = ["full_3k", "no_group_stats", "no_row_mask", "no_pattern_token", "no_objectives", "arch_off"]
DESC = {"full_3k": "all parts on (3k steps)", "no_group_stats": "without col_group_stats", "no_row_mask": "without row_missing_aware",
        "no_pattern_token": "without pattern_token", "no_objectives": "cell reconstruction, no consistency loss",
        "arch_off": "all parts off, new prior only"}

def load(cfg):
    frames = []
    for base in [f"{REPO}/results/headroom/{cfg}/results.csv", f"{REPO}/results/headroom/tabpfn_{cfg}/results.csv"]:
        if os.path.exists(base):
            frames.append(pd.read_csv(base))
    for v in VARIANTS:
        f = f"{ROOT}/{v}/{cfg}/results.csv"
        if os.path.exists(f):
            d = pd.read_csv(f); d = d[d.model == "tabicl_aware"].copy(); d["model"] = v; frames.append(d)
    f = f"{REPO}/results/sa_eval/{cfg}/results.csv"
    if os.path.exists(f):
        d = pd.read_csv(f); d = d[d.model == "tabicl_aware"].copy(); d["model"] = "full_10k"; frames.append(d)
    df = pd.concat(frames, ignore_index=True); df = df[df.error.isna()].copy()
    for c in ("rmse", "auc"):
        if c not in df: df[c] = np.nan
    df["metric"] = np.where(df.task == "regression", df.rmse, df.auc); df["dataset"] = df.dataset.map(lambda d: names.get(d, d))
    return df.drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")

def gain_table(df, mech):
    """Paired gain of each variant over tabicl_impute, per dataset, at both rates x 5 seeds."""
    models = [m for m in ["full_10k"] + VARIANTS + ["tabicl_aware", "tabpfn"] if m in df.model.unique()]
    lines = ["| dataset | " + " | ".join(f"`{m}`" for m in models) + " |", "|---|" + "---|" * len(models)]
    tot = {m: [] for m in models}
    for ds, sub in df[df.mechanism == mech].groupby("dataset", sort=False):
        reg = sub.task.iloc[0] == "regression"
        p = sub.pivot_table(index=["rate", "seed"], columns="model", values="metric")
        cells = []
        for m in models:
            if m not in p or "tabicl_impute" not in p:
                cells.append("—"); continue
            d = ((p["tabicl_impute"] - p[m]) if reg else (p[m] - p["tabicl_impute"])).dropna()
            tot[m].append((d > 0).mean() if len(d) else np.nan)
            cells.append(f"{d.mean():+.3f} ({int((d > 0).sum())}/{int((d < 0).sum())})")
        lines.append(f"| {ds} ({'RMSE' if reg else 'AUC'}) | " + " | ".join(cells) + " |")
    lines.append("| **win rate, all datasets** | " + " | ".join(f"**{np.nanmean(tot[m]):.2f}**" if tot[m] else "—" for m in models) + " |")
    return "\n".join(lines)

lines = ["# Ablation of the source-aware parts", "",
         "Each variant: classifier, 3000 steps, lr 5e-5, source-aware prior, one switch off. "
         "Cells: mean paired gain over `tabicl_impute` (AUC up / RMSE down) and wins/losses over rates 0.3, 0.5 x 5 seeds. "
         "`full_10k` is the main 10k-step checkpoint; `tabicl_aware` the first stage-4 checkpoint (old prior, value-level parts).", ""]
for v in VARIANTS:
    lines.append(f"- `{v}`: {DESC[v]}")
lines.append("")
for cfg, title in [("loso", "Leave-one-source-out"), ("random_split", "Random split")]:
    if not any(os.path.exists(f"{ROOT}/{v}/{cfg}/results.csv") for v in VARIANTS):
        continue
    df = load(cfg)
    for mech in ["block_shift", "block"]:
        lines += [f"## {title}, {mech}", "", gain_table(df, mech), ""]
open(f"{ROOT}/summary.md", "w").write("\n".join(lines)); print("\n".join(lines))
