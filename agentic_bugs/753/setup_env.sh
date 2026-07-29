#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install \
  --no-deps \
  -e codebase/llama-index-core \
  -e codebase/llama-index-integrations/llms/llama-index-llms-bedrock-converse
