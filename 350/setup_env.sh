#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -d .venv ]; then
  python3.12 -m venv .venv
fi

PYTHONNOUSERSITE=1 .venv/bin/python -m pip install --upgrade pip setuptools wheel
PYTHONNOUSERSITE=1 .venv/bin/python -m pip install -r requirements.txt
