#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

python3 -m venv --clear "${VENV_DIR}"
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "${ROOT_DIR}/requirements.txt"

# Install a CPU-only torch build. Keep torchvision absent to reproduce the bug.
python -m pip install --index-url https://download.pytorch.org/whl/cpu --no-cache-dir "torch==2.8.0"

echo "Environment ready at ${VENV_DIR}"
