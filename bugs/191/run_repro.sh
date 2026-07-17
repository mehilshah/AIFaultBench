#!/usr/bin/env bash
set -euo pipefail

./setup_env.sh
.repro-venv/bin/python repro.py
