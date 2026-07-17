#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"

cd "${ROOT_DIR}"
PYTHONPATH="${ROOT_DIR}/codebase/src${PYTHONPATH:+:${PYTHONPATH}}" \
  "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
