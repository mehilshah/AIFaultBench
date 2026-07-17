#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --disable-pip-version-check --upgrade pip setuptools wheel
"${VENV_DIR}/bin/python" -m pip install --disable-pip-version-check -r "${ROOT_DIR}/requirements.txt"
