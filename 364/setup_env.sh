#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONNOUSERSITE=1

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
