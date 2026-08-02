#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 91fe33e75ce31d3ca447c017a5ea153ed8b38700
# then: bash setup_env.sh && bash run_repro.sh
