"""Regression ablation: which source-aware part helps or hurts the regressor, against the released
TabICLv2 regressor and TabPFN-3 on the same splits. Writes results/sa_ablation_reg/summary.md."""
import os, glob
import pandas as pd, numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(ROOT))
names = {"openml:189": "kin8nm", "openml:507": "space_ga", "openml:42225": "diamonds", "openml:44970": "44970", "openml:531": "boston", "openml:560": "bodyfat"}
VARIANTS = ["full_3k", "no_group_stats", "no_row_mask", "no_pattern_token", "no_objectives", "arch_off"]
DESC = {"full_3k": "all parts on", "no_group_stats": "without col_group_stats", "no_row_mask": "without row_missing_aware",
        "no_pattern_token": "without pattern_token", "no_objectives": "cell reconstruction, no consistency loss", "arch_off": "all parts off, new prior only"}
def load(cfg):
    frames = []
    for base in [f"{REPO}/results/broad/{cfg}/results.csv", f"{REPO}/results/broad/tabpfn_{cfg}/results.csv"]:
        if os.path.exists(base):
            d = pd.read_csv(base); d = d[d.task == "regression"]; d["model"] = d.model.replace({"tabicl_aware": "full_20k"}); frames.append(d)
    for v in VARIANTS:
        f = f"{ROOT}/{v}/{cfg}/results.csv"
        if os.path.exists(f):
            d = pd.read_csv(f); d = d[d.model == "tabicl_aware"].copy(); d["model"] = v; frames.append(d)
    df = pd.concat(frames, ignore_index=True); df = df[df.error.isna()].copy(); df["dataset"] = df.dataset.map(lambda x: names.get(x, x))
    return df.drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")
def block(df, mechs, title):
    p = df[df.mechanism.isin(mechs)].pivot_table(index=["dataset", "mechanism", "rate", "seed"], columns="model", values="rmse")
    models = [m for m in VARIANTS + ["full_20k", "tabicl_impute", "tabpfn25", "tabpfn3", "catboost"] if m in p and p[m].notna().mean() > 0.95]
    p = p[models].dropna(); ranks = p.rank(axis=1)
    L = [f"## {title}: {len(p)} conditions", "", "| variant | mean rank | vs released TabICLv2 (wins/losses, mean % RMSE) | vs TabPFN-3 (wins/losses, mean % RMSE) |", "|---|---|---|---|"]
    for m in ranks.mean().sort_values().index:
        cells = []
        for ref in ["tabicl_impute", "tabpfn3"]:
            if ref in p and m != ref:
                d = p[ref] - p[m]; rel = 100 * d / p[ref]
                cells.append(f"{int((d > 0).sum())}/{int((d < 0).sum())}, {rel.mean():+.2f} %")
            else: cells.append("—")
        L.append(f"| `{m}` | {ranks[m].mean():.2f} | {cells[0]} | {cells[1]} |")
    return L + [""]
lines = ["# Regression ablation of the source-aware parts", "",
         "Regressor, 3000 steps each from the released TabICLv2 regressor on the source-aware prior, one switch off at a time; "
         "seven regression datasets, block and block_shift at 0.3 / 0.5, 5 seeds. Lower RMSE is better; positive % = the variant is better than the reference. "
         "`full_20k` is the main 20k-step checkpoint (10k + stage 4b).", ""] + [f"- `{v}`: {DESC[v]}" for v in VARIANTS] + [""]
for cfg, title in [("loso", "Leave-one-source-out"), ("random_split", "Random split")]:
    if not any(os.path.exists(f"{ROOT}/{v}/{cfg}/results.csv") for v in VARIANTS): continue
    df = load(cfg)
    lines += block(df, ["none"], f"{title}, complete data (base strength)")
    lines += block(df, ["block_shift"], f"{title}, held-out source with offset") if cfg == "loso" else []
    lines += block(df, ["block"], f"{title}, block without offset")
    lines += block(df, ["block", "block_shift"], f"{title}, all incomplete conditions")
open(f"{ROOT}/summary.md", "w").write("\n".join(lines)); print("\n".join(lines[:40]))
