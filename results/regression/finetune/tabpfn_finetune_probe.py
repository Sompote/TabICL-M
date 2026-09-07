"""TabPFN-3 fine-tuned on the same context rows and splits, for a fair test-time-training comparison."""
import importlib.util, sys, time, warnings, json
import numpy as np
warnings.filterwarnings("ignore")
spec = importlib.util.spec_from_file_location("abl", "/workspace/TabICL-M/scripts/ablation_missingness.py"); abl = importlib.util.module_from_spec(spec); spec.loader.exec_module(abl)
from tabpfn import TabPFNRegressor
from tabpfn.constants import ModelVersion
from tabpfn.finetuning import FinetunedTabPFNRegressor
from huggingface_hub import hf_hub_download
ZS_PATH = hf_hub_download("Prior-Labs/tabpfn_3", "tabpfn-v3-regressor-v3_default.ckpt")
v3 = [m for m in ModelVersion if "3" in m.name and "2" not in m.name][0]; print("model version:", v3, flush=True)
rows = []
for name in ["openml:189", "openml:507"]:
    data = abl.load_dataset(name, None, None, 3000, np.random.default_rng(0)); X, y = data["X"], data["y"]
    for seed in [0, 1, 2]:
        tr, te = abl._split(len(y), 0.3, np.random.default_rng(seed), y, "regression")
        zs = TabPFNRegressor(model_path=ZS_PATH, device="cuda", random_state=seed).fit(X[tr], y[tr])
        out = dict(dataset=name, seed=seed, zeroshot=float(np.sqrt(np.mean((zs.predict(X[te]) - y[te]) ** 2))))
        for tag, kw in {"default_e30_lr1e-5": dict(epochs=30, learning_rate=1e-5),
                        "e100_lr5e-5": dict(epochs=100, learning_rate=5e-5, early_stopping_patience=25)}.items():
            t = time.time()
            try:
                ft = FinetunedTabPFNRegressor(model_version=v3, device="cuda", random_state=seed, extra_regressor_kwargs={"model_path": ZS_PATH}, **kw).fit(X[tr], y[tr])
                out[tag] = float(np.sqrt(np.mean((ft.predict(X[te]) - y[te]) ** 2)))
            except Exception as e:
                out[tag] = None; out["err_" + tag] = f"{type(e).__name__}: {str(e)[:120]}"
            out["t_" + tag] = round(time.time() - t, 1)
        print(json.dumps(out), flush=True); rows.append(out)
json.dump(rows, open(sys.argv[1], "w"), indent=1)
