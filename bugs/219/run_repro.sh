#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

bash "$ROOT_DIR/setup_env.sh"

STDOUT_LOG="$ROOT_DIR/repro_stdout.log"
STDERR_LOG="$ROOT_DIR/repro_stderr.log"

: >"$STDOUT_LOG"
: >"$STDERR_LOG"

set +e
"$ROOT_DIR/.venv/bin/python" "$ROOT_DIR/repro.py" >"$STDOUT_LOG" 2>"$STDERR_LOG"
status=$?
set -e

echo "exit_code=$status"
echo "stdout_log=$STDOUT_LOG"
echo "stderr_log=$STDERR_LOG"
exit "$status"

