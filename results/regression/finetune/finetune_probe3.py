import importlib.util, sys, time, warnings, json
import numpy as np
warnings.filterwarnings("ignore")
spec = importlib.util.spec_from_file_location("abl", "/workspace/TabICL-M/scripts/ablation_missingness.py"); abl = importlib.util.module_from_spec(spec); spec.loader.exec_module(abl)
from tabicl import FinetunedTabICLRegressor
CK = "/workspace/TabICL-M/checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt"
rows = []
for name in ["openml:189", "openml:507"]:
    data = abl.load_dataset(name, None, None, 3000, np.random.default_rng(0)); X, y = data["X"], data["y"]
    for seed in [0, 1, 2]:
        tr, te = abl._split(len(y), 0.3, np.random.default_rng(seed), y, "regression")
        out = dict(dataset=name, seed=seed)
        for tag, kw in {"e1000_lr5e-5_p100": dict(epochs=1000, learning_rate=5e-5, patience=100),
                        "e1000_lr2e-5_p100": dict(epochs=1000, learning_rate=2e-5, patience=100),
                        "e1000_lr5e-5_noES": dict(epochs=1000, learning_rate=5e-5, early_stopping=False)}.items():
            t = time.time()
            ft = FinetunedTabICLRegressor(model_path=CK, n_estimators_inference=8, device="cuda", random_state=seed, verbose=False, **kw).fit(X[tr], y[tr])
            out[tag] = float(np.sqrt(np.mean((ft.predict(X[te]) - y[te]) ** 2))); out["t_" + tag] = round(time.time() - t, 1)
        print(json.dumps(out), flush=True); rows.append(out)
json.dump(rows, open(sys.argv[1], "w"), indent=1)
