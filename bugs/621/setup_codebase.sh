#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout b4b5244c9c7cdb80d0aaafdb8f35244612788532
# then: bash setup_env.sh && bash run_repro.sh
