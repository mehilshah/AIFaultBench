#!/usr/bin/env bash
set -euo pipefail

rm -f repro_stdout.log repro_stderr.log reproduction.json

python3 repro.py >repro_stdout.log 2>repro_stderr.log

cat repro_stdout.log
if [[ -s repro_stderr.log ]]; then
  cat repro_stderr.log >&2
fi
