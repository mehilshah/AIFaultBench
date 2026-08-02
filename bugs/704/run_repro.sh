#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d codebase/.git ]]; then
  bash setup_codebase.sh
fi

if [[ ! -x .venv/bin/python ]]; then
  bash setup_env.sh
fi

.venv/bin/python repro.py
