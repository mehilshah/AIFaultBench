#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

PYTHONPATH="$ROOT/codebase" TEST_ENUM_PYRO_BACKEND=contrib.funsor \
  "$ROOT/.venv/bin/python" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
