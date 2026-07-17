#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  bash setup_env.sh
fi

. .venv/bin/activate

set +e
python repro.py > repro_stdout.log 2> repro_stderr.log
rc=$?
set -e

echo "$rc" > repro_repro_rc.txt
exit "$rc"
