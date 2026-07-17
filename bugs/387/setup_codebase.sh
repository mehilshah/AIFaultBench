#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout b895858c1e306b64f5debf7adc78bdb2b9c78131
# then: bash setup_env.sh && bash run_repro.sh
