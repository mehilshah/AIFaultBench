#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 96256aa3dbfa058a8f963c9bf5c803447ccc1c54
# then: bash setup_env.sh && bash run_repro.sh
