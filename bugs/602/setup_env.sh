#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

python3 -m venv .venv_bug602
source .venv_bug602/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
