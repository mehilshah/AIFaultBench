#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT_DIR}/.venv/bin/activate"

export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"
export PYTHONUNBUFFERED=1

stdout_log="${ROOT_DIR}/repro_stdout.log"
stderr_log="${ROOT_DIR}/repro_stderr.log"
: >"${stdout_log}"
: >"${stderr_log}"

python "${ROOT_DIR}/repro.py" >"${stdout_log}" 2>"${stderr_log}"
