#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$("${ROOT_DIR}/setup_env.sh")"

set +e
"${PYTHON_BIN}" "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
STATUS=$?
set -e

printf 'repro exit status: %s\n' "${STATUS}"
exit "${STATUS}"
