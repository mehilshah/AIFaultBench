#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -x "$VENV/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install --upgrade --force-reinstall 'setuptools<81' wheel
"$VENV/bin/python" -m pip install --no-cache-dir torch==2.9.0 --index-url https://download.pytorch.org/whl/cpu
"$VENV/bin/python" -m pip install --no-cache-dir -r "$ROOT/requirements.txt"

PACKAGE_NAME=pytorch "$VENV/bin/python" -m pip install -e "$ROOT/codebase" --no-deps --no-build-isolation
