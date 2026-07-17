#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

: > repro_stdout.log
: > repro_stderr.log

exec > >(tee -a repro_stdout.log) 2> >(tee -a repro_stderr.log >&2)

echo "[setup] installing runtime dependencies"
bash ./setup_env.sh

echo "[run] executing repro.py"
PYTHONPATH="$PWD/codebase/src" python3 repro.py
