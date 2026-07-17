#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}"

if [ -x "$ROOT/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT/.venv/bin/python"
else
  PYTHON_BIN="$(command -v python3)"
fi

"$PYTHON_BIN" repro.py 2> >(tee repro_stderr.log >&2) | tee repro_stdout.log
