#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -x ".venv/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

PYTHONPATH="$ROOT/codebase" "$ROOT/.venv/bin/python" "$ROOT/repro.py"
