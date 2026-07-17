#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout ff3b86b4755b46a7b5656dfcf84d25bd25ad4740
# then: bash setup_env.sh && bash run_repro.sh
