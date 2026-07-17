#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 63168b151fa15987064a22c77b8b8ec72946f54e
# then: bash setup_env.sh && bash run_repro.sh
