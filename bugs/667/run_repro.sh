#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  bash setup_env.sh
fi
.venv/bin/python repro.py
