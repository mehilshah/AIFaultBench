#!/usr/bin/env bash
set -euo pipefail

bash ./setup_env.sh

VENV_PY=".venv/bin/python"
"${VENV_PY}" repro.py > repro_stdout.log 2> repro_stderr.log

