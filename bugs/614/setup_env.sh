#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install -U pip setuptools wheel
python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch
python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torchvision
python -m pip install --no-cache-dir pyyaml huggingface_hub safetensors 'numpy<2.0'
python -m pip install --no-cache-dir -e "${ROOT_DIR}/codebase"
