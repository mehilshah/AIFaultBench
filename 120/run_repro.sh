#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

bash "$ROOT_DIR/setup_env.sh"
source "$ROOT_DIR/.venv/bin/activate"

set +e
python repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e

printf 'repro exit status: %s\n' "$status"
exit "$status"
