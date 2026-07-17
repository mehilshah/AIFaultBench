#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="$PWD/codebase${PYTHONPATH:+:$PYTHONPATH}" python3 repro.py \
  > repro_stdout.log \
  2> repro_stderr.log
