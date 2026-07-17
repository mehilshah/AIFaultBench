#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_STDOUT="${ROOT_DIR}/repro_stdout.log"
LOG_STDERR="${ROOT_DIR}/repro_stderr.log"

"${ROOT_DIR}/setup_env.sh"

set +e
"${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" >"${LOG_STDOUT}" 2>"${LOG_STDERR}"
status=$?
set -e

echo "exit_code=${status}"
exit "${status}"
