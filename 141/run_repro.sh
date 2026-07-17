#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

source "$ROOT/.venv/bin/activate"
export PYTHONPATH="$ROOT/codebase/bindings/python/py_src${PYTHONPATH:+:$PYTHONPATH}"

python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
cat "$ROOT/repro_stdout.log"
if [[ -s "$ROOT/repro_stderr.log" ]]; then
  cat "$ROOT/repro_stderr.log" >&2
fi
