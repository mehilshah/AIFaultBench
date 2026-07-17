#!/usr/bin/env bash
set -euo pipefail

exec > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)

if [ ! -x .venv/bin/python ]; then
  bash setup_env.sh
fi

.venv/bin/python repro.py
