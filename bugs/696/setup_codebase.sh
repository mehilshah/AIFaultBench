#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 9542621aec4ff90602806525f024a0f5812c5054
# then: bash setup_env.sh && bash run_repro.sh
