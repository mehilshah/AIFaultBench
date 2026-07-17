#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT}/repro_stdout.log"
STDERR_LOG="${ROOT}/repro_stderr.log"

: >"${STDOUT_LOG}"
: >"${STDERR_LOG}"

if [[ ! -x "${ROOT}/.venv/bin/python" ]]; then
  {
    echo "[setup] bootstrapping environment"
    bash "${ROOT}/setup_env.sh"
  } > >(tee -a "${STDOUT_LOG}") 2> >(tee -a "${STDERR_LOG}" >&2)
fi

{
  echo "[run] executing repro.py"
  "${ROOT}/.venv/bin/python" "${ROOT}/repro.py"
} > >(tee -a "${STDOUT_LOG}") 2> >(tee -a "${STDERR_LOG}" >&2)
