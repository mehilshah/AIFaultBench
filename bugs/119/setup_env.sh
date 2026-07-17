#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 -m pip install -e ./codebase
