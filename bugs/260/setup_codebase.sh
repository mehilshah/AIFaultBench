#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 41ce2b9f35ee3aabeee1ae401b6d9130100b496b
# then: bash setup_env.sh && bash run_repro.sh
