#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

: >"${STDOUT_LOG}"
: >"${STDERR_LOG}"

"${ROOT_DIR}/setup_env.sh" >>"${STDOUT_LOG}" 2>>"${STDERR_LOG}"

PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}" \
  python3 "${ROOT_DIR}/repro.py" \
  --mode single \
  --single-steps 20 \
  --seq-len 1024 \
  --batch-size 2 \
  >>"${STDOUT_LOG}" 2>>"${STDERR_LOG}"
