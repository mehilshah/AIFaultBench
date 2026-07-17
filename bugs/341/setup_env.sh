#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -x .venv/bin/python ]]; then
  rm -rf .venv
  python3 -m venv .venv
fi

PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"

"$PYTHON_BIN" -m pip install -r requirements.txt
