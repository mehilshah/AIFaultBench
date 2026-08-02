#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout a771a4f67e43bb5d2675972496a4e5c70f847052
# then: bash setup_env.sh && bash run_repro.sh
