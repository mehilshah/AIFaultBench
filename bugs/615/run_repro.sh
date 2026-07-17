#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

source "$VENV_DIR/bin/activate"
export PYTHONPATH="$ROOT/codebase:${PYTHONPATH:-}"
python "$ROOT/repro.py"
