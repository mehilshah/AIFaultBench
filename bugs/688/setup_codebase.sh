#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langchain codebase
git -C codebase checkout 6f7c8f54454ae45b07ca274cbfbb0afb8cef9041
# then: bash setup_env.sh && bash run_repro.sh
