#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 5c4db60f019a183231cf020e5679baaf1e8c293f
# then: bash setup_env.sh && bash run_repro.sh
