#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install -U pip setuptools wheel
python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r "${ROOT_DIR}/requirements.txt"
python -m pip install --no-deps -e "${ROOT_DIR}/codebase"
