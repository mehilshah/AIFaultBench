#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${PYTHON_BIN}" -m pip install --quiet --upgrade pip
"${PYTHON_BIN}" -m pip install --quiet -r "${ROOT_DIR}/requirements.txt"
"${PYTHON_BIN}" -m pip install --quiet -e "${ROOT_DIR}/codebase" --no-deps
