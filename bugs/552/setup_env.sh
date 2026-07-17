#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-}"

if [[ -z "${PYTHON_BIN}" ]]; then
  if command -v python3.10 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3.10)"
  elif [[ -x python3.10 ]]; then
    PYTHON_BIN="python3.10"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "No usable Python interpreter found" >&2
    exit 1
  fi
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r "${ROOT_DIR}/requirements.txt"
