#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)/codebase/src${PYTHONPATH:+:${PYTHONPATH}}"

python3 repro.py > repro_stdout.log 2> repro_stderr.log
