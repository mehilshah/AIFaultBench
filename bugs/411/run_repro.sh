#!/usr/bin/env bash
set -euo pipefail

bash ./setup_env.sh

. .venv/bin/activate
export HF_HUB_DISABLE_XET=1

python repro.py > repro_stdout.log 2> repro_stderr.log
