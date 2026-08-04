#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout a7f29523361b2cc12e51c1f5133d95f122f6f45c
# then: bash setup_env.sh && bash run_repro.sh
