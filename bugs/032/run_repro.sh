#!/usr/bin/env bash
set -euo pipefail

if [ -d .venv ]; then
  . .venv/bin/activate
fi

python repro.py
