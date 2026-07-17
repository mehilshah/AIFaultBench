#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
  PYTHON=""
  for candidate in python3.10 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON="$(command -v "$candidate")"
      break
    fi
  done
fi

if [[ -z "$PYTHON" ]]; then
  echo "No usable Python interpreter found." >&2
  exit 1
fi

export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

set -o pipefail
"$PYTHON" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
