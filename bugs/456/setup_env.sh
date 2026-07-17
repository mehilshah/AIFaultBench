#!/usr/bin/env bash
set -euo pipefail

if [ ! -d codebase ]; then
  bash setup_codebase.sh
fi

if [ ! -d .venv ]; then
  uv venv --python 3.9 .venv
fi
. .venv/bin/activate

if [ -s requirements.txt ]; then
  uv pip install --python .venv/bin/python -r requirements.txt
fi
