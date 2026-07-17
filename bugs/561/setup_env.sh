#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to set up the repro environment" >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  uv venv --python 3.12 --seed --managed-python "$VENV_DIR"
fi

. "$VENV_DIR/bin/activate"
uv pip install -r "$ROOT/requirements.txt"
