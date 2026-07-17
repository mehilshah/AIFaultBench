#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$ROOT/.venv/bin/activate" ]; then
  bash "$ROOT/setup_env.sh"
fi

# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"

export JAX_PLATFORMS=cpu
export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

python "$ROOT/repro.py"
