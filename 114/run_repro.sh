#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

: >"${STDOUT_LOG}"
: >"${STDERR_LOG}"

bash "${ROOT_DIR}/setup_env.sh" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"

source "${ROOT_DIR}/.venv/bin/activate"
python "${ROOT_DIR}/repro.py" >>"${STDOUT_LOG}" 2>>"${STDERR_LOG}"
