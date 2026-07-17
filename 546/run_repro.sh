#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

export PYTHONPATH="$(pwd)/codebase/src${PYTHONPATH:+:${PYTHONPATH}}"
python repro.py > repro_stdout.log 2> repro_stderr.log
