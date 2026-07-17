#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONNOUSERSITE=1
. .venv/bin/activate
python repro.py
