#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout 0d4ac836e3a943a6a807910001f84a1d11b52776
# then: bash setup_env.sh && bash run_repro.sh
