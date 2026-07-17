#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout cac0a28c83cf87b7a05495de3177099c635ba852
# then: bash setup_env.sh && bash run_repro.sh
