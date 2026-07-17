#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_COMMIT="b1059b73aab9043b118ff19b0cf96263ea86248a"
if [[ ! -d "$ROOT_DIR/codebase/.git" ]] || [[ "$(git -C "$ROOT_DIR/codebase" rev-parse HEAD 2>/dev/null || true)" != "$TARGET_COMMIT" ]]; then
  rm -rf "$ROOT_DIR/codebase"
  bash "$ROOT_DIR/setup_codebase.sh"
fi
if [[ -f "$ROOT_DIR/.venv_repro/bin/activate" ]]; then
  source "$ROOT_DIR/.venv_repro/bin/activate"
else
  source "$ROOT_DIR/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT_DIR/codebase/src${PYTHONPATH:+:$PYTHONPATH}"

python "$ROOT_DIR/repro.py"
