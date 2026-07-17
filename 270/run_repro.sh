#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  # shellcheck disable=SC1090
  source "${VENV_DIR}/bin/activate"
fi

: > "${ROOT_DIR}/repro_stdout.log"
: > "${ROOT_DIR}/repro_stderr.log"

run_case() {
  local port="$1"
  shift
  CUDA_VISIBLE_DEVICES=0 accelerate launch \
    --config_file "${ROOT_DIR}/ds_zero2.yaml" \
    --num_processes=1 \
    --main_process_port="${port}" \
    "${ROOT_DIR}/repro.py" \
    "$@" \
    > >(tee -a "${ROOT_DIR}/repro_stdout.log") \
    2> >(tee -a "${ROOT_DIR}/repro_stderr.log" >&2)
}

run_case 29513 \
  --batch-size 2 \
  --gradient-accumulation-steps 4 \
  --max-steps 8 \
  --summary-file "${ROOT_DIR}/run_b2_g4.json" \
  --output-dir "${ROOT_DIR}/SFT-bsz2-grad_acc4-zero2"

run_case 29514 \
  --batch-size 8 \
  --gradient-accumulation-steps 1 \
  --max-steps 8 \
  --summary-file "${ROOT_DIR}/run_b8_g1.json" \
  --output-dir "${ROOT_DIR}/SFT-bsz8-grad_acc1-zero2"

ROOT_DIR="${ROOT_DIR}" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["ROOT_DIR"])
a = json.loads((root / "run_b2_g4.json").read_text(encoding="utf-8"))
b = json.loads((root / "run_b8_g1.json").read_text(encoding="utf-8"))

loss_delta = abs(a["train_loss"] - b["train_loss"])
step_deltas = [
    abs(x["loss"] - y["loss"])
    for x, y in zip(a["logs"], b["logs"])
    if "loss" in x and "loss" in y
]
max_step_delta = max(step_deltas) if step_deltas else None

result = {
    "train_loss_a": a["train_loss"],
    "train_loss_b": b["train_loss"],
    "train_loss_delta": loss_delta,
    "max_step_loss_delta": max_step_delta,
    "reproducible_here": loss_delta > 1e-3 or (max_step_delta is not None and max_step_delta > 1e-3),
}
result_path = root / "reproduction.json"
result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
PY
