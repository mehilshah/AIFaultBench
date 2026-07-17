#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  "${ROOT_DIR}/setup_env.sh"
fi

export PYTHONPATH="${ROOT_DIR}/codebase"

set +e
"${VENV_PYTHON}" "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
status=$?
set -e

exit "${status}"
