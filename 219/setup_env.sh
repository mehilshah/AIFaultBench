#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_VERSION="3.10.13"

cd "$ROOT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to create the Python 3.10 environment." >&2
  exit 1
fi

uv python install "$PYTHON_VERSION" >/dev/null

rm -rf "$VENV_DIR"
uv venv --seed --python "$PYTHON_VERSION" "$VENV_DIR" >/dev/null

"$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null
"$VENV_DIR/bin/python" -m pip install -r requirements.txt >/dev/null
