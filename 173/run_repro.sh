#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  bash setup_env.sh
fi

if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python repro.py

