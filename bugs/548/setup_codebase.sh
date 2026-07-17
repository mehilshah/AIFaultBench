#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout ea9ddf59fc9d262da7467699959d8c84600c073c
# then: bash setup_env.sh && bash run_repro.sh
