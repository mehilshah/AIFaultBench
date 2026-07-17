#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

bash setup_env.sh >repro_stderr.log 2>&1 || {
  cat repro_stderr.log
  exit 1
}

.venv/bin/python repro.py >repro_stdout.log 2>>repro_stderr.log
