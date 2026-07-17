#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Virtualenv not found. Run ./setup_env.sh first." >&2
  exit 2
fi

set +e
"${PYTHON_BIN}" "${ROOT_DIR}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
status=$?
set -e

exit "${status}"
