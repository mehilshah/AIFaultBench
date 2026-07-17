#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
