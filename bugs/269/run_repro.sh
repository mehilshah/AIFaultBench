#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

export PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$ROOT/.venv/bin/python" "$ROOT/repro.py"
