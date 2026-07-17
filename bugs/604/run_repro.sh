#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT/.venv}"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Virtual environment not found. Run ./setup_env.sh first." >&2
  exit 1
fi

exec "$VENV_DIR/bin/python" "$ROOT/repro.py"
