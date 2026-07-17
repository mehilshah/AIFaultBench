#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

set +e
"${VENV_DIR}/bin/python" "${ROOT_DIR}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
exit_code=$?
set -e

exit "${exit_code}"

