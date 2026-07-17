#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$ROOT/setup_env.sh"

set +e
"$ROOT/.venv/bin/python" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e

printf '%s\n' "$status" >"$ROOT/repro_exit_code.txt"
exit 0
