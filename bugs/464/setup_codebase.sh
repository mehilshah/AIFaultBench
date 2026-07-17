#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout c96378c4136f5882fee50d8ff8ee1e9588a17eb6
# then: bash setup_env.sh && bash run_repro.sh
