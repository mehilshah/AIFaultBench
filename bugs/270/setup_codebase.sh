#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout b9ca0de682f25f15357a3f9f1a4d94374a1d451d
# then: bash setup_env.sh && bash run_repro.sh
