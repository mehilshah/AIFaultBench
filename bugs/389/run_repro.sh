#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  "${ROOT}/setup_env.sh"
fi

export JAX_PLATFORMS=cpu
exec "${VENV_DIR}/bin/python" "${ROOT}/repro.py"
