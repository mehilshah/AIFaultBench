#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -x .venv/bin/python ]; then
  bash ./setup_env.sh
fi

set +e
PYTHONNOUSERSITE=1 .venv/bin/python repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e

printf '%s\n' "$status" > repro_exit_code.txt
exit "$status"
