#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langgraph codebase
git -C codebase checkout df8becd5cfc74bb09ab2d7cbdf17c5559114b8d8
# then: bash setup_env.sh && bash run_repro.sh
