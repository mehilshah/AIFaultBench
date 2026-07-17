#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout ab379793d44be16d8fcac5c098a3ab9b6f5a7ec3
# then: bash setup_env.sh && bash run_repro.sh
