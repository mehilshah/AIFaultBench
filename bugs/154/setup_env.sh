#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv --system-site-packages .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
