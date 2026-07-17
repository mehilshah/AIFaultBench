#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/python ]]; then
  echo "Virtualenv not found; run ./setup_env.sh first." >&2
  exit 1
fi

set +e
.venv/bin/python repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e

printf '{"exit_code":%d}\n' "$status" > repro_run_status.json
exit "$status"
