#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

exec > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

PYTHONUNBUFFERED=1 "$ROOT/.venv/bin/python" "$ROOT/repro.py"
