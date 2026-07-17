#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ ! -x .venv_bug602/bin/python ]; then
  bash setup_env.sh
fi

source .venv_bug602/bin/activate
export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"
export TORCH_HOME="$ROOT/.torch_home"

python repro.py
