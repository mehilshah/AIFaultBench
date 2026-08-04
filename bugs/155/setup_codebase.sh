#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 9971e410516146a78972cb9034eec1a408a29ede
# then: bash setup_env.sh && bash run_repro.sh
