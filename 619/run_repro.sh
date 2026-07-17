#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT/.venv}"

"$ROOT/setup_env.sh"
source "$VENV_DIR/bin/activate"

: > "$ROOT/repro_stdout.log"
: > "$ROOT/repro_stderr.log"

exec > >(tee -a "$ROOT/repro_stdout.log") 2> >(tee -a "$ROOT/repro_stderr.log" >&2)

python "$ROOT/repro.py"
