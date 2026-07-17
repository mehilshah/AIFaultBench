#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_STDOUT="${ROOT_DIR}/repro_stdout.log"
LOG_STDERR="${ROOT_DIR}/repro_stderr.log"

: >"${LOG_STDOUT}"
: >"${LOG_STDERR}"

"${ROOT_DIR}/setup_env.sh" >>"${LOG_STDOUT}" 2>>"${LOG_STDERR}"

source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONPATH="${ROOT_DIR}/codebase/src:${PYTHONPATH:-}"

python "${ROOT_DIR}/repro.py" >>"${LOG_STDOUT}" 2>>"${LOG_STDERR}"
