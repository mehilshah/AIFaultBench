#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.repro-venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install -r "${ROOT}/requirements.txt"
cd "${ROOT}/codebase"
pip install -e . --no-deps
