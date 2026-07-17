#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3.11 >/dev/null 2>&1; then
  PYTHON_BIN="python3.11"
else
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" -m venv "$ROOT_DIR/.venv"
"$ROOT_DIR/.venv/bin/python" -m pip install --upgrade pip setuptools wheel
"$ROOT_DIR/.venv/bin/pip" install -r "$ROOT_DIR/requirements.txt"
