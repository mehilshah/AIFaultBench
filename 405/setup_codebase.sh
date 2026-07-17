#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 181beb3ba4c47098ed8cbc97ee250d1d45ae0107
# then: bash setup_env.sh && bash run_repro.sh
