#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Missing .venv/bin/python. Run ./setup_env.sh first." >&2
  exit 1
fi

"${VENV_PYTHON}" "${ROOT_DIR}/repro.py"
