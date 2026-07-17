#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

{
  bash setup_env.sh
  . .venv/bin/activate
  python repro.py
} > repro_stdout.log 2> repro_stderr.log
