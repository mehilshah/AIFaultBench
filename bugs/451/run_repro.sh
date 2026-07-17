#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="$ROOT/.venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
  bash "$ROOT/setup_env.sh"
fi

"$VENV_PY" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
