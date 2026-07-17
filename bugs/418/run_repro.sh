#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  bash setup_env.sh
fi

source .venv/bin/activate
python repro.py
