#!/usr/bin/env bash
set -euo pipefail

# The repro itself is stdlib-only, but keep the environment hook for parity
# with other standardized bug folders.
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
if [ -s requirements.txt ]; then
  python -m pip install -r requirements.txt
fi
