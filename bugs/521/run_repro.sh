#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  "$ROOT/setup_env.sh"
fi

export PYTHONPATH="$ROOT:$ROOT/codebase/src"
exec "$ROOT/.venv/bin/python" "$ROOT/repro.py"
