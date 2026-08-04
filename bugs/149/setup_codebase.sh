#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/sentence-transformers codebase
git -C codebase checkout f5f6249e3c46ed56d8c304abf9134af84138c047
# then: bash setup_env.sh && bash run_repro.sh
