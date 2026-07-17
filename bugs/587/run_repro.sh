#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log" || true

if [[ -f "$ROOT/reproduction.json" ]]; then
  cat "$ROOT/reproduction.json"
fi
