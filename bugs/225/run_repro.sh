#!/usr/bin/env bash
set -euo pipefail

bash ./setup_env.sh
.venv/bin/python ./repro.py
