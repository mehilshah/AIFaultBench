#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

set +e
"${PYTHON_BIN}" "${ROOT_DIR}/repro.py" \
  >"${ROOT_DIR}/repro_stdout.log" \
  2>"${ROOT_DIR}/repro_stderr.log"
status=$?
set -e

cat "${ROOT_DIR}/repro_stdout.log"
cat "${ROOT_DIR}/repro_stderr.log" >&2

exit "${status}"
