#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .venv/bin/activate ]]; then
  bash setup_env.sh
fi

. .venv/bin/activate
export KERAS_BACKEND=tensorflow
python repro.py
