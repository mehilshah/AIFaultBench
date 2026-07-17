#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Virtual environment not found. Run ./setup_env.sh first." >&2
  exit 2
fi

source "$VENV_DIR/bin/activate"
python "$ROOT/repro.py"
