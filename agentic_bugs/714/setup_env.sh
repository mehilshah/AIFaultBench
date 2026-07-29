#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
# Use the pinned buggy source, while the released wheel above supplies its dependencies.
.venv/bin/pip install --no-deps -e codebase/src/lfx
