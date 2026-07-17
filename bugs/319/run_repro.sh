#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_STDOUT="${ROOT_DIR}/repro_stdout.log"
LOG_STDERR="${ROOT_DIR}/repro_stderr.log"
RESULT_JSON="${ROOT_DIR}/reproduction.json"

rm -f "${LOG_STDOUT}" "${LOG_STDERR}" "${RESULT_JSON}"

python3 "${ROOT_DIR}/repro.py" \
  --result-file "${RESULT_JSON}" \
  --mode auto \
  >"${LOG_STDOUT}" \
  2>"${LOG_STDERR}"

cat "${RESULT_JSON}"
