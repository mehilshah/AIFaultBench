#!/usr/bin/env bash
set -euo pipefail

if [ -x .venv/bin/python ]; then
  .venv/bin/python repro.py
else
  python3 repro.py
fi
