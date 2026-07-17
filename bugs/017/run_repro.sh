#!/usr/bin/env bash
set -euo pipefail

. .venv/bin/activate
export PYTHONPATH="$(pwd)/codebase/research:${PYTHONPATH:-}"
python repro.py
