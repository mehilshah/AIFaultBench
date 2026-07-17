#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout d87f670d5b23860b5937473a5fddbba9d675780a
# then: bash setup_env.sh && bash run_repro.sh
