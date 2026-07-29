#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install pip==26.1.2
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install --no-deps -e codebase
