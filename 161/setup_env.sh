#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export REPRO_ROOT="$ROOT"
export PYTHONNOUSERSITE=1
export REPRO_PYTHON="$(command -v python3)"
"$REPRO_PYTHON" -m pip --version >/dev/null
