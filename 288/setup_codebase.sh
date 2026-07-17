#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 0a9396a25e3c2c399cde4f748ca6b2209b9dafe7
# then: bash setup_env.sh && bash run_repro.sh
