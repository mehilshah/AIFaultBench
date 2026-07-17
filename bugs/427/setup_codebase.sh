#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 0645384b3a68d0ddf4657400125bb2c68c42bc60
# then: bash setup_env.sh && bash run_repro.sh
