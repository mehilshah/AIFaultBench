#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip setuptools wheel
.venv/bin/pip install -r requirements.txt
