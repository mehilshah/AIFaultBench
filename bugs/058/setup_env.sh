#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-}"

if [[ -z "${PYTHON_BIN}" ]]; then
  if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="python3.11"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
    PYTHON_VERSION="$("${PYTHON_BIN}" -c 'import sys; print("{}.{}".format(*sys.version_info[:2]))')"
    case "${PYTHON_VERSION}" in
      3.10|3.11) ;;
      *)
        echo "Python 3.10 or 3.11 is required; found ${PYTHON_VERSION}." >&2
        exit 1
        ;;
    esac
  else
    echo "No supported Python interpreter found." >&2
    exit 1
  fi
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "${ROOT_DIR}/requirements.txt"
