#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${ROOT_DIR}/setup_env.sh"

set +e
export PYTHONPATH="${ROOT_DIR}/codebase:${PYTHONPATH:-}"
PYTHONWARNINGS=error::DeprecationWarning "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" \
  >"${ROOT_DIR}/repro_stdout.log" \
  2>"${ROOT_DIR}/repro_stderr.log"
status=$?
set -e

printf 'exit_code=%s\n' "${status}" >> "${ROOT_DIR}/repro_stdout.log"
exit "${status}"
