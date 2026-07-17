#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout b3cfca996c8340263cd1fb770a4c5e0b7f400b26
# then: bash setup_env.sh && bash run_repro.sh
