#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
# This monorepo derives every package's development version from its Git revision.
# Install the sibling package first; then avoid pip trying to resolve that unreleased
# dynamic version from PyPI while installing the slim checkout.
.venv/bin/pip install -e codebase/pydantic_graph
.venv/bin/pip install --no-deps -e codebase/pydantic_ai_slim
