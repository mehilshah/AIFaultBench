#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

PYTHONNOUSERSITE=1 "$ROOT/.venv/bin/python" "$ROOT/repro.py"
