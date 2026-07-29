#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout 8ccead9560f6cd76537f632d7a310ba41e38f28b
# then: bash setup_env.sh && bash run_repro.sh
