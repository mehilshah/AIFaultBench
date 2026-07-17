#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 5ad982ac517b6e686be6461242313c55755a9dbf
# then: bash setup_env.sh && bash run_repro.sh
