#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$ROOT/setup_env.sh"
fi

export PYTHONPATH="$ROOT/codebase/src"

"$VENV_DIR/bin/python" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
