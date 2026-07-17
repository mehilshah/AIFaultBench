#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.7.1 torchvision==0.22.1
python -m pip install -r "$ROOT/requirements.txt"

export PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}"
