#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Run setup_env.sh first" >&2
  exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
export PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}"

python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
