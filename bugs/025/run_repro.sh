#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

bash setup_env.sh >repro_stdout.log 2>repro_stderr.log
python3 repro.py >>repro_stdout.log 2>>repro_stderr.log
