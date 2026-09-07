#!/bin/bash
# 1) weight soup of the 10k and 20k source-aware regressors; 2) sample-efficiency curve ours vs TabPFN-3.
cd /workspace/TabICL-M; export HF_HOME=/workspace/.hf_home PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
S=/tmp/claude-0/-workspace-TabICL-M/53d1cc77-4eb2-48ce-a6a2-d3f11554faee/scratchpad/reg_probe
log() { echo "=== $* $(date -u)"; }
log "soup build"
/venv/main/bin/python - <<'PY'
import torch
a = torch.load("checkpoints/tabicl-m-sa/reg/step-10000.ckpt", map_location="cpu", weights_only=True)
b = torch.load("checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt", map_location="cpu", weights_only=True)
assert a["state_dict"].keys() == b["state_dict"].keys()
sd = {k: (a["state_dict"][k].float() + b["state_dict"][k].float()) / 2 if a["state_dict"][k].is_floating_point() else b["state_dict"][k] for k in b["state_dict"]}
torch.save({"config": b["config"], "state_dict": sd}, "/tmp/claude-0/-workspace-TabICL-M/53d1cc77-4eb2-48ce-a6a2-d3f11554faee/scratchpad/reg_probe/soup_reg.ckpt"); print("soup saved")
PY
DS="--datasets diabetes openml:189 openml:507 openml:42225 --max_rows 3000"
log "soup eval"
/venv/main/bin/python scripts/ablation_missingness.py --out $S/soup $DS --mechanisms block --rates 0.5 --seeds 0 1 2 --split random --models tabicl_aware --aware_ckpt_reg $S/soup_reg.ckpt --device cuda > $S/soup.log 2>&1; log "soup eval exit=$?"
log "scaling eval"
for n in 430 860 1720 3000; do
  /venv/main/bin/python scripts/ablation_missingness.py --out $S/scale_ours_$n --datasets openml:189 openml:507 --max_rows $n --mechanisms block --rates 0.5 --seeds 0 1 2 --split random --models tabicl_aware tabicl_impute --aware_ckpt_reg checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt --device cuda > $S/scale_ours_$n.log 2>&1
  /venv/tabpfn25/bin/python scripts/ablation_missingness.py --out $S/scale_tabpfn_$n --datasets openml:189 openml:507 --max_rows $n --mechanisms block --rates 0.5 --seeds 0 1 2 --split random --models tabpfn3 tabpfn25 --device cuda > $S/scale_tabpfn_$n.log 2>&1
  log "scale n=$n done"
done
log "done"
