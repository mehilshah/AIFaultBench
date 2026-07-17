#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${BUG458_VENV_DIR:-/tmp/bug458-venv}"

bash "$ROOT_DIR/setup_env.sh"

PYTHON_BIN="$VENV_DIR/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="$VENV_DIR/bin/python3"
fi

PYTHONPATH="$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}" \
  "$PYTHON_BIN" "$ROOT_DIR/repro.py"
