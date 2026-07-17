#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  bash setup_env.sh
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python repro.py
