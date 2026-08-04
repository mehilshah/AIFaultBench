#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/sentence-transformers codebase
git -C codebase checkout 03dff58425e0b9c2f52f6f29d51f430d0b60795a
# then: bash setup_env.sh && bash run_repro.sh
