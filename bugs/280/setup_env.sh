#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [ ! -d "${VENV_DIR}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1090
. "${VENV_DIR}/bin/activate"

python -m pip install -U pip setuptools wheel
python -m pip install -r "${ROOT_DIR}/requirements.txt"

# Build POT against the active NumPy/SciPy stack without re-resolving
# incompatible build-time dependencies.
python -m pip install --no-build-isolation --no-deps -e "${ROOT_DIR}/codebase"
