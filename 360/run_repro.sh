#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec > >(tee "$ROOT/repro_stdout.log") 2> >(tee "$ROOT/repro_stderr.log" >&2)

bash "$ROOT/setup_env.sh"

export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"
export JAX_PLATFORMS=cpu

"$ROOT/.venv/bin/python" "$ROOT/repro.py"
