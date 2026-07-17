#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout b70d02fc724d04c916832ca4ead03ff05e8fb1ee
# then: bash setup_env.sh && bash run_repro.sh
