#!/usr/bin/env bash
set -euo pipefail

if [ ! -x .venv/bin/python ]; then
  bash ./setup_env.sh
fi

. .venv/bin/activate
export PYTHONPATH="$(pwd)/codebase${PYTHONPATH:+:$PYTHONPATH}"
python repro.py
