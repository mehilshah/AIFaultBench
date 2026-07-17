#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$ROOT/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
  echo "Virtualenv not found. Run ./setup_env.sh first." >&2
  exit 1
fi

exec "$PYTHON" "$ROOT/repro.py"
