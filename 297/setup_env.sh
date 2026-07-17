#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  python3 -m pip install --user -r requirements.txt
fi

uv --version
python3 --version
