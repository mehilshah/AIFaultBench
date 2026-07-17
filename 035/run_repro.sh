#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -x ".venv/bin/python" ]; then
  bash setup_env.sh
fi

. .venv/bin/activate

python repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
printf 'exit_code=%s\n' "$status" | tee -a repro_stdout.log
exit "$status"
