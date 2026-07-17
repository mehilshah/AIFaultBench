#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  "$ROOT/setup_env.sh"
fi

exec "$VENV/bin/python" "$ROOT/repro.py"
