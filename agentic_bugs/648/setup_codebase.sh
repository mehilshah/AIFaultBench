#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout 5796ca9a0ad8ec53dbcf12fa9f1d671b826e5f1d
# then: bash setup_env.sh && bash run_repro.sh
