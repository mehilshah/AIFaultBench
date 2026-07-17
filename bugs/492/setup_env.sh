#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="/tmp/repro_bug_492_venv"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel
"$VENV_DIR/bin/python" -m pip install -r requirements.txt
