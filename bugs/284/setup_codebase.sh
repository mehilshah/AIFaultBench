#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 208704a27a6f362b67cd1a04fa1db0b98036d26f
# then: bash setup_env.sh && bash run_repro.sh
