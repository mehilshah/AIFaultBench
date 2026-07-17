#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  echo "Virtualenv not found. Run ./setup_env.sh first." >&2
  exit 1
fi

PYTHONPATH="$ROOT/codebase" "$ROOT/.venv/bin/python" "$ROOT/repro.py"
