#!/usr/bin/env bash
set -euo pipefail

. .venv/bin/activate
python repro.py > repro_stdout.log 2> repro_stderr.log
