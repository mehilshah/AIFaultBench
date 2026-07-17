#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [ ! -x "${VENV_PYTHON}" ]; then
  bash "${ROOT_DIR}/setup_env.sh" >>"${STDOUT_LOG}" 2>>"${STDERR_LOG}"
fi

: > "${STDOUT_LOG}"
: > "${STDERR_LOG}"

set +e
"${VENV_PYTHON}" "${ROOT_DIR}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
exit_code=$?
set -e

cat "${STDOUT_LOG}"
if [ -s "${STDERR_LOG}" ]; then
  cat "${STDERR_LOG}" >&2
fi

exit "${exit_code}"
