#!/usr/bin/env bash
set -uo pipefail

source .venv/bin/activate
python repro.py --cuda --num-data 10 --batch-size 10 --num-epochs 1 \
  > repro_stdout.log \
  2> repro_stderr.log
exit $?
