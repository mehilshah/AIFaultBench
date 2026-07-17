#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT/.venv}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  "$ROOT/setup_env.sh" >/dev/null
fi

export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"
exec "$VENV_DIR/bin/python" "$ROOT/repro.py"
