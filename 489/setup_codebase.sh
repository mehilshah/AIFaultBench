#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout b2034bb6c57fa6b41fda7398140bf21405361df7
# then: bash setup_env.sh && bash run_repro.sh
