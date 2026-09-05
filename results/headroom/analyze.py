"""Headroom analysis: oracle (complete) vs base model vs imputers vs TabICL-M, per regime."""
import sys
import pandas as pd, numpy as np

names = {"openml:1590": "adult", "openml:31": "credit-g", "openml:531": "boston"}
cols = ["tabicl_impute", "tabicl_indicator", "tabicl_iterimpute", "tabicl_knnimpute", "tabicl_aware_zero", "tabicl_aware", "xgboost", "catboost"]

def load(cfg):
    df = pd.read_csv(f"results/headroom/{cfg}/results.csv")
    df = df[df.error.isna()]
    df["metric"] = np.where(df.task == "regression", df.rmse, df.auc)
    df["dataset"] = df.dataset.map(lambda d: names.get(d, d))
    return df

def table(df, rate):
    rows = []
    for ds, sub in df.groupby("dataset", sort=False):
        reg = sub.task.iloc[0] == "regression"
        oracle = sub[sub.mechanism == "none"].groupby("model").metric.mean()["tabicl_impute"]
        for mech in ["block", "block_shift"]:
            m = sub[(sub.mechanism == mech) & (sub.rate == rate)].groupby("model").metric.mean()
            if m.empty: continue
            r = {"dataset": ds, "mech": mech, "oracle": oracle}
            r.update({c: m.get(c, np.nan) for c in cols})
            rows.append(r)
    t = pd.DataFrame(rows).set_index(["dataset", "mech"])
    return t

def paired(df, a, b):
    """wins/losses/mean gain of a over b, positive = a better, over (dataset, mech, rate, seed)."""
    out = []
    for ds, sub in df[df.mechanism != "none"].groupby("dataset", sort=False):
        reg = sub.task.iloc[0] == "regression"
        m = sub.pivot_table(index=["mechanism", "rate", "seed"], columns="model", values="metric")
        if a not in m or b not in m: continue
        d = (m[b] - m[a]) if reg else (m[a] - m[b])
        d = d.dropna()
        out.append(dict(dataset=ds, n=len(d), wins=int((d > 0).sum()), losses=int((d < 0).sum()), mean_gain=round(d.mean(), 4)))
    return pd.DataFrame(out)

if __name__ == "__main__":
    for cfg in sys.argv[1:]:
        df = load(cfg)
        print(f"\n######## {cfg}: mean metric over seeds at rate 0.5 (AUC up / RMSE down); 'oracle' = complete data, random split")
        print(table(df, 0.5).round(3).to_string())
        print(f"\n-- {cfg}: tabicl_aware vs tabicl_impute, paired (block + block_shift, both rates, 5 seeds)")
        print(paired(df, "tabicl_aware", "tabicl_impute").to_string(index=False))
        print(f"\n-- {cfg}: best classical imputer (iterimpute) vs tabicl_impute")
        print(paired(df, "tabicl_iterimpute", "tabicl_impute").to_string(index=False))
