#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 3467efa65a27e4b4c3caa6e01ebb9ca035e14674
# then: bash setup_env.sh && bash run_repro.sh
