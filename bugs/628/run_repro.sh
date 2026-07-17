#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

rm -f "$ROOT/repro_stdout.log" "$ROOT/repro_stderr.log"

set +e
timeout 40s env PYTHONPATH="$ROOT/codebase" "$ROOT/.venv/bin/python" "$ROOT/repro.py" \
  >"$ROOT/repro_stdout.log" \
  2>"$ROOT/repro_stderr.log"
status=$?
set -e

exit "$status"
