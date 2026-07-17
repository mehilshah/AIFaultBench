#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 8c17d556a8fe9522e10d73d7bd3fad46a6ecae14
# then: bash setup_env.sh && bash run_repro.sh
