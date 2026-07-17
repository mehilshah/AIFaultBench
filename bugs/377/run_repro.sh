#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

: > "${STDOUT_LOG}"
: > "${STDERR_LOG}"

{
  echo "[run_repro] setting up environment"
  bash "${ROOT_DIR}/setup_env.sh"
  echo "[run_repro] running repro"
  "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py"
} >>"${STDOUT_LOG}" 2>>"${STDERR_LOG}"
