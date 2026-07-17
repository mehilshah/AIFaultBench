#!/usr/bin/env bash
set -euo pipefail

if [ ! -x .repro-venv/bin/python ]; then
  python3 -m venv .repro-venv
fi

.repro-venv/bin/python -m pip install --upgrade "pip==24.0" setuptools wheel packaging
