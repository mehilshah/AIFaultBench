#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --requirement requirements.txt
.venv/bin/python -m pip install --no-deps --editable codebase
