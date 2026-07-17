#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -q -U pip setuptools wheel
.venv/bin/python -m pip install -q -r requirements.txt
