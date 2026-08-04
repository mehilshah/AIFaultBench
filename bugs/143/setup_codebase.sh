#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/sentence-transformers codebase
git -C codebase checkout 15d3898c213f833354a37772190465a47bb1d444
# then: bash setup_env.sh && bash run_repro.sh
