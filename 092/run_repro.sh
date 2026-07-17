#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PY}" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

exec "${VENV_PY}" "${ROOT_DIR}/repro.py"
