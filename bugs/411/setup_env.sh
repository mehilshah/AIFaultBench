#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install --no-deps -r requirements.txt
python -m pip install --no-deps -e codebase
