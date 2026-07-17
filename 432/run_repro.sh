#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

: > repro_stdout.log
: > repro_stderr.log

exec > >(tee -a repro_stdout.log)
exec 2> >(tee -a repro_stderr.log >&2)

bash setup_env.sh
source "$ROOT/.venv/bin/activate"
python repro.py
