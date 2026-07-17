#!/usr/bin/env bash
set -euo pipefail

python3 -m venv --clear .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
