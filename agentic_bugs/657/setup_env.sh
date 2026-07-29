#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
# The monorepo root is not itself a Python distribution. Install the two
# checkout packages imported by repro.py so the pinned source is exercised.
.venv/bin/python -m pip install --no-deps -e codebase/libs/core -e codebase/libs/partners/anthropic
