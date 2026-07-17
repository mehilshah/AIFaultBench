#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir --force-reinstall --index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1+cpu'
python -m pip install -r requirements.txt
