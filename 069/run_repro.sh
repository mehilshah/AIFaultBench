#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  echo "Virtual environment not found. Run ./setup_env.sh first." >&2
  exit 1
fi

.venv/bin/python repro.py
