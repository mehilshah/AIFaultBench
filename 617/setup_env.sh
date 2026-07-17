#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3.9}"

if [[ ! -x "$(command -v "${PYTHON_BIN}" || true)" ]]; then
  echo "python interpreter not found: ${PYTHON_BIN}" >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install --upgrade --force-reinstall -r "${ROOT_DIR}/requirements.txt" -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install --upgrade -e "${ROOT_DIR}/codebase"
