#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

bash setup_env.sh

. .venv/bin/activate
set +e
python repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e
exit "$status"
