#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if command -v uv >/dev/null 2>&1; then
  if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
    uv venv "${VENV_DIR}"
  fi
  uv pip install --python "${VENV_DIR}/bin/python" -r "${ROOT_DIR}/requirements.txt"
else
  if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
    python3 -m venv "${VENV_DIR}"
  fi
  "${VENV_DIR}/bin/python" -m pip install --upgrade pip
  "${VENV_DIR}/bin/python" -m pip install -r "${ROOT_DIR}/requirements.txt"
fi
