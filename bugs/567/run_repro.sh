#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

if [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PYTHON="${ROOT}/.venv/bin/python"
else
  PYTHON="python3"
fi

: > repro_stdout.log
: > repro_stderr.log

"${PYTHON}" repro.py >repro_stdout.log 2>repro_stderr.log
status=$?

exit "${status}"
