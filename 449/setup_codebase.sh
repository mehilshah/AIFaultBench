#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 7b89511f58828f90e86ee118a4fd693bbebe7ba3
# then: bash setup_env.sh && bash run_repro.sh
