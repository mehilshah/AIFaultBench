#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
# langgraph is a monorepo; its installable package lives in this subdirectory.
.venv/bin/python -m pip install --no-deps -e codebase/libs/langgraph
