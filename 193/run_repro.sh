#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -x .venv/bin/python ]]; then
  bash setup_env.sh
fi

: > repro_stdout.log
: > repro_stderr.log

JAX_TRACEBACK_FILTERING=off .venv/bin/python repro.py \
  > >(tee -a repro_stdout.log) \
  2> >(tee -a repro_stderr.log >&2)
