#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout df191731918482c5eaf2934a2df0c9cb3571db0c
# then: bash setup_env.sh && bash run_repro.sh
