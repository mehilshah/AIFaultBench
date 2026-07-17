#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3.10 || command -v python3)}"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"

if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3.10 or python3 is required" >&2
  exit 1
fi

"${PYTHON_BIN}" -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "${ROOT_DIR}/requirements.txt"

echo "Virtualenv ready at ${VENV_DIR}"
