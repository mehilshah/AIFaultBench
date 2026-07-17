#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$ROOT/.venv" ]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
fi

PYTHON_BIN="${PYTHON_BIN:-python3.10}"
if [ -x "$ROOT/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT/.venv/bin/python"
elif ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python3.10"
fi

PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}" \
  "$PYTHON_BIN" "$ROOT/repro.py" \
  >"$ROOT/repro_stdout.log" \
  2>"$ROOT/repro_stderr.log"
