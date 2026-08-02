#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout 97320843fe78b93bd5290ce366841ff9850bf379
# then: bash setup_env.sh && bash run_repro.sh
