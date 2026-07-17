#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  bash setup_env.sh
fi

. .venv/bin/activate
export PYTHONPATH="$ROOT_DIR/codebase/src${PYTHONPATH:+:$PYTHONPATH}"
python repro.py
