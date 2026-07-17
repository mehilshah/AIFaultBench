#!/usr/bin/env bash
set -euo pipefail

rm -rf .venv
python3 -m venv .venv

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple -r requirements.txt
