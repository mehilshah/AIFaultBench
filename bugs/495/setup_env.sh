#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv_repro"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

if [ ! -x "${VENV_DIR}/bin/python" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/pip" install --upgrade pip wheel
"${VENV_DIR}/bin/pip" install 'setuptools<82'
"${VENV_DIR}/bin/pip" install torch==2.11.0+cu128 --index-url https://download.pytorch.org/whl/cu128
"${VENV_DIR}/bin/pip" install -r "${ROOT_DIR}/requirements.txt"
