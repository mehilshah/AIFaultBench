#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 25fcb65d51deef0026aa34e6067703da4a91f956
# then: bash setup_env.sh && bash run_repro.sh
