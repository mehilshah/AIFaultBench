#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
  bash setup_env.sh
fi

: > repro_stdout.log
: > repro_stderr.log

set +e
.venv/bin/python repro.py >repro_stdout.log 2>repro_stderr.log
status=$?
set -e

exit "$status"
