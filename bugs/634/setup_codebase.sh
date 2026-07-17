#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 0a4d1c8bac38208fb5b424a510b8a9cef149d1ee
# then: bash setup_env.sh && bash run_repro.sh
