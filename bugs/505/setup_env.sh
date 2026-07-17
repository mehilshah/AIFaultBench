#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
PIP_BIN="${VENV_DIR}/bin/pip"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${PIP_BIN}" install --upgrade pip setuptools wheel
"${PIP_BIN}" install --no-cache-dir \
  --extra-index-url https://download.pytorch.org/whl/cu130 \
  -r "${ROOT_DIR}/requirements.txt"
