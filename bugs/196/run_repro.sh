#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

python3 repro.py > repro_stdout.log 2> repro_stderr.log
cat repro_stdout.log
if [[ -s repro_stderr.log ]]; then
  cat repro_stderr.log >&2
fi
