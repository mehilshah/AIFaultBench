#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${ROOT}/.venv/bin/python"
PYTHON_BIN="${VENV_PY}"
if [ ! -x "${PYTHON_BIN}" ]; then
  PYTHON_BIN="python3"
fi

gpu_count=0
if command -v nvidia-smi >/dev/null 2>&1; then
  gpu_count="$(nvidia-smi -L | awk '/^GPU / {count++} END {print count+0}')"
fi
echo "Visible CUDA devices: ${gpu_count}"
if [ "${gpu_count}" -lt 2 ]; then
  echo "BLOCKED: the reported bug requires multiple GPUs, but this machine only exposes ${gpu_count}."
  exit 3
fi

cd "${ROOT}"
PYTHONPATH="${ROOT}/codebase/src:${PYTHONPATH:-}" "${PYTHON_BIN}" "${ROOT}/repro.py"
