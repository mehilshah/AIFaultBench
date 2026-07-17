#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"

if [[ ! -d "$VENV_DIR" ]]; then
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
if [[ -s "$ROOT_DIR/requirements.txt" ]]; then
  python -m pip install -r "$ROOT_DIR/requirements.txt"
fi
