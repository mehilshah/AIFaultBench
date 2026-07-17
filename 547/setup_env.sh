#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  python3 -m venv "${VENV_DIR}"
  "${PYTHON_BIN}" -m pip install --upgrade pip >/dev/null 2>&1
  "${PYTHON_BIN}" -m pip install -r "${ROOT_DIR}/requirements.txt" >/dev/null 2>&1
fi

printf '%s\n' "${PYTHON_BIN}"
