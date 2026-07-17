#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [ ! -d "$VENV_DIR" ]; then
  python3.12 -m venv "$VENV_DIR"
fi

# Keep the build pure-Python so the local codebase installs quickly in this folder.
export DS_BUILD_OPS=0

source "$VENV_DIR/bin/activate"
cd "$ROOT"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "$ROOT/requirements.txt"
