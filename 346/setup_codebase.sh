#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout eee480d59810135f45280f8db99f14d0136bed82
# then: bash setup_env.sh && bash run_repro.sh
