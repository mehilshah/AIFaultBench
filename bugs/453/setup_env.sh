#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -U pip setuptools wheel
.venv/bin/pip install -r requirements.txt
DS_BUILD_OPS=0 .venv/bin/pip install -e codebase
