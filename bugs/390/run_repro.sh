#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -d .repro_venv ]; then
  bash setup_env.sh
fi

source .repro_venv/bin/activate
export PYTHONNOUSERSITE=1
export PYTHONPATH="$ROOT/codebase/src"

python repro.py >repro_stdout.log 2>repro_stderr.log
