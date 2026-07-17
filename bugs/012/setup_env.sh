#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_PY="$VENV_DIR/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
  rm -rf "$VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install --no-cache-dir -r "$ROOT/requirements.txt"
