#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
# The repository is a multi-package workspace without a root Python project.
.venv/bin/python -m pip install --no-deps -e codebase/libs/core -e codebase/libs/partners/anthropic
