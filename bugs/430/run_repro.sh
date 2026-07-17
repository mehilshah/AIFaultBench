#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"

export PYTHONNOUSERSITE=1
python "$ROOT/repro.py"
