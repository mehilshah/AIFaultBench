#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 2a41613f92cef0249e3b8950c24f8d66c9080641
# then: bash setup_env.sh && bash run_repro.sh
