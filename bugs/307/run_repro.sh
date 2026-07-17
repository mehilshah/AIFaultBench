#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

exec > >(tee "$ROOT/repro_stdout.log") 2> >(tee "$ROOT/repro_stderr.log" >&2)

if [ ! -x ".venv/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

".venv/bin/python" "$ROOT/repro.py"
