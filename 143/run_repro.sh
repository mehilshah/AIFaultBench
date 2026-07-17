#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$ROOT/setup_env.sh"

PYTHONPATH="$ROOT/codebase" "$ROOT/.venv/bin/python" "$ROOT/repro.py" \
  >"$ROOT/repro_stdout.log" \
  2>"$ROOT/repro_stderr.log"
