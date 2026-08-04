#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/sentence-transformers codebase
git -C codebase checkout 5eb2a1b26b09d7aebc5713252bb0b5c59a643e74
# then: bash setup_env.sh && bash run_repro.sh
