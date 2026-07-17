#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"
source "${ROOT_DIR}/.venv/bin/activate"

python "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
cat "${ROOT_DIR}/repro_stdout.log"
if [[ -s "${ROOT_DIR}/repro_stderr.log" ]]; then
  printf '\n--- stderr ---\n'
  cat "${ROOT_DIR}/repro_stderr.log"
fi
