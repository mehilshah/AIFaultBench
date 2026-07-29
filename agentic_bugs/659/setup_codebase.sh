#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout d2f97191abc457954dff23ee1d9342516128ec01
# then: bash setup_env.sh && bash run_repro.sh
