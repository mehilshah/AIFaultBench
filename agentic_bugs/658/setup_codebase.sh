#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langchain codebase
git -C codebase checkout bc1540084b19eda40a44885d8eaa0a5804b061c8
# then: bash setup_env.sh && bash run_repro.sh
