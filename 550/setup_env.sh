#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu \
  "torch==2.7.1+cpu" \
  "numpy==2.5.1" \
  "cloudpickle==3.1.2" \
  "pyvers==0.2.3" \
  "packaging==26.2"
python -m pip install --no-deps "tensordict==0.10.0"
