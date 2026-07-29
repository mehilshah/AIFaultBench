#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langchain codebase
git -C codebase checkout 6e51a7e48bd61568fd6a58e98a5c9ecba615ee12
# then: bash setup_env.sh && bash run_repro.sh
