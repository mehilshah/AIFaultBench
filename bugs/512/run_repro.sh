#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_STDOUT="${ROOT_DIR}/repro_stdout.log"
LOG_STDERR="${ROOT_DIR}/repro_stderr.log"

if [[ ! -d "${ROOT_DIR}/.venv" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONPATH="${ROOT_DIR}/codebase/src${PYTHONPATH:+:${PYTHONPATH}}"

set +e
python "${ROOT_DIR}/repro.py" >"${LOG_STDOUT}" 2>"${LOG_STDERR}"
exit_code=$?
set -e

echo "${exit_code}" > "${ROOT_DIR}/repro_exit_code.txt"
exit "${exit_code}"
