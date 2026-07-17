#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON_VERSION="3.9.25"
VENV_DIR="$ROOT/.venv"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to provision Python ${PYTHON_VERSION}" >&2
  exit 1
fi

rm -rf "$VENV_DIR"
uv python install "$PYTHON_VERSION"
uv venv --python "$PYTHON_VERSION" "$VENV_DIR"
uv pip install --python "$VENV_DIR/bin/python" --upgrade pip
uv pip install --python "$VENV_DIR/bin/python" -r requirements.txt
