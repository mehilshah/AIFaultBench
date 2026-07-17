#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
TORCH_INDEX_URL="${TORCH_INDEX_URL:-https://download.pytorch.org/whl/cpu}"
TORCH_VERSION="${TORCH_VERSION:-2.3.1}"
MARKER_FILE="${VENV_DIR}/.repro_deps_installed"

if [ ! -d "${VENV_DIR}" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

if [ ! -f "${MARKER_FILE}" ]; then
  python -m pip install --quiet --upgrade pip setuptools wheel
  python -m pip install --quiet --index-url "${TORCH_INDEX_URL}" "torch==${TORCH_VERSION}"
  python -m pip install --quiet -r "${ROOT_DIR}/requirements.txt"
  touch "${MARKER_FILE}"
fi
