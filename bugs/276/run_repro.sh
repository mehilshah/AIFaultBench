#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 repro.py >repro_stdout.log 2>repro_stderr.log
