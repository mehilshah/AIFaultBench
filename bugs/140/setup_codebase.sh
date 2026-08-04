#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/safetensors codebase
git -C codebase checkout 08db34094e9e59e2f9218f2df133b7b4aaff5a99
# then: bash setup_env.sh && bash run_repro.sh
