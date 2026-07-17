#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout fdb6d318138c10ad29ac750388917808f50c867c
# then: bash setup_env.sh && bash run_repro.sh
