"""20-dataset benchmark: source-aware TabICL-M (and its test-time variants) vs TabPFN 2.5 / 3, base model, CatBoost.
Writes results/broad/summary.md with mean ranks, paired win/loss and per-dataset tables."""
import os
import pandas as pd, numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__))
ORDER = ["tabicl_impute", "tabicl_aware", "tabicl_aware_ewt", "tabicl_aware_si", "tabpfn25", "tabpfn3", "catboost"]
def load(cfg):
    fs = [f"{ROOT}/{cfg}/results.csv", f"{ROOT}/tabpfn_{cfg}/results.csv"]
    df = pd.concat([pd.read_csv(f) for f in fs if os.path.exists(f)], ignore_index=True); df = df[df.error.isna()].copy()
    for c in ("rmse", "auc"):
        if c not in df: df[c] = np.nan
    df["metric"] = np.where(df.task == "regression", df.rmse, df.auc)
    return df.drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")
lines = ["# 20-dataset benchmark", "", "Block and block_shift missingness at rates 0.3 / 0.5, 5 seeds. Rank 1 = best per condition; "
         "`tabicl_aware` = source-aware TabICL-M, `_ewt` = transductive column embedding, `_si` = self-imputation.", ""]
for cfg, title in [("loso", "Leave-one-source-out"), ("random_split", "Random split")]:
    if not os.path.exists(f"{ROOT}/{cfg}/results.csv"): continue
    df = load(cfg); models = [m for m in ORDER if m in df.model.unique()]
    for mech_sel, name in [(["block", "block_shift"], "all"), (["block_shift"], "block_shift only"), (["block"], "block only")]:
        p = df[df.mechanism.isin(mech_sel)].pivot_table(index=["dataset", "mechanism", "rate", "seed"], columns="model", values="metric")[models].dropna()
        reg = p.index.get_level_values("dataset").isin(df[df.task == "regression"].dataset.unique())
        ranks = p.mul(np.where(reg, -1.0, 1.0), axis=0).rank(axis=1, ascending=False)
        lines += [f"## {title}, {name}: {len(p)} conditions", "", "| model | mean rank | times first |", "|---|---|---|"]
        for m in ranks.mean().sort_values().index:
            lines.append(f"| `{m}` | {ranks[m].mean():.2f} | {int((ranks[m] == 1).sum())} |")
        lines.append("")
        for a in ["tabicl_aware", "tabicl_aware_ewt", "tabicl_aware_si"]:
            if a not in p: continue
            row = []
            for b in ["tabpfn25", "tabpfn3", "tabicl_impute"]:
                if b not in p: continue
                d = pd.Series(np.where(reg, p[b] - p[a], p[a] - p[b]), index=p.index)
                per = d.groupby(level="dataset").mean()
                row.append(f"vs `{b}`: {int((d > 0).sum())}/{int((d < 0).sum())} ({(d > 0).mean():.0%}), datasets won {int((per > 0).sum())}/{len(per)}")
            lines.append(f"- `{a}` paired: " + "; ".join(row))
        lines.append("")
    lines += [f"## {title}: per-dataset means, block_shift@0.5", ""]
    t = df[(df.mechanism == "block_shift") & (df.rate == 0.5)].pivot_table(index="dataset", columns="model", values="metric")[models]
    lines += ["| dataset | " + " | ".join(f"`{m}`" for m in models) + " |", "|---|" + "---|" * len(models)]
    for ds, r in t.iterrows():
        isreg = ds in df[df.task == "regression"].dataset.unique(); best = r.idxmin() if isreg else r.idxmax()
        lines.append(f"| {ds}{' (RMSE)' if isreg else ''} | " + " | ".join(("**%.3f**" if m == best else "%.3f") % r[m] if r[m] == r[m] else "—" for m in models) + " |")
    lines.append("")
open(f"{ROOT}/summary.md", "w").write("\n".join(lines)); print("\n".join(lines[:40]))
