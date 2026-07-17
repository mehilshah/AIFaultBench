#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec > >(tee "$ROOT/repro_stdout.log") 2> >(tee "$ROOT/repro_stderr.log" >&2)

"$ROOT/setup_env.sh"
export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

VENV_DIR="${VENV_DIR:-$ROOT/.venv}"
"$VENV_DIR/bin/python" "$ROOT/repro.py"
