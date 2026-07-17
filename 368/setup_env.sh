#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv_repro"
TORCH_INDEX_URL="https://download.pytorch.org/whl/cu128"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
pip install --index-url "${TORCH_INDEX_URL}" torch==2.9.0 torchvision==0.24.0
pip install -r "${ROOT_DIR}/requirements.txt"
