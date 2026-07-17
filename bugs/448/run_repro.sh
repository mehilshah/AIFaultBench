#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

: > repro_stdout.log
: > repro_stderr.log

bash setup_env.sh >> repro_stdout.log 2>> repro_stderr.log
source .venv/bin/activate
python repro.py >> repro_stdout.log 2>> repro_stderr.log
