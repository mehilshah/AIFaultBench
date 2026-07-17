#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

PYTHONNOUSERSITE=1 .venv/bin/python -m pip install --upgrade pip
PYTHONNOUSERSITE=1 .venv/bin/python -m pip install -r requirements.txt
