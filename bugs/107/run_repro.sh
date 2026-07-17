#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -d .venv ]; then
  bash setup_env.sh
fi

# shellcheck disable=SC1091
source .venv/bin/activate

: > repro_stdout.log
: > repro_stderr.log

python repro.py > repro_stdout.log 2> repro_stderr.log
