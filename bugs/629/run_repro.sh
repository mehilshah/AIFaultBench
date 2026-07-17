#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

JAX_CHECK_TRACER_LEAKS=1 "$ROOT/.venv/bin/python" "$ROOT/repro.py"
