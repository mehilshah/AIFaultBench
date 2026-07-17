#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv_test"

if [ ! -e "${ROOT_DIR}/codebase" ]; then
    bash "${ROOT_DIR}/setup_codebase.sh"
fi

python3 -m venv "${VENV_DIR}"
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "${ROOT_DIR}/requirements.txt"

# Install the checked-out DeepSpeed source in editable mode without building ops.
cd "${ROOT_DIR}/codebase"
DS_BUILD_OPS=0 python -m pip install -e . --no-deps
