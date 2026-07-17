#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  "$ROOT/setup_env.sh"
fi

PYTHONPATH="$ROOT/codebase" \
  "$ROOT/.venv/bin/python" "$ROOT/repro.py" \
  > "$ROOT/repro_stdout.log" \
  2> "$ROOT/repro_stderr.log"
