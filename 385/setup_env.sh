#!/usr/bin/env bash
set -euo pipefail

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
