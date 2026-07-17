#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install -U pip setuptools wheel
"${VENV_DIR}/bin/python" -m pip install -r "${ROOT_DIR}/requirements.txt"
