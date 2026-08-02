#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout a6dde39be72e0a8f7ea3eea946e0993720e982ce
# then: bash setup_env.sh && bash run_repro.sh
