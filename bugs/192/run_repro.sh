#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$root_dir"

: > repro_stdout.log
: > repro_stderr.log

bash setup_env.sh >repro_stdout.log 2>>repro_stderr.log
python3 repro.py >>repro_stdout.log 2>>repro_stderr.log
