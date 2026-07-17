#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

bash "${ROOT}/setup_env.sh"

STDOUT_LOG="${ROOT}/repro_stdout.log"
STDERR_LOG="${ROOT}/repro_stderr.log"
: > "${STDOUT_LOG}"
: > "${STDERR_LOG}"

set +e
"${ROOT}/.venv/bin/python" "${ROOT}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
status=$?
set -e

echo "repro_exit_code=${status}"
exit 0
