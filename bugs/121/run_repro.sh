#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

bash setup_env.sh

set +e
PYTHONPATH="$ROOT_DIR/.deps:$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}" python3 repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e

exit "$status"
