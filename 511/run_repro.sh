#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${ROOT}/.venv/bin/python"

if [[ ! -x "${PYTHON}" ]]; then
  echo "Missing virtualenv. Run bash setup_env.sh first." >&2
  exit 1
fi

"${PYTHON}" "${ROOT}/repro.py" > "${ROOT}/repro_stdout.log" 2> "${ROOT}/repro_stderr.log"
