#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langchain codebase
git -C codebase checkout 0501325e6c536a0693565bec99dde038cc5c4d20
# then: bash setup_env.sh && bash run_repro.sh
