#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

source ./setup_env.sh
python3 ./repro.py
