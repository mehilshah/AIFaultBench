#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$ROOT/.venv" ]; then
  "$ROOT/setup_env.sh"
fi

source "$ROOT/.venv/bin/activate"

set +e
python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e
printf '%s\n' "$status" > "$ROOT/repro_exit_code.txt"
exit "$status"
