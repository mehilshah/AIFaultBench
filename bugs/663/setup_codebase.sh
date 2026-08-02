#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 9f66e8a649856524ef0ff081a23d58cd071b6ae4
# then: bash setup_env.sh && bash run_repro.sh
