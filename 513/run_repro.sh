#!/usr/bin/env bash
set -euo pipefail

. .venv/bin/activate
export PYTHONUNBUFFERED=1
python repro.py
