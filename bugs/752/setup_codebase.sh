#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 7d4436cac2fd0fe488c3330234abcca0310cbeae
# then: bash setup_env.sh && bash run_repro.sh
