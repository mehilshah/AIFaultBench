#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

: > repro_stdout.log
: > repro_stderr.log

echo "Running: python3 repro.py" | tee repro_stdout.log
python3 repro.py >> repro_stdout.log 2>> repro_stderr.log
