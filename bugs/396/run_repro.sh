#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
source .venv/bin/activate
export PYTHONPATH="$PWD/codebase/src${PYTHONPATH:+:$PYTHONPATH}"
python repro.py
