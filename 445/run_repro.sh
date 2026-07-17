#!/usr/bin/env bash
set -euo pipefail

source .venv445/bin/activate
python repro.py > repro_stdout.log 2> repro_stderr.log
