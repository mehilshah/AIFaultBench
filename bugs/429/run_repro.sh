#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "BLOCKED: the reported crash requires macOS with Apple MPS; current host is $(uname -s)." 
  exit 2
fi

bash "$ROOT/setup_env.sh"
source "$ROOT/.venv/bin/activate"
python "$ROOT/repro.py"
