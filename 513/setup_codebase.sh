#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 37831808444e089a182f66713935d27c39a0cf2c
# then: bash setup_env.sh && bash run_repro.sh
