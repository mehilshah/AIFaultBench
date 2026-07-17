#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout dc9f845ddc54c1df38fdbce5afe03f9fd15813bd
# then: bash setup_env.sh && bash run_repro.sh
