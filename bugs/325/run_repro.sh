#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${ROOT}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Virtual environment not found. Run setup_env.sh first." >&2
  exit 1
fi

export JAX_PLATFORM_NAME=cpu
export PYTHONWARNINGS=always

"${VENV_PYTHON}" "${ROOT}/repro.py" >"${ROOT}/repro_stdout.log" 2>"${ROOT}/repro_stderr.log"
status=$?

cat "${ROOT}/repro_stdout.log"
cat "${ROOT}/repro_stderr.log" >&2

exit "${status}"
