#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv ]; then
python3 -m venv .venv
fi

source .venv/bin/activate
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install "$repo_root/codebase"
