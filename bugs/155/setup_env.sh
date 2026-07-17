#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

VENV_DIR="$PWD/.venv"
if [ ! -x "$VENV_DIR/bin/python3" ]; then
  python3 -m venv "$VENV_DIR"
fi

export PATH="$VENV_DIR/bin:$PATH"
python3 -m pip install --quiet --disable-pip-version-check -r requirements.txt
export PYTHONPATH="$PWD/codebase/src${PYTHONPATH:+:$PYTHONPATH}"
