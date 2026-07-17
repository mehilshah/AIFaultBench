#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

# Install the runtime needed by the local codebase and the repro script.
"${VENV_DIR}/bin/python" -m pip install -U pip setuptools wheel
"${VENV_DIR}/bin/python" -m pip install -r "${ROOT}/requirements.txt"
"${VENV_DIR}/bin/python" -m pip install -e "${ROOT}/codebase" --no-deps
