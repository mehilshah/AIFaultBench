#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${ROOT}/.venv"

if [[ ! -x "${VENV}/bin/python" ]]; then
  echo "Missing virtualenv. Run ./setup_env.sh first." >&2
  exit 1
fi

source "${VENV}/bin/activate"
export PYTHONNOUSERSITE=1

stdout_log="${ROOT}/repro_stdout.log"
stderr_log="${ROOT}/repro_stderr.log"
: > "${stdout_log}"
: > "${stderr_log}"

set +e
timeout 5s python -u "${ROOT}/repro.py" >"${stdout_log}" 2>"${stderr_log}"
status=$?
set -e

if grep -q '^call start$' "${stdout_log}" && ! grep -q '^call returned ' "${stdout_log}"; then
  status=124
  echo "result=timeout" >> "${stdout_log}"
fi

{
  echo "exit_status=${status}"
} >> "${stdout_log}"

exit "${status}"
