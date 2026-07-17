#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "${ROOT_DIR}/.venv/bin/python" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

cd "${ROOT_DIR}"
"${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
