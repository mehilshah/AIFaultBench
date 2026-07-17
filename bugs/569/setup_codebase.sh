#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout ad697ec123f5133e5aae45c97c23d90ea52a1bd8
# then: bash setup_env.sh && bash run_repro.sh
