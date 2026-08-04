#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout a30413b78feed68da5c486746f745db092bfdf9a
# then: bash setup_env.sh && bash run_repro.sh
