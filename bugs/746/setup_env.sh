#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d codebase/.git ]]; then
    bash setup_codebase.sh
fi

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install --no-deps \
    -e codebase/libs/core \
    -e codebase/libs/text-splitters \
    -e codebase/libs/langchain
