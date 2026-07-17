#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${ROOT_DIR}/setup_env.sh"
PYTHONPATH="${ROOT_DIR}/codebase" "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" > "${ROOT_DIR}/repro_stdout.log" 2> "${ROOT_DIR}/repro_stderr.log"
cat "${ROOT_DIR}/repro_stdout.log"
if [[ -s "${ROOT_DIR}/repro_stderr.log" ]]; then
  printf '\n--- STDERR ---\n' >&2
  cat "${ROOT_DIR}/repro_stderr.log" >&2
fi
