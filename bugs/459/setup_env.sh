#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
