#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 63e161f2965e77b2c3ffcd159ce45b2157a21b43
# then: bash setup_env.sh && bash run_repro.sh
