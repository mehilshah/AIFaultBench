#!/usr/bin/env bash
set -euo pipefail

# The repro is stdlib-only, but create a venv so the run is isolated from any
# preinstalled packages in the host Python environment.
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

echo "Virtual environment ready at .venv"
