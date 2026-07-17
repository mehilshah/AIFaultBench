#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${ROOT_DIR}/.venv/bin/python"
WORLD_SIZE=4

if [[ ! -x "${VENV_PY}" ]]; then
  "${ROOT_DIR}/setup_env.sh"
fi

CUDA_COUNT="$(${VENV_PY} - <<'PY'
import torch
print(torch.cuda.device_count())
PY
)"

if [[ "${CUDA_COUNT}" -ge "${WORLD_SIZE}" ]]; then
  export CUDA_VISIBLE_DEVICES="0,1,2,3"
  PYTHONPATH="${ROOT_DIR}/codebase/src" "${VENV_PY}" -m accelerate.commands.launch \
    --multi_gpu \
    --num_processes "${WORLD_SIZE}" \
    --mixed_precision bf16 \
    "${ROOT_DIR}/repro.py" \
    --world-size "${WORLD_SIZE}" \
    --mixed-precision bf16
else
  echo "BLOCKED: requested ${WORLD_SIZE} GPUs, but only ${CUDA_COUNT} CUDA device(s) are available." >&2
  echo "Running smoke test instead." >&2
  PYTHONPATH="${ROOT_DIR}/codebase/src" "${VENV_PY}" "${ROOT_DIR}/repro.py" \
    --smoke \
    --world-size "${WORLD_SIZE}" \
    --mixed-precision bf16
fi
