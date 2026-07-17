#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 4ca863323d550842e7d0122efd57d84d9b75d1cf
# then: bash setup_env.sh && bash run_repro.sh
