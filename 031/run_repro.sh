#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  echo "Missing .venv. Run setup_env.sh first." >&2
  exit 1
fi

./.venv/bin/python repro.py
