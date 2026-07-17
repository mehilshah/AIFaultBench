#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 21ba39457d0b9b72dc59ef8aec7981c947c59f6b
# then: bash setup_env.sh && bash run_repro.sh
