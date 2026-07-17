#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/.venv/bin/activate"
export PYTHONPATH="$ROOT/codebase"

set +e
python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e
printf 'exit code: %s\n' "$status" >>"$ROOT/repro_stdout.log"
exit "$status"
