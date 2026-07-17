#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

PYTHON_BIN="$ROOT/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="$(command -v python3)"
fi

set +e
"$PYTHON_BIN" repro.py >repro_stdout.log 2>repro_stderr.log
status=$?
set -e

printf 'repro exit code: %s\n' "$status"
exit "$status"
