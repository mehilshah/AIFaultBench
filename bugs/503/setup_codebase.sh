#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 3bacf433889b345c75f8f0271bc3066bb15402d7
# then: bash setup_env.sh && bash run_repro.sh
