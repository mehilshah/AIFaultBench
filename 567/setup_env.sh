#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install \
  --index-url https://download.pytorch.org/whl/cu121 \
  torch==2.5.1+cu121
python -m pip install scipy
python -m pip install \
  --no-index \
  --find-links https://data.pyg.org/whl/torch-2.5.1+cu121.html \
  -r "${ROOT}/requirements.txt"
python -m pip install -e "${ROOT}/codebase"
