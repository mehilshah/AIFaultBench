#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout bc529a5f677db9c4b3fc72c76962c4e2f61567e1
# then: bash setup_env.sh && bash run_repro.sh
