#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 2ae00fb092d1b0e7d74de06e738dd48d04a8b2c2
# then: bash setup_env.sh && bash run_repro.sh
