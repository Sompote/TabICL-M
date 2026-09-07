"""Test-time fine-tuning of the source-aware regressor on the context rows, on the runner's exact splits."""
import importlib.util, sys, time, warnings, json
import numpy as np, torch
warnings.filterwarnings("ignore")
spec = importlib.util.spec_from_file_location("abl", "/workspace/TabICL-M/scripts/ablation_missingness.py")
abl = importlib.util.module_from_spec(spec); spec.loader.exec_module(abl)
from tabicl import TabICLRegressor, FinetunedTabICLRegressor
CK = "/workspace/TabICL-M/checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt"
rows = []
for name in ["openml:189", "openml:507", "openml:42225"]:
    data = abl.load_dataset(name, None, None, 3000, np.random.default_rng(0))
    X, y = data["X"], data["y"]
    for seed in [0, 1, 2]:
        tr, te = abl._split(len(y), 0.3, np.random.default_rng(seed), y, "regression")
        t = time.time(); zs = TabICLRegressor(model_path=CK, device="cuda", random_state=seed).fit(X[tr], y[tr])
        r_zs = float(np.sqrt(np.mean((zs.predict(X[te]) - y[te]) ** 2))); t_zs = time.time() - t
        out = dict(dataset=name, seed=seed, n_train=len(tr), zeroshot=r_zs, t_zeroshot=round(t_zs, 1))
        for lr in [1e-5, 3e-5]:
            t = time.time()
            ft = FinetunedTabICLRegressor(model_path=CK, epochs=30, learning_rate=lr, patience=8, n_estimators_inference=8,
                                          device="cuda", random_state=seed, verbose=False).fit(X[tr], y[tr])
            r_ft = float(np.sqrt(np.mean((ft.predict(X[te]) - y[te]) ** 2)))
            out[f"finetune_lr{lr:g}"] = r_ft; out[f"t_lr{lr:g}"] = round(time.time() - t, 1)
        print(json.dumps(out), flush=True); rows.append(out)
json.dump(rows, open(sys.argv[1], "w"), indent=1)
