#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install --index-url https://download.pytorch.org/whl/cpu -r requirements.txt
python -m pip install -e codebase
