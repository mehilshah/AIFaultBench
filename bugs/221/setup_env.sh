#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

export PIP_DISABLE_PIP_VERSION_CHECK=1
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$ROOT/requirements.txt"
"$VENV_DIR/bin/python" -m pip install -e "$ROOT/codebase" --no-deps
