#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT/codebase:$ROOT${PYTHONPATH:+:$PYTHONPATH}"

python3 repro.py > repro_stdout.log 2> repro_stderr.log
