#!/usr/bin/env bash
set -euo pipefail

python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
export PYTHONPATH="$(pwd)/codebase/src"
