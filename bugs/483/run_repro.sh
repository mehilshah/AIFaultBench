#!/usr/bin/env bash
set -euo pipefail

if [ ! -x .venv/bin/python ]; then
  bash setup_env.sh
fi

stdout_file="repro_stdout.log"
stderr_file="repro_stderr.log"

: > "$stdout_file"
: > "$stderr_file"

PYTHONPATH="$PWD/codebase/src" .venv/bin/python repro.py >"$stdout_file" 2>"$stderr_file"

stdout_bytes=$(wc -c <"$stdout_file")
stderr_bytes=$(wc -c <"$stderr_file")

printf 'stdout_bytes=%s stderr_bytes=%s\n' "$stdout_bytes" "$stderr_bytes" | tee -a "$stderr_file"

if [ "$stdout_bytes" -eq 0 ] && [ "$stderr_bytes" -eq 0 ]; then
  printf 'No import-time diagnostics were emitted.\n' | tee -a "$stderr_file" >/dev/null
fi
