#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
# Install the pinned checkout itself without resolving its unrelated optional
# application dependencies; the requirements above cover this cache repro.
.venv/bin/python -m pip install --no-deps -e codebase/src/backend/base
