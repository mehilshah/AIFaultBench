#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/safetensors codebase
git -C codebase checkout 079781fd0dc455ba0fe851e2b4507c33d0c0d407
# then: bash setup_env.sh && bash run_repro.sh
