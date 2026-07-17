#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -U pip setuptools wheel
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install --no-build-isolation -e codebase
