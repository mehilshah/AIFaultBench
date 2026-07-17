#!/usr/bin/env bash
set -euo pipefail

python3 repro.py --iterations "${1:-20}" 2>repro_stderr.log | tee repro_stdout.log
