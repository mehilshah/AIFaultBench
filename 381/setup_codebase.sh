#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 4aceabf8c1a40f8d576ba9b83e4b9a8854eda2d5
# then: bash setup_env.sh && bash run_repro.sh
