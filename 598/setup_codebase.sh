#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout b22f088ff662de748cf3f97c7ad8bf5a6dd6a7b9
# then: bash setup_env.sh && bash run_repro.sh
