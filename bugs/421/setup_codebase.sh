#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 4757c7c465157ce843294424a5dd9fcd24f52cb2
# then: bash setup_env.sh && bash run_repro.sh
