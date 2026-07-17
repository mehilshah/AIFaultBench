#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

set +e
python "$ROOT_DIR/repro.py" >"$ROOT_DIR/repro_stdout.log" 2>"$ROOT_DIR/repro_stderr.log"
status=$?
set -e

cat "$ROOT_DIR/repro_stdout.log"
cat "$ROOT_DIR/repro_stderr.log" >&2

exit "$status"
