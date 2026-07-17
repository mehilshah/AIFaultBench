#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 907a86d145cc62521ea0281eb24465f537480e2d
# then: bash setup_env.sh && bash run_repro.sh
