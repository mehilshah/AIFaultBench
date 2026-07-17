#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

exec > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)

./setup_env.sh
source .venv/bin/activate
python repro.py
