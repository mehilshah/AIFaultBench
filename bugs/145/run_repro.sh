#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  bash setup_env.sh
fi

source .venv/bin/activate
python repro.py > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)
