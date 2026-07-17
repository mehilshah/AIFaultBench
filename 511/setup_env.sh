#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "python3.11 is required to set up the repro environment." >&2
  exit 1
fi

"${PYTHON_BIN}" -m venv "${ROOT}/.venv"
"${ROOT}/.venv/bin/pip" install --upgrade pip
"${ROOT}/.venv/bin/pip" install -r "${ROOT}/requirements.txt"
"${ROOT}/.venv/bin/pip" install -e "${ROOT}/codebase"
