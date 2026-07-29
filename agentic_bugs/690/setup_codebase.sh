#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout 30355a7a5df0c7ec49eba125e546c58b7360c10e
# then: bash setup_env.sh && bash run_repro.sh
