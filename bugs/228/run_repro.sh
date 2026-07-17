#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

STDOUT_LOG="$ROOT/repro_stdout.log"
STDERR_LOG="$ROOT/repro_stderr.log"

rm -f "$STDOUT_LOG" "$STDERR_LOG"

"$VENV_DIR/bin/python" "$ROOT/repro.py" >"$STDOUT_LOG" 2>"$STDERR_LOG"
cat "$STDOUT_LOG"
if [[ -s "$STDERR_LOG" ]]; then
  cat "$STDERR_LOG" >&2
fi
