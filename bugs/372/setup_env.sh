#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if command -v python3.11 >/dev/null 2>&1; then
  PYTHON_BIN="python3.11"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "python3.11 is required" >&2
  exit 1
fi

PYTHON_VERSION="$("${PYTHON_BIN}" -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')"
if [[ "${PYTHON_VERSION}" != "3.11" ]]; then
  echo "python3.11 is required, found ${PYTHON_VERSION}" >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "${ROOT}/requirements.txt"
python -m pip install -e "${ROOT}/codebase"
