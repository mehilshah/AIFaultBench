#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout e4620984f8f2d3b91585f7d8c03f8c57cd453f50
# then: bash setup_env.sh && bash run_repro.sh
