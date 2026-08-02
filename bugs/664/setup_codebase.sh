#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout d601b0f36af4f6362375eefeda509d1070340652
# then: bash setup_env.sh && bash run_repro.sh
