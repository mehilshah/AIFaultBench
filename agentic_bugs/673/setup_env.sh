#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
# The repository is a monorepo; the Python package lives in this subdirectory.
.venv/bin/python -m pip install --no-deps -e codebase/libs/agno
