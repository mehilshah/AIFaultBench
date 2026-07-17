#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -x .venv/bin/python ]; then
  bash setup_env.sh
fi

set +e
.venv/bin/python -u repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e

exit "$status"
