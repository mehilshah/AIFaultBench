#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/triton-inference-server/server codebase
git -C codebase checkout 441d7cf5f7e8531f8e2d07b8f48ff501bb029a99
# then: bash setup_env.sh && bash run_repro.sh
