#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/python ]]; then
  bash setup_env.sh
fi

. .venv/bin/activate
python repro.py > repro_stdout.log 2> repro_stderr.log
