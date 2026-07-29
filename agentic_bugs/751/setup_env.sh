#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install \
  -e codebase/libs/checkpoint \
  -e codebase/libs/checkpoint-postgres \
  -e codebase/libs/prebuilt \
  -e codebase/libs/sdk-py \
  -e codebase/libs/langgraph
