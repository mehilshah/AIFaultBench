#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langchain codebase
git -C codebase checkout bc5f1517cf7ac27addd4286e388228b8172b93b9
# then: bash setup_env.sh && bash run_repro.sh
