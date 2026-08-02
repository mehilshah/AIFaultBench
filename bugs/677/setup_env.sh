#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
# The source checkout is the system under test. --no-deps keeps the issue-era
# OpenAI/OpenTelemetry pins above instead of resolving unrelated SDK extras.
.venv/bin/python -m pip install -e codebase/python --no-deps
