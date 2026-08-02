#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout 6c6978918e48cc41792ebcd0402e4358bfc12a31
# then: bash setup_env.sh && bash run_repro.sh
