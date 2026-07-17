#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$ROOT/setup_env.sh"
source "$ROOT/.venv/bin/activate"

PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}" \
  python "$ROOT/repro.py" \
  > >(tee "$ROOT/repro_stdout.log") \
  2> >(tee "$ROOT/repro_stderr.log" >&2)
