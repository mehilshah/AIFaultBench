#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ -x "$VENV_PYTHON" ]; then
    PYTHON="$VENV_PYTHON"
else
    PYTHON=python3
fi

"$PYTHON" "$SCRIPT_DIR/repro.py" >"$SCRIPT_DIR/repro_stdout.log" 2>"$SCRIPT_DIR/repro_stderr.log"
