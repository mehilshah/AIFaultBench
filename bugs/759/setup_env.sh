#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
# The library implementation is in the slim workspace package; install it and its local graph dependency.
.venv/bin/python -m pip install --no-deps -e codebase/pydantic_graph -e codebase/pydantic_ai_slim
