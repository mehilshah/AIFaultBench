#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

set +e
"${VENV_DIR}/bin/python" "${ROOT_DIR}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
STATUS=$?
set -e

echo "repro exit status: ${STATUS}"
exit "${STATUS}"
