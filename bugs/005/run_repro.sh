#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  echo "Missing virtual environment at ${VENV_DIR}; run setup_env.sh first." >&2
  exit 1
fi

source "${VENV_DIR}/bin/activate"
python repro.py
