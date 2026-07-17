#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
# `accelerate` 0.17 imports `pkg_resources`, which is not present in newer setuptools releases.
python -m pip install --upgrade "setuptools<81"
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.3.1
python -m pip install -r "${ROOT_DIR}/requirements.txt"
