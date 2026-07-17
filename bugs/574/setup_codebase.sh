#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 59575da46df964e6161fb0e1a77fa76ea9ce3106
# then: bash setup_env.sh && bash run_repro.sh
