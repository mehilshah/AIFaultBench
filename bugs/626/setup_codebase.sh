#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 9036c89ee410b30913ca8b7d362a7d0805583b51
# then: bash setup_env.sh && bash run_repro.sh
