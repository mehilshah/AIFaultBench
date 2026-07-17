#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"
MARKER="$VENV_DIR/.repro_deps_installed"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip

if [[ ! -f "$MARKER" ]] || [[ "$ROOT/requirements.txt" -nt "$MARKER" ]]; then
  "$VENV_DIR/bin/python" -m pip install --no-cache-dir -r "$ROOT/requirements.txt"
  touch "$MARKER"
fi
