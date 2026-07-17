#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"

if [[ ! -d "${VENV_DIR}" ]]; then
  bash setup_env.sh
fi

source "${VENV_DIR}/bin/activate"
export PYTHONPATH="$(pwd)/codebase:${PYTHONPATH:-}"

python repro.py
