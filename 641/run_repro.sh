#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

PYTHONPATH="${ROOT_DIR}/codebase" "${PYTHON_BIN}" "${ROOT_DIR}/repro.py"
