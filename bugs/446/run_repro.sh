#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  bash setup_env.sh
fi

. .venv/bin/activate
python repro.py > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)
