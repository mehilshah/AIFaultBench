#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required but not installed." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  uv venv .venv --python 3.12
fi

source .venv/bin/activate
uv pip install -r requirements.txt
