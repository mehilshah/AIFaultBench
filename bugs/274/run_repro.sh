#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="$(pwd)/codebase:${PYTHONPATH:-}"
if [ ! -x .venv/bin/python ]; then
  echo "Missing .venv; run ./setup_env.sh first." >&2
  exit 1
fi
.venv/bin/python repro.py
