#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 4d47b06102805e02662d5d9865994bed8aa6d7fb
# then: bash setup_env.sh && bash run_repro.sh
