#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3.9}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Missing $PYTHON_BIN; this repro expects a Python 3.9 interpreter." >&2
  exit 1
fi

if [ ! -d "$VENV" ]; then
  "$PYTHON_BIN" -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$ROOT/requirements.txt"
