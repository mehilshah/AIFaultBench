#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT}/.venv/bin/activate"

export DS_ACCELERATOR=cpu
export MASTER_ADDR=127.0.0.1
export MASTER_PORT=29509
export RANK=0
export WORLD_SIZE=1
export LOCAL_RANK=0
export PYTHONPATH="${ROOT}/codebase"

python "${ROOT}/repro.py" >"${ROOT}/repro_stdout.log" 2>"${ROOT}/repro_stderr.log"
status=$?

cat "${ROOT}/repro_stdout.log"
if [[ -s "${ROOT}/repro_stderr.log" ]]; then
  cat "${ROOT}/repro_stderr.log" >&2
fi

exit "${status}"
