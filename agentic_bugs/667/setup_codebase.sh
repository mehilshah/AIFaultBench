#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 97963c96963f922d41840ec8fbdd1a28311fbc9a
# then: bash setup_env.sh && bash run_repro.sh
