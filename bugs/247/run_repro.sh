#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="$ROOT/repro_stdout.log"
STDERR_LOG="$ROOT/repro_stderr.log"
VENV_PYTHON="$ROOT/.venv/bin/python"

"$ROOT/setup_env.sh"

: >"$STDOUT_LOG"
: >"$STDERR_LOG"

PYTHONPATH="$ROOT/codebase" "$VENV_PYTHON" "$ROOT/repro.py" \
  1>"$STDOUT_LOG" \
  2>"$STDERR_LOG"
