#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"

if [ ! -x "$VENV/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

source "$VENV/bin/activate"
exec python "$ROOT/repro.py"
