#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

source "$ROOT/.venv/bin/activate"
exec > >(tee "$ROOT/repro_stdout.log") 2> >(tee "$ROOT/repro_stderr.log" >&2)
python -u "$ROOT/repro.py"
