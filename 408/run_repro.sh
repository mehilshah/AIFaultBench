#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -x .venv/bin/python ]; then
  bash setup_env.sh
fi

PYTHONNOUSERSITE=1 .venv/bin/python repro.py \
  > repro_stdout.log \
  2> repro_stderr.log
