#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if [ ! -d "${VENV_DIR}" ]; then
    python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
. "${VENV_DIR}/bin/activate"
python -m pip install --disable-pip-version-check --upgrade pip setuptools wheel
python -m pip install --disable-pip-version-check -r "${ROOT}/requirements.txt"
