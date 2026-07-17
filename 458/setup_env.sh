#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${BUG458_VENV_DIR:-/tmp/bug458-venv}"

rm -rf "$VENV_DIR"
python3 -m venv "$VENV_DIR"

PYTHON_BIN="$VENV_DIR/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="$VENV_DIR/bin/python3"
fi

"$PYTHON_BIN" -m pip install -r "$ROOT_DIR/requirements.txt"
