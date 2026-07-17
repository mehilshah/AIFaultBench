#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 3b39fd284aa3bcfcad57736cdd5ddb9eb4b746d2
# then: bash setup_env.sh && bash run_repro.sh
