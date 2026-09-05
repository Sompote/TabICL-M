"""Compare the source-aware TabICL-M (tabicl_m_sa) with every baseline on the headroom
configurations and the standard ablation. Writes results/sa_eval/summary_vs_baselines.md."""
import os, sys
import pandas as pd, numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ROOT))
names = {"openml:1590": "adult", "openml:31": "credit-g", "openml:531": "boston"}
ORDER = ["tabicl_impute", "tabicl_indicator", "tabicl_patternnorm", "tabicl_iterimpute", "tabicl_knnimpute",
         "tabicl_aware_zero", "tabicl_aware", "tabicl_m_sa", "tabpfn", "xgboost", "catboost"]

def _read(path, rename=None):
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df = df[df.error.isna()].copy()
    if rename:
        df["model"] = df.model.replace(rename)
    return df

def load(cfg):
    parts = [
        _read(f"{REPO}/results/headroom/{cfg}/results.csv"),
        _read(f"{REPO}/results/headroom/tabpfn_{cfg}/results.csv"),
        _read(f"{REPO}/results/headroom/patternnorm_{cfg}/results.csv"),
        _read(f"{ROOT}/{cfg}/results.csv", rename={"tabicl_aware": "tabicl_m_sa"}),
    ]
    parts = [p for p in parts if p is not None]
    df = pd.concat(parts, ignore_index=True)
    for c in ("rmse", "auc", "coverage80", "width80"):
        if c not in df:
            df[c] = np.nan
    df["metric"] = np.where(df.task == "regression", df.rmse, df.auc)
    df["dataset"] = df.dataset.map(lambda d: names.get(d, d))
    # the sa_eval run re-fits the base models too; keep one copy per (dataset, mech, rate, seed, model)
    df = df.drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")
    return df

def md_table(df, rows_spec, cols):
    cols = [c for c in cols if c in df.model.unique()]
    lines = ["| dataset | condition | " + " | ".join(f"`{c}`" for c in cols) + " |", "|---|---|" + "---|" * len(cols)]
    for ds, sub in df.groupby("dataset", sort=False):
        reg = sub.task.iloc[0] == "regression"
        for mech, rate in rows_spec:
            m = sub[(sub.mechanism == mech) & (sub.rate == rate)].groupby("model").metric.mean()
            if m.empty:
                continue
            fmt = (lambda v: f"{v:.2f}") if reg else (lambda v: f"{v:.3f}")
            best = (m.idxmin() if reg else m.idxmax()) if len(m) else None
            cells = []
            for c in cols:
                v = m.get(c, np.nan)
                cells.append(("**" + fmt(v) + "**") if c == best else (fmt(v) if v == v else "—"))
            lines.append(f"| {ds} ({'RMSE' if reg else 'AUC'}) | {mech if mech != 'none' else 'complete'}@{rate} | " + " | ".join(cells) + " |")
    return "\n".join(lines)

def paired(df, a, b, mechs=None):
    out = []
    for ds, sub in df[df.mechanism != "none"].groupby("dataset", sort=False):
        if mechs:
            sub = sub[sub.mechanism.isin(mechs)]
        reg = sub.task.iloc[0] == "regression"
        p = sub.pivot_table(index=["mechanism", "rate", "seed"], columns="model", values="metric")
        if a not in p or b not in p:
            continue
        d = ((p[b] - p[a]) if reg else (p[a] - p[b])).dropna()
        if len(d) == 0:
            continue
        out.append(f"| {ds} | {'RMSE' if reg else 'AUC'} | {int((d > 0).sum())} / {int((d < 0).sum())} | {d.mean():+.4f} |")
    return "| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |\n|---|---|---|---|\n" + "\n".join(out)

lines = ["# Source-aware TabICL-M against the baselines", "",
         "`tabicl_m_sa` = source-aware stage-4 checkpoint (`checkpoints/tabicl-m-sa/*/step-10000.ckpt`); "
         "`tabicl_aware` = first stage-4 checkpoint (3000 steps, value-level parts only); "
         "`tabicl_impute` = released TabICLv2 with mean imputation; `tabpfn` = TabPFN v2. "
         "Mean over 5 seeds; bold = best in row.", ""]
for cfg, title in [("loso", "Leave-one-source-out (held-out synthetic source)"), ("random_split", "Random split")]:
    if not os.path.exists(f"{ROOT}/{cfg}/results.csv"):
        continue
    df = load(cfg)
    lines += [f"## {title}", "", md_table(df, [("none", 0.0), ("block", 0.5), ("block_shift", 0.5)], ORDER), ""]
    for b in ["tabicl_impute", "tabicl_aware", "tabpfn", "tabicl_patternnorm"]:
        lines += [f"### {cfg}: `tabicl_m_sa` vs `{b}`, paired over block + block_shift, rates 0.3/0.5, 5 seeds", "", paired(df, "tabicl_m_sa", b), ""]
    lines += [f"### {cfg}: `tabicl_m_sa` vs `tabicl_impute`, block_shift only", "", paired(df, "tabicl_m_sa", "tabicl_impute", ["block_shift"]), ""]
    cov = df[(df.task == "regression") & (df.mechanism == "block_shift") & (df.rate == 0.5)].groupby(["dataset", "model"])[["coverage80", "width80"]].mean().round(3)
    cov = cov[cov.coverage80.notna()]
    if len(cov):
        lines += [f"### {cfg}: 80 % interval coverage / width, regression, block_shift@0.5", "", cov.to_markdown(), ""]
std = f"{ROOT}/standard/results.csv"
if os.path.exists(std):
    df = _read(std, rename={"tabicl_aware": "tabicl_m_sa"})
    old = _read(f"{REPO}/results/ablation_m/builtin/results.csv"); old2 = _read(f"{REPO}/results/ablation_m/openml/results.csv")
    df = pd.concat([df] + [x for x in (old, old2) if x is not None], ignore_index=True)
    for c in ("rmse", "auc"):
        if c not in df: df[c] = np.nan
    df["metric"] = np.where(df.task == "regression", df.rmse, df.auc); df["dataset"] = df.dataset.map(lambda d: names.get(d, d))
    df = df.drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="first")
    lines += ["## Standard ablation (random split, mcar / mar / mnar / block at 0.5)", "",
              md_table(df, [("none", 0.0), ("mcar", 0.5), ("mar", 0.5), ("mnar", 0.5), ("block", 0.5)], ["tabicl_impute", "tabicl_aware", "tabicl_m_sa", "xgboost", "catboost"]), "",
              "### `tabicl_m_sa` vs `tabicl_impute`, paired over all mechanisms and rates", "", paired(df, "tabicl_m_sa", "tabicl_impute"), ""]
open(f"{ROOT}/summary_vs_baselines.md", "w").write("\n".join(lines))
print("\n".join(lines))
