#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install -U pip setuptools wheel
"${VENV_DIR}/bin/pip" install -r requirements.txt
