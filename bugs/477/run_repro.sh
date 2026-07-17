#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/pyrefly ]]; then
  bash setup_env.sh
fi

code="$(cat repro.py)"

# Snippet mode reproduces the unresolved-attribute diagnostic reliably here.
.venv/bin/pyrefly snippet "$code" \
  --search-path codebase \
  --python-interpreter-path .venv/bin/python \
  --summary=none \
  --progress-bar no \
  --output-format full-text
