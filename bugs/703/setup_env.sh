#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e codebase/pydantic_graph
.venv/bin/python -m pip install -e 'codebase/pydantic_ai_slim[bedrock]'
