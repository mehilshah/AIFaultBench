#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/.venv/bin/activate"
export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"
export JAX_PLATFORMS=cpu

python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
