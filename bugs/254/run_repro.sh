#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if [ ! -x "$ROOT/.venv_repro/bin/python" ]; then
  sh "$ROOT/setup_env.sh"
fi

PYTHON="$ROOT/.venv_repro/bin/python"
"$PYTHON" "$ROOT/repro.py"
