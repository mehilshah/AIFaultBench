#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

bash setup_env.sh

python3 repro.py \
  > >(tee repro_stdout.log) \
  2> >(tee repro_stderr.log >&2)
