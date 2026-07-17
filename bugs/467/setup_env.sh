#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ ! -d "$ROOT_DIR/codebase" ]]; then
  echo "codebase/ is missing; run setup_codebase.sh first." >&2
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip wheel
python -m pip install "setuptools<81"
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.6.0
python -m pip install -r "$ROOT_DIR/requirements.txt"
python -m pip install -e "$ROOT_DIR/codebase"
