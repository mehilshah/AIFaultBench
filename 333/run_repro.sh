#!/usr/bin/env bash
set -euo pipefail

bash setup_env.sh
python3 repro.py
