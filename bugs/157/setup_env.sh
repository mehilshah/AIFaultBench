#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.repro-venv"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv --system-site-packages "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install -q --upgrade pip
python -m pip install -q -r "$ROOT_DIR/requirements.txt"
