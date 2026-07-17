#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -f "$ROOT/.repro_deps/.ready" ]]; then
  bash "$ROOT/setup_env.sh"
fi

PYTHONNOUSERSITE=1 PYTHONPATH="$ROOT/.repro_deps:$ROOT/codebase/src" \
  python3 "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
