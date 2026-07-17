#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  "$ROOT/setup_env.sh"
fi

PYTHONUNBUFFERED=1 "$ROOT/.venv/bin/python" "$ROOT/repro.py"
