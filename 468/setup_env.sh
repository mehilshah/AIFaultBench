#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip >/dev/null
"${VENV_DIR}/bin/pip" install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu -r "${ROOT_DIR}/requirements.txt"

export PYTHONPATH="${ROOT_DIR}/codebase:${PYTHONPATH:-}"
export PYTHONUNBUFFERED=1
export PYTHONNOUSERSITE=1
export DS_SKIP_CUDA_CHECK=1
export PATH="${VENV_DIR}/bin:${PATH}"
