#!/usr/bin/env bash
set -euo pipefail

VENV_PATH=".venv"
python3 -m venv "$VENV_PATH"
"$VENV_PATH/bin/python" -m pip install --upgrade pip
"$VENV_PATH/bin/python" -m pip install -r requirements.txt
"$VENV_PATH/bin/python" -m pip install -e codebase/python/packages/autogen-core -e codebase/python/packages/autogen-agentchat
