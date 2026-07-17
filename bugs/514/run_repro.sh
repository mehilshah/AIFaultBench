#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -x "${ROOT_DIR}/.venv/bin/python" ]]; then
  echo "Missing .venv. Run ./setup_env.sh first." >&2
  exit 1
fi

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
exec "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py"
