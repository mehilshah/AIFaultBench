#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
TEMP_VENV_DIR="${ROOT_DIR}/.venv_test"

if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  source "${VENV_DIR}/bin/activate"
elif [[ -f "${TEMP_VENV_DIR}/bin/activate" ]]; then
  source "${TEMP_VENV_DIR}/bin/activate"
else
  bash "${ROOT_DIR}/setup_env.sh"
  source "${VENV_DIR}/bin/activate"
fi

export PYTHONPATH="${ROOT_DIR}/codebase/src${PYTHONPATH:+:${PYTHONPATH}}"

python "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
