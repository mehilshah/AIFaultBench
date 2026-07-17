#!/usr/bin/env bash
set -euo pipefail

rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e ./codebase
