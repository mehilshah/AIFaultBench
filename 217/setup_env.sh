#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python3.11 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

python -m pip install -U pip setuptools wheel
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.3.1+cpu
python -m pip install -r "${ROOT}/requirements.txt"
python -m pip install -e "${ROOT}/codebase"
