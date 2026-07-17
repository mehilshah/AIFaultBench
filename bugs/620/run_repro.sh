#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  ./setup_env.sh
fi

. .venv/bin/activate
python repro.py >repro_stdout.log 2>repro_stderr.log
