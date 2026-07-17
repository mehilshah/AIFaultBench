#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
VENV="$ROOT/.venv_repro"

if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV"
fi

exit 0
