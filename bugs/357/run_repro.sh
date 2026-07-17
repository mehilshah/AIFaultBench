#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

bash setup_env.sh

mkdir -p .mypy_cache

exec > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)

.venv/bin/mypy \
  --cache-dir .mypy_cache \
  --install-types \
  --non-interactive \
  --config-file codebase/setup.cfg \
  repro.py
