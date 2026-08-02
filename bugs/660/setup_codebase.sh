#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout f9870bc9aefeb271927ffd5ad558b22e416793ef
# then: bash setup_env.sh && bash run_repro.sh
