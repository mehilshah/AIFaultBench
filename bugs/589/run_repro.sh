#!/usr/bin/env bash
set -euo pipefail

bash setup_env.sh
.venv/bin/python repro.py > repro_stdout.log 2> repro_stderr.log
