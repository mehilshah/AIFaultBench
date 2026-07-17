#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -d codebase ]; then
  bash setup_codebase.sh
fi

if [ ! -d .repro_venv ]; then
  python3 -m venv .repro_venv
fi

source .repro_venv/bin/activate

python -m pip install -U pip setuptools wheel
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.13.0
python -m pip install -r requirements.txt
