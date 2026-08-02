#!/usr/bin/env bash
set -euo pipefail

# The reported failure is specific to Python 3.13.  uv provides a pinned CPython
# interpreter on this host without requiring a system-wide Python installation.
uv venv --python 3.13 --seed .venv
.venv/bin/python -m pip install -r requirements.txt
