#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv --system-site-packages .venv
fi

PYTHONNOUSERSITE=1 .venv/bin/python -m pip install --upgrade pip
PYTHONNOUSERSITE=1 .venv/bin/python -m pip install --upgrade --force-reinstall -r requirements.txt
PYTHONNOUSERSITE=1 .venv/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu --upgrade --force-reinstall torch==2.5.1
