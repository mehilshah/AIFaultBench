#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Missing ${PYTHON_BIN} on PATH" >&2
  exit 1
fi

"${PYTHON_BIN}" -m venv "${VENV_DIR}"
# shellcheck disable=SC1090
. "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "${ROOT}/requirements.txt"
